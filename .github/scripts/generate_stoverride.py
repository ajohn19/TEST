# author:Levi
# 搭配convert_js_to_stoverride.yml使用。可将qx的js/conf/snippet文件转换为stoverride文件。

import os
import re

def task_local_to_stoverride(js_content):
    cron_content = ''
    # 定义解析cron配置的正则表达式
    cron_block_match = re.search(r'\[cron\](.*?)\n\[', js_content, re.DOTALL | re.IGNORECASE)
    if cron_block_match:
        cron_block = cron_block_match.group(1)
        # 单独提取每一个cron任务
        cron_tasks = cron_block.strip().split('\n\n')
        for task in cron_tasks:
            # 从cron任务中提取信息
            cron_match = re.search(r'([^\s]+)\s+(.*?)\s([\s\S]+)', task)
            cron_entry = cron_match.groups() if cron_match else None
            if cron_entry:
                name, expression, specifics = cron_entry
                cron_content += f'  script:\n    - name: "{name}"\n      cron: "{expression}"{specifics}'
    # 如果有cron配置，则返回对应的stoverride格式的字符串
    return cron_content


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
    hostname_content = hostname_match.group(1).strip() if hostname_match else ''

    mitm_content_with_append = (mitm_content)

    # Generate stoverride content
    stoverride_content = f"""
name: |-
{project_name}
desc: |-
{project_desc}
"""

    # 调用函数转换cron配置
    cron_stoverride_content = task_local_to_stoverride(js_content)
    if cron_stoverride_content:
        stoverride_content += f"\ncron:{cron_stoverride_content}\n"

    # 将rewrite规则转换为stoverride格式的逻辑代码
    script_content = ''
    rewrite_local_pattern = r'^(.*?)\s*url\s+script-(response-body|request-body|echo-response|request-header|response-header|analyze-echo-response)\s+(\S+)'
    rewrite_local_matches = re.finditer(rewrite_local_pattern, js_content, re.MULTILINE)
    for match in rewrite_local_matches:
        pattern, script_type, script_path = match.groups()
        script_type_alt = 'http-request' if 'request-body' in script_type or 'request-header' in script_type else 'http-response'
        specific_settings = match.group(4)  # 这部分要保持原样，对应具体脚本设置
        script_content += f"\n    - match: \"{pattern}\"\n      type: \"{script_type_alt}\"\n      require-body: true\n      max-size: -1\n      timeout: 60{specific_settings}\n"

    if script_content:
        stoverride_content += f"  script:{script_content}"

    # 省略其他内容...

    return stoverride_content

def main():
    # Process files in the 'scripts' folder
    qx_folder_path = 'scripts'
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
