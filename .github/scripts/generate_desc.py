import os

def generate_comment(file_name, base_url, folder_name):
    """
    Generate a comment block with URLs based on the file name, base URL, and folder name.
    """
    file_base_name = os.path.splitext(file_name)[0]
    file_extension = os.path.splitext(file_name)[1]
    
    # URL templates based on different folders and file extensions
    url_templates = {
        'qx': f'{base_url}/{folder_name}/{file_name}',
        'surge': f'{base_url}/surge/{file_base_name}.sgmodule',
        'loon': f'{base_url}/loon/{file_base_name}.plugin',
        'stash': f'{base_url}/stash/{file_base_name}.stoverride',
    }
    
    # Generating comment text
    comment_lines = [
        '/*******************************************',
        f' * 文件名: {file_base_name}{file_extension}',
        f' * Quantumult X 脚本链接: {url_templates["qx"]}',
        f' * Surge 模块链接: {url_templates.get("surge", "N/A")}',
        f' * Loon 插件链接: {url_templates.get("loon", "N/A")}',
        f' * Stash 覆写链接: {url_templates.get("stash", "N/A")}',
        ' *******************************************/',
    ]
    
    return '\n'.join(comment_lines) + '\n'

def add_comments_to_files():
    """
    Traverses the specified folders and adds comments to the files.
    """
    base_url = 'https://raw.githubusercontent.com/ajohn19/TEST/main'
    file_extensions = ['.js', '.conf', '.snippet']
    
    folders = {
        'qx': file_extensions,  # QX folder can contain multiple types of extensions
        'surge': '.sgmodule',
        'loon': '.plugin',
        'stash': '.stoverride',
    }
    
    for folder_name, extensions in folders.items():
        folder_path = os.path.join(os.getcwd(), folder_name)
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if isinstance(extensions, list):  
                    valid_extensions = extensions
                else:
                    valid_extensions = [extensions]
                if any(file_name.endswith(ext) for ext in valid_extensions):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r+', encoding='utf-8') as file:
                        content = file.read()
                        if content.startswith('/*'):
                            continue  # Already contains a comment
                        comment = generate_comment(file_name, base_url, folder_name)
                        file.seek(0, 0)
                        file.write(comment + content)

add_comments_to_files()
