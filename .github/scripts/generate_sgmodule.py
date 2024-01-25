import os
import re

def insert_append(content):
    # Insert %APPEND% after the first '=' sign
    return re.sub(r'=', '= %APPEND%', content, count=1)

def extract_name_desc(js_content):
    # Extract patterns and scripts from rewrite_local_content
    patterns_and_scripts = re.findall(r'^(.*?)\s*(?:url\s+script-(response-body|request-body|echo-response|request-header|response-header|analyze-echo-response)\s+(\S+.*?)$)', js_content, re.MULTILINE)
    
    if not patterns_and_scripts:
        raise ValueError("No [rewrite_local] rule found")

    last_pattern, script_type, script = patterns_and_scripts[-1]
    return os.path.splitext(os.path.basename(script))[0]

def js_to_sgmodule(js_content):
    # Extract information from the JS content
    name = extract_name_desc(js_content)
    desc = name  # Using the same value for desc for now, you can modify this as needed

    rewrite_match = re.search(r'\[rewrite_local\]\s*(.*?)\s*\[mitm\]\s*hostname\s*=\s*(.*?)\s*', js_content, re.DOTALL | re.MULTILINE)
    mitm_match = re.search(r'\[mitm\]\s*([^=\n]+=[^\n]+)\s*', js_content, re.DOTALL | re.MULTILINE)
    hostname_match = re.search(r'hostname\s*=\s*([^=\n]+=[^\n]+)\s*', js_content, re.DOTALL | re.MULTILINE)

    if not (rewrite_match and mitm_match):
        raise ValueError("Invalid JS file format")

    project_name = name.strip()
    project_desc = desc.strip()

    rewrite_local_content = rewrite_match.group(1).strip()
    mitm_content = mitm_match.group(1).strip() if mitm_match else ''
    hostname_content = hostname_match.group(1).strip() if hostname_match else ''

    # Insert %APPEND% into mitm and hostname content
    mitm_content_with_append = insert_append(mitm_content)

    # Extract patterns and scripts from rewrite_local_content
    patterns_and_scripts = re.findall(r'^(.*?)\s*(?:url\s+script-(response-body|request-body|echo-response|request-header|response-header|analyze-echo-response)\s+(\S+.*?)$)', rewrite_local_content, re.MULTILINE)
    if not patterns_and_scripts:
        raise ValueError("Invalid rewrite_local format")

    # Generate sgmodule content
    sgmodule_content = f"""#!name={project_name}
#!desc={project_desc}

[MITM]
{mitm_content_with_append}

[Script]
"""

    for pattern, script_type, script in patterns_and_scripts:
        # Remove the '-body' or '-header' suffix from the script type
        script_type = script_type.replace('-body', '').replace('-header', '')
        sgmodule_content += f"{project_name} = type=http-{script_type},pattern={pattern},requires-body=1,max-size=0,script-path={script}\n"

    return sgmodule_content

def main():
    # Process each file in the 'qx' folder
    qx_folder_path = 'qx'
    if not os.path.exists(qx_folder_path):
        print(f"Error: {qx_folder_path} does not exist.")
        return

    for file_name in os.listdir(qx_folder_path):
        if file_name.endswith(".js"):
            file_path = os.path.join(qx_folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as js_file:
                js_content = js_file.read()
                try:
                    sgmodule_content = js_to_sgmodule(js_content)
                    # Write sgmodule content to surge folder
                    surge_folder_path = 'surge'
                    os.makedirs(surge_folder_path, exist_ok=True)
                    sgmodule_file_path = os.path.join(surge_folder_path, f"{os.path.splitext(file_name)[0]}.sgmodule")
                    with open(sgmodule_file_path, "w", encoding="utf-8") as sgmodule_file:
                        sgmodule_file.write(sgmodule_content)

                    print(f"Generated {sgmodule_file_path}")

                    # Add a dummy change and commit
                    with open(file_path, 'a', encoding='utf-8') as js_file:
                        js_file.write("\n// Adding a dummy change to trigger git commit\n")

                    os.system(f'git add {file_path}')
                    os.system('git commit -m "Trigger update"')

                except ValueError as e:
                    print(f"Error processing {file_name}: {e}")

if __name__ == "__main__":
    main()
