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
    mitm_match = re.search(r'\[mitm\]\s*hostname\s*=\s*([^=\n]+=[^\n]+)\s*', js_content, re.DOTALL | re.MULTILINE)

    if not (name_match and desc_match):
        # If project name or description is not found, use the last part of the URL
        url_matches = re.findall(r'url\s+script-(?:response-body|request-body|response-header|request-header|echo-response|analyze-echo-response)\s+(.*?)$', js_content, re.MULTILINE)
        if not url_matches:
            raise ValueError("Invalid JS file format")
        project_name = project_desc = os.path.splitext(os.path.basename(url_matches[-1]))[0]
    else:
        project_name = name_match.group(1).strip()
        project_desc = desc_match.group(1).strip()

    # Extract and insert %APPEND% into mitm content
    mitm_content = mitm_match.group(1).strip() if mitm_match else ''
    mitm_content_with_append = insert_append(mitm_content)

    # Extract and process each rewrite_local rule
    rewrite_local_matches = re.finditer(r'\[rewrite_local\]\s*(.*?)\s*(?:(?=\[|$))', js_content, re.DOTALL | re.MULTILINE)
    if not rewrite_local_matches:
        raise ValueError(f"No [rewrite_local] rule found\nJS content:\n{js_content}")

    # Generate sgmodule content for each rewrite_local rule
    sgmodule_content = ""
    for match in rewrite_local_matches:
        rewrite_local_content = match.group(1).strip()

        # Extract pattern and script from rewrite_local_content
        pattern_script_matches = re.finditer(r'^\s*(.*?)\s*url\s+script-(response|request|echo-response|request-header|response-header|analyze-echo-response)\s+(.*?)$', rewrite_local_content, re.MULTILINE)
        if not pattern_script_matches:
            raise ValueError(f"Invalid rewrite_local format\nRewrite_local content:\n{rewrite_local_content}")

        # Generate sgmodule content for each pattern_script_match
        for pattern_script_match in pattern_script_matches:
            pattern = pattern_script_match.group(1).strip()
            script_type = pattern_script_match.group(2).strip()
            script = pattern_script_match.group(3).strip()

            # Generate sgmodule content
            sgmodule_content += f"""#!name={project_name}
#!desc={project_desc}

[Script]
{project_name} = type=http-{script_type},pattern={pattern},requires-body=1,max-size=0,script-path={script}

[MITM]
{mitm_content_with_append}
"""

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
