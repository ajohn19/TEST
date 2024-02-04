import os

def generate_comment(file_name, base_url, folder_name):
    """
    Generate a comment block with URLs based on file name, base URL, and folder.
    """
    file_base_name = os.path.splitext(file_name)[0]
    file_extension = os.path.splitext(file_name)[1]
    
    urls = {
        'qx': base_url + '/qx/' + file_name,
        'surge': base_url + '/surge/' + file_base_name + '.sgmodule',
        'loon': base_url + '/loon/' + file_base_name + '.plugin',
        'stash': base_url + '/stash/' + file_base_name + '.stoverride',
    }
    
    comment_lines = [
        '/*',
        f' * 文件名: {file_base_name}{file_extension}',
        f' * Quantumult X 链接: {urls.get("qx", "N/A")}',
        f' * Surge 模块链接: {urls.get("surge", "N/A")}',
        f' * Loon 插件链接: {urls.get("loon", "N/A")}',
        f' * Stash 覆写链接: {urls.get("stash", "N/A")}',
        ' */\n'
    ]
    
    return '\n'.join(comment_lines)

def add_comments_to_files():
    """
    Traverses directories and adds comments to files.
    """
    base_url = 'https://raw.githubusercontent.com/ajohn19/TEST/main'
    
    # Define folder to file extension mapping
    folders = {
        'qx': '.js',
        'surge': '.sgmodule',
        'loon': '.plugin',
        'stash': '.stoverride',
    }
    
    # Traverse directories and add comments
    for folder_name, extension in folders.items():
        folder_path = os.path.join(os.getcwd(), folder_name)
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(extension):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r+', encoding='utf-8') as file:
                        content = file.read()
                        if content.startswith('/*'):
                            continue  # Skip if comment already exists
                        comment = generate_comment(file_name, base_url, folder_name)
                        file.seek(0, 0)
                        file.write(comment + content)

add_comments_to_files()
