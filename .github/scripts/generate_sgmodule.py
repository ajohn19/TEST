import os
import re

def insert_append(content):
    return re.sub(r'=', '= %APPEND%', content, count=1)

def js_to_sgmodule(js_content):
    name_match = re.search(r'项目名称：(.*?)\n', js_content)
    desc_match = re.search(r'使用说明：(.*?)\n', js_content)
    hostname_match = re.search(r'\[mitm\]\s*([^=\n]+=[^\n]+)\s*', js_content, re.DOTALL | re.MULTILINE)

    if not (name_match and desc_match):
        url_pattern = r'url\s+script-(?:response-body|request-body|echo-response|request-header|response-header|analyze-echo-response)\s+(\S+.*?)$'
        last_part_match = re.search(url_pattern, js_content, re.MULTILINE)
        if last_part_match:
            project_name = os.path.splitext(os.path.basename(last_part_match.group(1).strip()))[0]
        else:
            raise ValueError("Invalid JS file format")

        project_desc = f"Generated from {project_name}"

    else:
        project_name = name_match.group(1).strip()
        project_desc = desc_match.group(1).strip()

    hostname_content = hostname_match.group(1).strip() if hostname_match else ''

    hostname_content_with_append = insert_append(hostname_content)

    sgmodule_content = f"""#!name={project_name}
#!desc={project_desc}
[MITM]
{hostname_content_with_append}
"""

    rewrite_local_pattern = re.compile(r'\[rewrite_local\]\s*(.*?)\s*\[mitm\]\s*hostname\s*=\s*(.*?)\s*', re.DOTALL | re.MULTILINE)
    rewrite_local_match = rewrite_local_pattern.search(js_content)

    if rewrite_local_match:
        rewrite_local_content = rewrite_local_match.group(1).strip()

        pattern_script_matches = re.finditer(r'\burl\s+script-(response-body|request-body|echo-response|request-header|response-header|analyze-echo-response)\s+(\S+.*?)$', rewrite_local_content, re.MULTILINE)

        if not pattern_script_matches:
            print("Warning: No valid rewrite_local rules found")

        sgmodule_content += "[Script]\n"
        for pattern_script_match in pattern_script_matches:
            pattern_script = pattern_script_match.group(2).strip()
            script_type = pattern_script_match.group(1).strip()
            script_type = script_type.replace('-body', '').replace('-header', '')
            sgmodule_content += f"{project_name} = type=http-{script_type},pattern={pattern_script},requires-body=1,max-size=0,script-path={pattern_script}\n"

    else:
        print("Warning: No [rewrite_local] rule found")

    return sgmodule_content

def main():
    qx_folder_path = 'qx'
    if not os.path.exists(qx_folder_path):
        print(f"Error: {qx_folder_path} does not exist.")
        return

    for file_name in os.listdir(qx_folder_path):
        if file_name.endswith(".js"):
            file_path = os.path.join(qx_folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as js_file:
                js_content = js_file.read()
                sgmodule_content = js_to_sgmodule(js_content)

                surge_folder_path = 'surge'
                os.makedirs(surge_folder_path, exist_ok=True)
                sgmodule_file_path = os.path.join(surge_folder_path, f"{os.path.splitext(file_name)[0]}.sgmodule")
                with open(sgmodule_file_path, "w", encoding="utf-8") as sgmodule_file:
                    sgmodule_file.write(sgmodule_content)

                print(f"Generated {sgmodule_file_path}")

                with open(file_path, 'a', encoding='utf-8') as js_file:
                    js_file.write("\n// Adding a dummy change to trigger git commit\n")

                os.system(f'git add {file_path}')
                os.system('git commit -m "Trigger update"')

if __name__ == "__main__":
    main()
