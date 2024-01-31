import os
import re

def extract_header_info(js_content):
    # Attempt to extract the header information or fallback to URL filenames
    name_match = re.search(r'项目名称：(.*?)\n', js_content)
    desc_match = re.search(r'使用说明：(.*?)\n', js_content)

    if name_match and desc_match:
        project_name = name_match.group(1).strip()
        project_desc = desc_match.group(1).strip()
    else:
        rewrite_url_match = re.search(
            r'url\s+script-(?:response|request)-(?:body|header)\s+(https?://[^\s]+)',
            js_content
        )
        if rewrite_url_match:
            last_url_segment = os.path.splitext(os.path.basename(rewrite_url_match.group(1)))[0]
            project_name = project_desc = last_url_segment
        else:
            project_name = project_desc = "DefaultProjectName"

    img_url_match = re.search(r'\[task_local\]\nimg-url\s*=\s*(https?://[^\s]+)', js_content)
    img_url = img_url_match.group(1).strip() if img_url_match else ""

    return project_name, project_desc, img_url

def extract_mitm_info(js_content):
    # Extract MITM information from [MITM]/[mitm] section
    mitm_match = re.search(r'\[MITM\]\s*hostname\s*=\s*(.*)', js_content, re.IGNORECASE)
    if not mitm_match:
        mitm_match = re.search(r'\[mitm\]\s*hostname\s*=\s*(.*)', js_content, re.IGNORECASE)

    hostname = mitm_match.group(1).strip() if mitm_match else ''
    return hostname

def convert_js_to_loon(js_content):
    # Convert JS content to Loon Plugin format
    project_name, project_desc, img_url = extract_header_info(js_content)
    mitm_hostname = extract_mitm_info(js_content)
    
    loon_plugin_content = f"#!name={project_name}\n#!desc={project_desc}\n"
    
    if img_url:
        loon_plugin_content += f"#!icon={img_url}\n"

    if mitm_hostname:
        loon_plugin_content += f"[MITM]\nhostname = {mitm_hostname}\n"
    
    # Extract rules and append to loon_plugin_content
    rules = extract_rules(js_content)
    loon_plugin_content += rules
    
    return loon_plugin_content

def extract_rules(js_content):
    # Extract Rewrite rules from [rewrite_local] section
    rewrite_local_pattern = re.compile(r'^\[rewrite_local\]([\s\S]*?)(?:\[|$)', re.MULTILINE)
    rewrite_local_match = rewrite_local_pattern.search(js_content)

    if not rewrite_local_match:
        return ''

    rewrite_local_content = rewrite_local_match.group(1).strip()
    url_script_matches = re.finditer(
        r'^([^#\n].*?)\s+url\s+(script-response-body|script-request-body|script-response-header|script-request-header|script-echo-response|script-analyze-echo-response)\s+(https?://[^\s]+)\s*,\s*tag\s*=\s*(\S+)',
        rewrite_local_content, re.MULTILINE
    )

    scripts = "[Script]\n"
    for match in url_script_matches:
        pattern, type, script_path, tag = match.groups()
        type = type.replace('script-', 'http-')
        last_url_segment = os.path.splitext(os.path.basename(script_path))[0]
        scripts += f"{type} {pattern} script-path={script_path}, tag={tag}, enabled=true\n"

    return scripts

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
            with open(file_path, 'r') as file:
                js_content = file.read()

            loon_plugin_content = convert_js_to_loon(js_content)
            output_file_name = f"{os.path.splitext(file_name)[0]}.plugin"
            output_file_path = os.path.join(loon_path, output_file_name)
            with open(output_file_path, 'w') as file:
                file.write(loon_plugin_content)
            print(f"Converted: {file_name} -> {output_file_name}")
