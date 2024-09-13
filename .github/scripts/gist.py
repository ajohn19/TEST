import os
import requests
import json
import random
import re

GITHUB_USERNAME = "ajohn19"
ICON_REPO_NAME = "TEST"
ICON_REPO_BRANCH = "main"
RAW_REPO_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{ICON_REPO_NAME}/{ICON_REPO_BRANCH}/icons/"

def generate_random_cron():
    minute = random.randint(0, 59)
    hour = random.randint(0, 23)
    return f"{minute} {hour} * * *"

def extract_cron_from_content(content):
    cron_pattern = r'\b(\d{1,2}\s+\d{1,2}\s+\*\s+\*\s+\*)\b'
    match = re.search(cron_pattern, content)
    return match.group(1) if match else None

def generate_task_json():
    github_token = os.getenv("GISTID")
    headers = {"Authorization": f"token {github_token}"}
    api_url = f"https://api.github.com/users/{GITHUB_USERNAME}/gists"
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        gists = response.json()
        result = {
            "name": "测试任务合集订阅",
            "description": "如有侵权请联系@bot删除。tg机器人：https://t.me",
            "task": []
        }
        
        for gist in gists:
            for file_name, file_info in gist['files'].items():
                if file_name.endswith('.js'):
                    content_response = requests.get(file_info['raw_url'])
                    if content_response.status_code == 200:
                        content = content_response.text
                        cron = extract_cron_from_content(content) or generate_random_cron()
                    else:
                        cron = generate_random_cron()
                    
                    base_name = os.path.splitext(file_name)[0]
                    icon_url = f"{RAW_REPO_BASE_URL}{base_name}.png"
                    
                    # 检查图标是否存在
                    icon_response = requests.head(icon_url)
                    img_url_param = f", img-url={icon_url}" if icon_response.status_code == 200 else ""
                    
                    task_entry = {
                        "config": f"{cron} {file_info['raw_url']}, tag={base_name}{img_url_param}, enabled=false",
                        "addons": f"{file_info['raw_url']}, tag={base_name}获取Token"
                    }
                    
                    result["task"].append(task_entry)
        
        output_file_path = "testtask.gallery.json"
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(result, output_file, indent=4, ensure_ascii=False)
        print(f"Updated collection saved to {output_file_path}")
    else:
        print(f"Failed to retrieve Gist list. Status code: {response.status_code}")

if __name__ == "__main__":
    generate_task_json()
