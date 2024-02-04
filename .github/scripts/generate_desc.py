import os
import re

def extract_usage_content(content, start_label='使用说明', end_label='*/'):
    # Use non-greedy regex to capture all text between the start and end labels
    usage_pattern = rf'{start_label}:(.*?){end_label}'
    usage_match = re.search(usage_pattern, content, re.DOTALL)
    if usage_match:
        # Return the match, stripping any leading or trailing whitespace
        return usage_match.group(1).strip()
    return None

def generate_comment(project_name, file_name, base_url, usage_content=None):
    qx_url = f'{base_url}/qx/{file_name}'

    # Generate the new comment block
    comment_lines = [
        '/*',
        f' * 项目名称: {project_name}',
        f' * Quantumult X 链接: {qx_url}',
        ' * Surge 模块链接: N/A',  
        ' * Loon 插件链接: N/A',  
        ' * Stash 覆写链接: N/A',
    ]

    # Add usage instructions if available
    if usage_content:
        comment_lines.append(' * 使用说明:')
        usage_lines = usage_content.split('\n')
        comment_lines.extend([f' * {line.strip()}' for line in usage_lines])

    comment_lines.append(' */\n')
    return '\n'.join(comment_lines)

def update_file_comment(file_path, base_url):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()

        # Extract the project name and usage content from the original comments
        project_name = extract_usage_content(content, '项目名称', '使用说明')
        usage_content = extract_usage_content(content, '使用说明', '*/')

        if not project_name:
            print(f"Project name not found in {file_path}")
            return

        # Generate the new comment
        new_comment = generate_comment(project_name, os.path.basename(file_path), base_url, usage_content)

        # Replace the old comment block with the new one
        # This regex matches the entire old comment block
        new_content = re.sub(r'/\*.*?\*/', new_comment, content, count=1, flags=re.DOTALL)

        # Write the updated content back to the file
        file.seek(0)
        file.write(new_content)
        file.truncate()

def process_qx_folder(base_url):
    qx_folder = 'qx'
    qx_path = os.path.join(os.getcwd(), qx_folder)
    for file_name in os.listdir(qx_path):
        if file_name.endswith(('.js', '.conf', '.snippet')):
            file_path = os.path.join(qx_path, file_name)
            update_file_comment(file_path, base_url)

base_url = 'https://raw.githubusercontent.com/ajohn19/TEST/main'  # Replace with your repository details
process_qx_folder(base_url)
