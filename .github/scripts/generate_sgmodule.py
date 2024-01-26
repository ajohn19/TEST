import os
import re
from github import Github

def insert_append(content):
    # Insert %APPEND% after the first '=' sign
    return re.sub(r'=', '= %APPEND%', content, count=1)

def js_to_sgmodule(js_content):
    # Extract information from the JS content
    name_match = re.search(r'项目名称：(.*?)\n', js_content)
    desc_match = re.search(r'使用说明：(.*?)\n', js_content)
    rewrite_matches = re.finditer(r'\[rewrite_local\]\s*(.*?)\s*(?:(?:\[|\[mitm\]).*?(?=\[|$))', js_content, re.DOTALL)
    mitm_match = re.search(r'\[mitm\].*?hostname\s*=\s*(.*?)(?:\[|$)', js_content, re.DOTALL)
    
    if not rewrite_matches:
        raise ValueError("No [rewrite_local] rule found")

    if name_match:
        project_name = name_match.group(1).strip()
    else:
        # If "项目名称" is not found, use the last part of the first URL as the project name
        project_name = re.search(r'\[rewrite_local\]\s*(.*?)(?:\[|\[mitm\])', js_content, re.DOTALL).group(1).split()[-1].rsplit('/', 1)[-1].split('.', 1)[0]
    
    project_desc = desc_match.group(1).strip() if desc_match else f"Generated from {project_name}"
    mitm_content = f"hostname = %APPEND% {mitm_match.group(1).strip()}" if mitm_match else ''

    sgmodule_content = f"""#!name={project_name}
#!desc={project_desc}

[MITM]
{mitm_content}

[Script]
"""

    # Process each rewrite rule
    for match in rewrite_matches:
        rewrite_local_content = match.group(1).strip()

        # Extract pattern and script from rewrite_local_content
        pattern_script_match = re.search(r'^(.*?)\s*url\s+script-(response|request|echo-response|request-header|response-header|analyze-echo-response)\s+(.*)$', rewrite_local_content, re.MULTILINE)
        if not pattern_script_match:
            raise ValueError("Invalid rewrite_local format")

        pattern = pattern_script_match.group(1).strip()
        script_type = pattern_script_match.group(2).strip()
        script_path = pattern_script_match.group(3).strip()

        # Insert %APPEND% into pattern
        pattern_with_append = insert_append(pattern)

        # Generate sgmodule content for each rule
        sgmodule_content += f"{project_name} = type=http-{script_type},pattern={pattern_with_append},requires-body=1,max-size=0,script-path={script_path}\n"

    return sgmodule_content

def main():
    # Process each file in the 'qx' folder
    qx_folder_path = 'qx'
    if not os.path.exists(qx_folder_path):
        print(f"Error: {qx_folder_path} does not exist.")
        return

    for file_name in os.listdir(qx_folder_path):
        if file_name.endswith(".js"):
            file_path = os.path.join(qx_folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as js_file:
                js_content = js_file.read()
                sgmodule_content = js_to_sgmodule(js_content)

                # Write sgmodule content to surge folder
                surge_folder_path = 'surge'
                os.makedirs(surge_folder_path, exist_ok=True)
                sgmodule_file_path = os.path.join(surge_folder_path, f"{file_name.split('.')[0]}.sgmodule")
                with open(sgmodule_file_path, "w", encoding="utf-8") as sgmodule_file:
                    sgmodule_file.write(sgmodule_content)

                print(f"Generated {sgmodule_file_path}")

                # Add a dummy change and commit
                with open(file_path, 'a', encoding='utf-8') as js_file:
                    js_file.write("\n// Adding a dummy change to trigger git commit\n")

                os.system(f'git add {file_path}')
                os.system('git commit -m "Trigger update"')

if __name__ == "__main__":
    main()
