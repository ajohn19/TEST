import os
import re

def contains_required_sections(js_content):
    # Check for the existence of [rewrite_local] or [MITM]/[mitm] sections
    return re.search(r'\[rewrite_local\]', js_content, re.IGNORECASE) or re.search(r'\[MITM\]', js_content, re.IGNORECASE)

def extract_header_info(js_content):
    name_match = re.search(r'项目名称：(.*?)\n', js_content)
    desc_match = re.search(r'使用说明：(.*?)\n', js_content)
    project_name = project_desc = img_url = ""

    if name_match and desc_match:
        project_name = name_match.group(1).strip()
        project_desc = desc_match.group(1).strip()
    else:
        rewrite_url_match = re.search(
            r'url\s+script-(?:response|request)-(?:body|header)\s+(https?:\/\/[^\/]+\/[^\/]+\/[^\/]+\/([^\/]+)\.\w+)',
            js_content
        )
        if rewrite_url_match:
            project_name = project_desc = rewrite_url_match.group(2)

    img_url_match = re.search(r'img-url=(https?://[^\s,"]+)', js_content)
    if img_url_match:
        img_url = img_url_match.group(1).strip()

    return project_name or 'DefaultProjectName', project_desc or 'DefaultProjectDescription', img_url

# Other functions (`extract_rules` and `convert_js_to_loon`) remain the same as before

# Set up the base repository path and the directories for qx and loon
base_path = os.getcwd()
qx_path = os.path.join(base_path, 'qx')
loon_path = os.path.join(base_path, 'loon')

# Create the 'loon' directory if it does not exist
if not os.path.exists(loon_path):
    os.makedirs(loon_path)

# Loop through all files in the 'qx' directory
for root, dirs, files in os.walk(qx_path):
    for file_name in files:
        # Only process files with the correct extensions
        if file_name.lower().endswith(('.js', '.conf', '.snippet')):
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r') as file:
                js_content = file.read()
            
            # Skip the conversion if the file does not contain the required sections
            if not contains_required_sections(js_content):
                print(f"Skipping file {file_name}: does not contain [rewrite_local] or [MITM]/[mitm] sections.")
                continue
            
            loon_plugin_content = convert_js_to_loon(js_content)
            # Define the output file path in the 'loon' folder
            output_file_name = f"{os.path.splitext(file_name)[0]}.plugin"
            output_file_path = os.path.join(loon_path, output_file_name)
            with open(output_file_path, 'w') as file:
                file.write(loon_plugin_content)
            print(f"Converted {file_name} to {output_file_name}")
