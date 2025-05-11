import urllib.request
import json
import re
import subprocess
import sys

def get_ladder_zip_download_url(owner, repo):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "Python-Release-Checker"}
    req = urllib.request.Request(api_url, headers=headers)
    with urllib.request.urlopen(req) as response:
        releases = json.load(response)
        if releases:
            assets = releases[0].get('assets', [])
            for asset in assets:
                if asset.get('name') == 'ladder.zip':
                    return asset.get('browser_download_url')
    return None

def update_dockerfile_ladder_url(dockerfile_path, new_url):
    if not new_url: return False
    with open(dockerfile_path, 'r') as file:
        lines = file.readlines()
    updated_lines = []
    line_updated = False
    for line in lines:
        match = re.match(r"^(ARG\s+LADDER_PLUGIN_URL=)(.*)$", line)
        if match:
            if match.group(2).strip() == new_url: return True # Already up to date
            updated_lines.append(f"{match.group(1)}{new_url}\n")
            line_updated = True
        else:
            updated_lines.append(line)
    if line_updated:
        with open(dockerfile_path, 'w') as file:
            file.writelines(updated_lines)
        return True
    return False

def run_git_command(command_list):
    subprocess.run(command_list, check=True)
    return True

if __name__ == "__main__":
    commit_message = sys.argv[1]
    owner = "mgetf"
    repo = "MGEmod_tournament"
    dockerfile_path = "packages/tf2-ladder/Dockerfile"

    new_ladder_url = get_ladder_zip_download_url(owner, repo)
    if new_ladder_url:
        if update_dockerfile_ladder_url(dockerfile_path, new_ladder_url):
            subprocess.run(['git', 'add', dockerfile_path], check=True)
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            subprocess.run(['git', 'push'], check=True)
