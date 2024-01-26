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
    rewrite_match = re.findall(r'\[rewrite_local\]\s*(.*?)\s*(?=\[|\n|$)', js_content, re.DOTALL | re.MULTILINE)
    mitm_match = re.search(r'\[mitm\]\s*hostname\s*=\s*([^=\n]+=[^\n]+)\s*', js_content, re.DOTALL | re.MULTILINE)

    if not rewrite_match:
        raise ValueError("No [rewrite_local] rule found")

    project_name = name_match.group(1).strip() if name_match else "rewrite_match[0].split()[-1].split('/')[-1].split('.')[0]
    project_desc = desc_match.group(1).strip() if desc_match else f"Generated from {rewrite_match[0].split()[-1].split('/')[-1].split('.')[0]}"

    mitm_content = mitm_match.group(1).strip() if mitm_match else ''

    # Insert %APPEND% into mitm content
    mitm_content_with_append = insert_append(mitm_content)

    # Generate sgmodule content
    sgmodule_content = f"""#!name={project_name}
#!desc={project_desc}

[MITM]
{mitm_content_with_append}

[Script]
"""

    # Process each rewrite_local rule
    for rule in rewrite_match:
        pattern_script_match = re.search(r'^(.*?)\s*url\s+script-(response|request|echo-response|request-header|response-header|analyze-echo-response)\s+(.*)$', rule, re.MULTILINE)
        if not pattern_script_match:
            raise ValueError("Invalid rewrite_local format")

        pattern = pattern_script_match.group(1).strip()
        script = pattern_script_match.group(2).strip()

        # Insert %APPEND% into pattern
        pattern_with_append = insert_append(pattern)

        # Append to sgmodule content
        sgmodule_content += f"{project_name} = type=http-{script},pattern={pattern_with_append},requires-body=1,max-size=0,script-path={script}\n"

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
