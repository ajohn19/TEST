import os

def generate_comment(file_name, base_url, folder_name):
    """
    Generate a comment block with URLs based on the file name, base URL, and folder name.
    """
    file_base_name, file_extension = os.path.splitext(file_name)
    
    # URL templates based on different folders and file extensions
    urls = {
        'qx': f'{base_url}/{folder_name}/{file_name}',
        'surge': f'{base_url}/surge/{file_base_name}.sgmodule',
        'loon': f'{base_url}/loon/{file_base_name}.plugin',
        'stash': f'{base_url}/stash/{file_base_name}.stoverride',
    }
    
    comment_lines = [
        '/*',
        f' * 项目名称: {file_base_name}{file_extension}',
        f' * Quantumult X 链接: {urls.get("qx", "N/A")}',
        f' * Surge 模块链接: {urls.get("surge", "N/A")}',
        f' * Loon 插件链接: {urls.get("loon", "N/A")}',
        f' * Stash 覆写链接: {urls.get("stash", "N/A")}',
        ' */\n',
    ]
    
    return '\n'.join(comment_lines)

def add_or_update_comments(base_url):
    """
    Traverse folders and add or update comments for files.
    """
    folders = {
        'qx': ['.js', '.conf', '.snippet'],
        'surge': ['.sgmodule'],
        'loon': ['.plugin'],
        'stash': ['.stoverride']
    }

    for folder_name, extensions in folders.items():
        folder_path = os.path.join(os.getcwd(), folder_name)
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if any(file_name.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r+', encoding='utf-8') as file:
                        content = file.read()
                        comment = generate_comment(file_name, base_url, folder_name)
                        content_without_comment = strip_top_comment_block(content)
                        file.seek(0, 0)
                        file.write(comment + content_without_comment)

def strip_top_comment_block(content):
    """
    Strip the top comment block if it exists.
    """
    if content.lstrip().startswith('/*'):
        end_comment_idx = content.find('*/') + 2
        return content[end_comment_idx:].lstrip()
    return content

base_url = 'https://raw.githubusercontent.com/ajohn19/TEST/main'
add_or_update_comments(base_url)
