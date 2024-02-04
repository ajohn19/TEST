import os

# Function to insert the new comment block at the beginning of the file content
def insert_comment_at_beginning(content, filename, base_url):
    # Extract base file name and extension
    file_base_name, file_extension = os.path.splitext(filename)
    # Remove the dot from extension
    file_extension = file_extension[1:]
    # Define the URLs in a dictionary
    urls = {
        'qx': f'{base_url}/qx/{filename}',
        'surge': f'{base_url}/surge/{file_base_name}.sgmodule',
        'loon': f'{base_url}/loon/{file_base_name}.plugin',
        'stash': f'{base_url}/stash/{file_base_name}.stoverride'
    }

    # Create the new comment block with URLs
    new_comment_block = (
        f'/*\n'
        f' * 文件名称: {file_base_name}{file_extension}\n'
        f' * Quantumult X 脚本链接: {urls.get("qx", "N/A")}\n'
        f' * Surge 模块链接: {urls.get("surge", "N/A")}\n'
        f' * Loon 插件链接: {urls.get("loon", "N/A")}\n'
        f' * Stash 覆写链接: {urls.get("stash", "N/A")}\n'
        '*/\n'
    )
    
    # Insert the new comment block at the beginning of the content
    return new_comment_block + '\n' + content

    # Call the function to insert the comment at the beginning
    updated_content = insert_comment_at_beginning(original_content, filename, base_url)
    print(updated_content)

main()
