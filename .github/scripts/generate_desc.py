import os

def generate_comment(file_name, base_url, folder_name):
    # 提取不带扩展名的文件名
    file_base_name = os.path.splitext(file_name)[0]
    file_extension = os.path.splitext(file_name)[1]
    
    # 模版注释中的URL部分
    urls = {
        'qx':      f'{base_url}/qx/{file_name}',
        'surge':        f'{base_url}/surge/{file_base_name}.sgmodule',
        'loon':         f'{base_url}/loon/{file_base_name}.plugin',
        'stash':        f'{base_url}/stash/{file_base_name}.stoverride',
    }
    
    # 生成注释文本
    comment_lines = [
        '/*',
        f' * 文件名: {file_base_name}{file_extension}',
        f' * 脚本链接: {urls.get("scripts", "N/A")}',
        f' * Surge 模块链接: {urls.get("Surge", "N/A")}',
        f' * Loon 插件链接: {urls.get("Loon", "N/A")}',
        f' * Stash 覆写链接: {urls.get("Stash", "N/A")}',
        ' */'
    ]

    # 将注释文本合并成单一字符串返回
    return '\n'.join(comment_lines) + '\n\n'

def add_comments_to_files(folders, file_types, base_url):
    # 遍历指定文件夹和文件类型添加注释
    for folder_name in folders:
        # 文件夹完整路径
        folder_path = os.path.join(os.getcwd(), folder_name) 
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(tuple(file_types.keys())):
                    # 文件完整路径
                    file_path = os.path.join(root, file_name) 
                    # 生成注释
                    comment = generate_comment(file_name, base_url, folder_name)

                    # print(file_path)
                    # print(comment)

# 配置信息
folders = ['qx', 'loon', 'surge', 'stash']
file_types = {
    '.js': 'qx',
    '.plugin': 'loon',
    '.sgmodule': 'surge',
    '.stoverride': 'stash',
}
base_url = 'https://raw.githubusercontent.com/ajohn19/TEST/main'

# 执行函数添加注释
add_comments_to_files(folders, file_types, base_url)
