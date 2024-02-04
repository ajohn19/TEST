import os
import re

# 定义函数提取旧的注释块
def extract_old_comment(content):
    pattern = r'/\*[\s\S]*?\*/'
    match = re.search(pattern, content)
    return match.group() if match else None

# 定义函数生成新的注释块，包括更新的链接
def generate_new_comment(file_path, base_url, old_comment):
    # 提取文件名作为项目名称
    file_name = os.path.basename(file_path)
    project_name = os.path.splitext(file_name)[0]

    # 定义链接
    qx_url = f'{base_url}/qx/{file_name}'
    surge_url = f'{base_url}/surge/{project_name}.sgmodule'
    loon_url = f'{base_url}/loon/{project_name}.plugin'
    stash_url = f'{base_url}/stash/{project_name}.stoverride'

    # 如果旧注释存在，保留它们除项目名称和链接外的所有内容
    if old_comment:
        old_comment = re.sub(r'项目名称:.*', '', old_comment)
        old_comment = re.sub(r'Quantumult X 链接:.*', '', old_comment)
        old_comment = re.sub(r'Surge 模块链接:.*', '', old_comment)
        old_comment = re.sub(r'Loon 插件链接:.*', '', old_comment)
        old_comment = re.sub(r'Stash 覆写链接:.*', '', old_comment)
        old_comment_lines = old_comment.splitlines()[1:-1] # 移除注释开头和结尾的符号
    else:
        old_comment_lines = []

    # 生成新的注释块
    new_comment_lines = [
        '/*',
        f' * 项目名称: {project_name}',
        f' * Quantumult X 链接: {qx_url}',
        f' * Surge 模块链接: {surge_url}',
        f' * Loon 插件链接: {loon_url}',
        f' * Stash 覆写链接: {stash_url}',
    ] + old_comment_lines + [' */']

    return '\n'.join(new_comment_lines)

# 更新文件中的注释
def update_file_comment(file_path, base_url):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        old_comment = extract_old_comment(content)
        new_comment = generate_new_comment(file_path, base_url, old_comment)
        updated_content = re.sub(r'/\*[\s\S]*?\*/', new_comment, content, count=1)
        file.seek(0)
        file.write(updated_content)
        file.truncate()

# 处理文件夹下的所有文件
def process_qx_folder(qx_folder, base_url):
    for file_name in os.listdir(qx_folder):
        if file_name.endswith(('.js', '.conf', '.snippet')): 
            file_path = os.path.join(qx_folder, file_name)
            update_file_comment(file_path, base_url)

# GitHub 仓库的基础 URL
base_url = 'https://raw.githubusercontent.com/ajohn19/TEST/main'

# 'qx' 文件夹路径
qx_folder = 'qx'

# 进行文件处理
process_qx_folder(qx_folder, base_url)
