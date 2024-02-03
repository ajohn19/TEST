# author: Levi
# 搭配convert_js_to_stoverride.yml使用。可将qx的js/conf/snippet文件转换为stoverride文件。

import os
import re
import random


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
    # 查找[Mitm]或[Mitm]标签内容
    mitm_match = re.search(r'\[mitm\]\s*([^=\n]+=[^\n]+)\s*', js_content, re.DOTALL | re.IGNORECASE)
    # 如果找到，则进一步处理
    if mitm_match:
        mitm_block = mitm_match.group(1)
        # 移除"hostname ="和空白字符
        mitm_block = re.sub(r'hostname\s*=\s*', '', mitm_block)
        # 分割主机名
        mitm_hosts = mitm_block.strip().split(',')
        # 为每个主机名添加"- "前缀，使其符合stoverride格式
        mitm_content = '\n'.join([f'    - "{host.strip()}"' for host in mitm_hosts if host.strip()])
    # 返回处理后的MITM字符串
    return mitm_content


def script_to_stoverride(js_content):
    script_content = ''
    # 正则表达式匹配 rewrite_local 部分
    rewrite_matches = re.finditer(
        r'^(.*?)(?:\s*url\s+script-(response|request)-(body|header)\s+(.*))$', 
        js_content, 
        re.MULTILINE
    )
    for match in rewrite_matches:
        pattern, method, kind, path = match.groups()
        stoverride_method = 'request' if method == 'request' else 'response'
        # kind 暂时未使用，实际过程中可能需要根据 'body' 和 'header' 修改脚本路径
        script_content += f'  \n- match: "{pattern.strip()}"\n'
        script_content += f'    type: {stoverride_method}\n'
        script_content += f'    require-body: true\n'
        script_content += f'    max-size: -1\n'
        script_content += f'    timeout: 60\n'  
    
    return script_content

# 使用全局变量 random_number
random_number = random.randint(0, 99)

def script_providers_to_stoverride(project_name, script_path):
    # 使用正确的 script_path 作为 url
    url = script_path.strip()
    interval = 86400  # 间隔时间设置为一天
    script_providers_content = (
        f'script-providers:\n'
        f'  "{project_name}_{random_number}":\n'
        f'    url: {url}\n'
        f'    interval: {interval}\n'
    )
    return script_providers_content


def js_to_stoverride(js_content):
    # Check for the presence of the [rewrite_local] and [mitm]/[MITM] sections
    if not (re.search(r'\[rewrite_local\]', js_content, re.IGNORECASE) or
            re.search(r'\[mitm\]', js_content, re.IGNORECASE) or
            re.search(r'\[MITM\]', js_content, re.IGNORECASE)):
        return None
    
    # Extract information from the JS content
    name_match = re.search(r'项目名称：(.*?)\n', js_content)
    desc_match = re.search(r'使用说明：(.*?)\n', js_content)

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

    # Create the final stoverride content string
    stoverride_content = (
        f"name: |-\n  {project_name}\ndesc: |-\n  {project_desc}\n\n"
        "http:\n\n"
    )

    # Process mitm content
    mitm_section = mitm_to_stoverride(js_content)
    if mitm_section:
        stoverride_content += f"  mitm:\n{mitm_section}\n"

    # Extract the script section
    script_section = script_to_stoverride(js_content)
    if script_section:
        stoverride_content += f"\n  script:{script_section}\n"

    # Search for the URL pattern in the rewrite_local section and retrieve the first match
    url_pattern = r'url\s+script-(?:response-body|request-body|response-header|request-header|echo-response|analyze-echo-response)\s+(\S+)'
    url_match = re.search(url_pattern, js_content, re.IGNORECASE)
    
    # If a URL match is not found, throw an error
    if not url_match:
        raise ValueError("未找到脚本路径。请确保在 js/conf/snippet 文件中包含了至少一个有效的链接.")

    script_path = url_match.group(1).strip()

    # Add the script-providers section with the project name and the extracted script path
    script_providers_section = script_providers_to_stoverride(project_name, script_path)
    stoverride_content += f"\n{script_providers_section}\n"

    # Process task_local section
    task_local_section = task_local_to_stoverride(js_content)
    if task_local_section:
        stoverride_content += f"\n{task_local_section}\n"

    # Return the final stoverride content
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
