import os
import re

def contains_required_sections(js_content):
    # Check for the existence of [rewrite_local] or [MITM]/[mitm] sections
    return re.search(r'\[rewrite_local\]', js_content, re.IGNORECASE) or re.search(r'\[MITM\]', js_content, re.IGNORECASE)

def extract_header_info(js_content):
    # Attempt to extract the header information or fallback to URL filenames
    name_match = re.search(r'项目名称：(.*?)\n', js_content)
    desc_match = re.search(r'使用说明：(.*?)\n', js_content)

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
        else:
            project_name = project_desc = "DefaultProjectName"

    img_url_match = re.search(r'img-url=(https?://[^\s,"]+)', js_content)
    img_url = img_url_match.group(1).strip() if img_url_match else ""

    return project_name, project_desc, img_url

def extract_rules(js_content):
    # Extract MITM and Rewrites
    mitm_match = re.search(r'\[MITM\]\nhostname\s*=\s*(.*)', js_content)
    mitm = f"[MITM]\nhostname = {mitm_match.group(1).strip()}\n" if mitm_match else ""

    rewrite_rules = re.findall(
        r'(?:^|\n)\s*([^#\n].*?)\s+url\s+script-(response|request)-(body|header)\s+(https?://\S+)\s*,\s*tag\s*=\s*(\S+)',
        js_content, re.MULTILINE
    )
    scripts = "[Script]\n"
    for rule in rewrite_rules:
        pattern, type, section, script_path, tag = rule
        scripts += f"http-{type} {section} {pattern} script-path={script_path}, tag={tag}\n"

    return mitm + scripts

def convert_js_to_loon(js_content):
    # Convert JS content to Loon Plugin format
    project_name, project_desc, img_url = extract_header_info(js_content)
    rules = extract_rules(js_content)
    
    loon_plugin_content = f"#!name={project_name}\n#!desc={project_desc}\n"
    if img_url:
        loon_plugin_content += f"#!icon={img_url}\n"
    loon_plugin_content += rules
    
    return loon_plugin_content

# Repository structure and file conversion
base_path = os.getcwd()
qx_path = os.path.join(base_path, 'qx')
loon_path = os.path.join(base_path, 'loon')

# Create 'loon' directory if it doesn't exist
if not os.path.exists(loon_path):
    os.makedirs(loon_path)

# Loop through all files in 'qx' directory
for root, dirs, files in os.walk(qx_path):
    for file_name in files:
        if file_name.lower().endswith(('.js', '.conf', '.snippet')):
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                js_content = file.read()

            if not contains_required_sections(js_content):
                print(f"Skipping file: {file_name} - Required sections not found.")
                continue

            loon_plugin_content = convert_js_to_loon(js_content)
            output_file_name = f"{os.path.splitext(file_name)[0]}.plugin"
            output_file_path = os.path.join(loon_path, output_file_name)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(loon_plugin_content)
            print(f"Converted: {file_name} -> {output_file_name}")
