# author: Levi
# 搭配convert_js_to_stoverride.yml使用。可将qx的js/conf/snippet文件转换为stoverride文件。

import os
import re

def insert_append(content):
    # Insert - after the first '=' sign
    return re.sub(r'=', '= -', content, count=1)

def task_local_to_stoverride(js_content):
    cron_content = ''
    cron_match = re.search(r'\[task_local\](.*?)\n\[', js_content, re.DOTALL | re.IGNORECASE)
    if cron_match:
        cron_block = cron_match.group(1)
        cron_entries = re.finditer(r'((?:(?:\d+\s?\*|\*,?){5,6})\s+)(\S+)', cron_block)
        for cron_entry in cron_entries:
            cron, script = cron_entry.groups()
            cron_content += f'\n    - name: "cron_{os.path.basename(script)}"\n      cron: "{cron.strip()}"\n      script-path: {script.strip()}\n      timeout: 60\n'
    return cron_content

def mitm_to_stoverride(js_content):
    mitm_content = ''
    mitm_match = re.search(r'\[mitm\](.*?)\n\[', js_content, re.DOTALL | re.IGNORECASE)
    if mitm_match:
        mitm_block = mitm_match.group(1)
        mitm_hosts = mitm_block.strip().split(',')
        mitm_content = '\n'.join([f'    - "{host.strip()}"' for host in mitm_hosts if host.strip()])
    return mitm_content

def js_to_stoverride(js_content):
    # Check for the presence of the [rewrite_local] and [mitm]/[MITM] sections
    if not (re.search(r'\[rewrite_local\]', js_content, re.IGNORECASE) or
            re.search(r'\[mitm\]', js_content, re.IGNORECASE) or
            re.search(r'\[MITM\]', js_content, re.IGNORECASE)):
        return None
    
    # Extract information from the JS content
    name_match = re.search(r'项目名称：(.*?)\n', js_content)
    desc_match = re.search(r'使用说明：(.*?)\n', js_content)
    mitm_match = re.search(r'\[mitm\]\s*([^=\n]+=[^\n]+)\s*', js_content, re.DOTALL | re.IGNORECASE)
    hostname_match = re.search(r'hostname\s*=\s*([^=\n]+=[^\n]+)\s*', js_content, re.DOTALL | re.IGNORECASE)

    
    # If there is no project name and description, use the last part of the matched URL as the project name
    if not (name_match and desc_match):
        url_pattern = r'url\s+script-(?:response-body|request-body|echo-response|request-header|response-header|analyze-echo-response)\s+(\S+.*?)$'
        last_part_match = re.search(url_pattern, js_content, re.MULTILINE)
        if last_part_match:
            project_name = os.path.splitext(os.path.basename(last_part_match.group(1).strip()))[0]
        else:
            raise ValueError("文件内容匹配错误，请按照要求修改，详情请按照levifree.tech文章内容修改")

        project_desc = f"{project_name} is automatically converted by LEVI SCRIPT; if not available plz use Script-Hub."

    else:
        project_name = name_match.group(1).strip()
        project_desc = desc_match.group(1).strip()

    mitm_content = mitm_match.group(1).strip() if mitm_match else ''

    mitm_content_with_append = (mitm_content)

    # Insert - into mitm and hostname content
    mitm_content_with_append = insert_append(mitm_content)

    # Create the final stoverride content string
    stoverride_content = (
        f"name: |-\n  {project_name}\ndesc: |-\n  {project_desc}\n\n"
        "http:\n\n"
    )

    if mitm_content_with_append:
        stoverride_content += f"  mitm:\n"{mitm_content_with_append}"\n  require-body: true\n  max-size: -1\n  timeout: 60"

    # convert and add [task_local] section
    task_local_stoverride_content = task_local_to_stoverride(js_content)
    stoverride_content += task_local_stoverride_content
    
    # Regex pattern to find rewrite_local
    rewrite_local_pattern = r'^(.*?)\s*url\s+script-(response-body|request-body|echo-response|request-header|response-header|analyze-echo-response)\s+(\S+)'
    rewrite_local_matches = re.finditer(rewrite_local_pattern, js_content, re.MULTILINE)

    for match in rewrite_local_matches:
        pattern = match.group(1).strip()
        script_type = match.group(2).replace('-body', '').replace('-header', '').strip()
        script_path = match.group(3).strip()

        # Append the rewrite rule to the stoverride content
        stoverride_content += f"\ncron:\n{task_local_to_stoverride}\n"

    return stoverride_content

def main():
    # Process files in the 'qx' folder
    qx_folder_path = 'qx'
    if not os.path.exists(qx_folder_path):
        print(f"Error: {qx_folder_path} does not exist.")
        return

    # Define the supported file extensions
    supported_extensions = ('.js', '.conf', '.snippet')

    for file_name in os.listdir(qx_folder_path):
        if file_name.endswith(supported_extensions):
            # File extension check for .js, .conf, or .snippet
            file_path = os.path.join(qx_folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                js_content = file.read()
                stoverride_content = js_to_stoverride(js_content)
                
                if stoverride_content is not None:
                    # Write stoverride content to 'stash' folder if stoverride_content is not None
                    stash_folder_path = 'stash'
                    os.makedirs(stash_folder_path, exist_ok=True)
                    stoverride_file_path = os.path.join(stash_folder_path, f"{os.path.splitext(file_name)[0]}.stoverride")
                    
                    with open(stoverride_file_path, "w", encoding="utf-8") as stoverride_file:
                        stoverride_file.write(stoverride_content)
                    print(f"Generated {stoverride_file_path}")
                else:
                    # Skip files without the required sections
                    print(f"跳过 {file_name} 由于文件缺失匹配内容，请仔细检查.")

                # Since we're simulating a git operation, we'll do this for all file types
                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write("\n// Adding a dummy stoverride change to trigger git commit\n")
                os.system(f'git add {file_path}')
                os.system('git commit -m "Trigger update"')

if __name__ == "__main__":
    main()
