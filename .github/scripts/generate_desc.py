import os
import re

def replace_urls_and_project_name(content, base_url, file_name, project_name):
    # 更新注释块中的链接和项目名称
    content = re.sub(r'\* Quantumult X 链接:.*', f'* Quantumult X 链接: {base_url}/qx/{file_name}', content)
    content = re.sub(r'\* Surge 模块链接:.*', f'* Surge 模块链接: {base_url}/surge/{project_name}.sgmodule', content)
    content = re.sub(r'\* Loon 插件链接:.*', f'* Loon 插件链接: {base_url}/loon/{project_name}.plugin', content)
    content = re.sub(r'\* Stash 覆写链接:.*', f'* Stash 覆写链接: {base_url}/stash/{project_name}.stoverride', content)
    content = re.sub(r'\* 项目名称:.*', f'* 项目名称: {project_name}', content)

    return content

def extract_and_update_comment_block(old_comment, base_url, file_name):
    # 从旧注释中提取项目名称
    project_name_match = re.search(r'\* 项目名称: (.+?)\s*\*', old_comment)
    if project_name_match:
        project_name = project_name_match.group(1).strip()
    else:
        project_name = '未命名项目'

    # 替换链接并返回完整的新注释块
    return replace_urls_and_project_name(old_comment, base_url, file_name, project_name)

def update_file_comment(file_path, base_url):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        # 匹配并提取旧的注释块
        old_comment_pattern = r'/\*[\s\S]*?\*/'
        old_comment_match = re.search(old_comment_pattern, content)
        if old_comment_match:
            new_comment_block = extract_and_update_comment_block(old_comment_match.group(0), base_url, os.path.basename(file_path))
            # 新的注释块替换旧的注释块
            updated_content = content.replace(old_comment_match.group(0), new_comment_block)
            file.seek(0)
            file.write(updated_content)
            file.truncate()
        else:
            print(f"No existing comment block found in {file_path}")

def process_qx_folder(qx_folder, base_url):
    for file_name in os.listdir(qx_folder):
        if file_name.endswith(('.js', '.conf', '.snippet')):
            file_path = os.path.join(qx_folder, file_name)
            update_file_comment(file_path, base_url)

# 设置为您的仓库路径
base_url = 'https://raw.githubusercontent.com/ajohn19/TEST/main'
# 设置为具体的 qx 文件夹路径
qx_folder = 'TEST/qx'

process_qx_folder(qx_folder, base_url)
