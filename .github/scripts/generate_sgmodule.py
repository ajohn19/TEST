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
    # Replace with your GitHub repository details
    repo_owner = "ajohn19"
    repo_name = "TEST"

    # Replace with your GitHub personal access token
    github_token = "sgmoduleToken"

    # Connect to GitHub repository
    g = Github(github_token)
    repo = g.get_user(repo_owner).get_repo(repo_name)

    # Create 'surge' folder if it doesn't exist
    surge_folder = "surge"
    if not os.path.exists(surge_folder):
        os.makedirs(surge_folder)

    # Process each file in the 'qx' folder
    qx_folder_contents = repo.get_contents("qx")
    for file in qx_folder_contents:
        if file.type == "file" and file.name.endswith(".js"):
            js_content = file.decoded_content.decode("utf-8")
            sgmodule_content = js_to_sgmodule(js_content)

            # Write sgmodule content to surge folder
            sgmodule_file_path = os.path.join(surge_folder, f"{file.name.split('.')[0]}.sgmodule")
            with open(sgmodule_file_path, "w", encoding="utf-8") as sgmodule_file:
                sgmodule_file.write(sgmodule_content)

            print(f"Generated {sgmodule_file_path}")

if __name__ == "__main__":
    main()
