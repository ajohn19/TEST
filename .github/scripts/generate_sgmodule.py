import os
import re
from github import Github

def js_to_sgmodule(js_content):
    # Extract information from the JS content
    name_match = re.search(r'项目名称：(.*?)\n', js_content)
    desc_match = re.search(r'使用说明：(.*?)\n', js_content)
    rewrite_match = re.search(r'\[rewrite_local\]\s*(.*?)\s*\[mitm\]\s*hostname\s*=\s*(.*?)\s*', js_content, re.DOTALL | re.MULTILINE)

    if not (name_match and desc_match and rewrite_match):
        raise ValueError("Invalid JS file format")

    project_name = name_match.group(1).strip()
    project_desc = desc_match.group(1).strip()

    rewrite_local_content = rewrite_match.group(1).strip()
    mitm_hostname = rewrite_match.group(2).strip()

    # Generate sgmodule content
    sgmodule_content = f"""#!name={project_name}
#!desc={project_desc}

[Script]
{project_name} = {rewrite_local_content},requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/Yu9191/Rewrite/main/{project_name}.js

[MITM]
hostname= %APPEND% {mitm_hostname}
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

if __name__ == "__main__":
    main()
