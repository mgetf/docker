import urllib.request
import json
import re # Added for regex-based line replacement
import os # Added to construct the Dockerfile path
import subprocess # Added for running Git commands
import sys # Added for accessing command-line arguments

def get_most_recent_release_info(owner, repo):
    """
    Fetches and prints information about the most recent release for a given GitHub repository.
    This includes pre-releases if they are the most recent chronologically.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {
        "Accept": "application/vnd.github.v3+json",  # Recommended by GitHub API docs
        "User-Agent": "Python-Release-Checker"      # Good practice to set a User-Agent
    }

    req = urllib.request.Request(api_url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                releases = json.load(response)
                if releases:
                    # The first release in the list is the most recent chronologically
                    latest_release = releases[0]
                    
                    print(f"Most Recent Release Information for {owner}/{repo}:")
                    print(f"  Tag Name: {latest_release.get('tag_name')}")
                    print(f"  Release Name: {latest_release.get('name')}")
                    print(f"  Published At: {latest_release.get('published_at')}")
                    print(f"  URL: {latest_release.get('html_url')}")
                    print(f"  Pre-release: {latest_release.get('prerelease')}")
                    
                    assets = latest_release.get('assets', [])
                    if assets:
                        print("  Assets:")
                        for asset in assets:
                            print(f"    - {asset.get('name')} ({asset.get('size')} bytes)")
                            print(f"      Download URL: {asset.get('browser_download_url')}")
                    else:
                        print("  No assets found for this release.")
                else:
                    print(f"No releases found for {owner}/{repo}.")
            else:
                print(f"Error fetching releases: HTTP {response.status}")
                # Try to print more details from the error response if possible
                try:
                    error_details = json.load(response)
                    print(f"  Error details: {error_details.get('message')}")
                except json.JSONDecodeError:
                    print(f"  Response body: {response.read().decode(errors='ignore')}")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching releases: {e.code} {e.reason}")
        try:
            # Try to print more details from the error response if possible
            error_body = e.read().decode(errors='ignore')
            print(f"  Response body: {error_body}")
        except Exception:
            pass # Ignore if reading the body fails
    except urllib.error.URLError as e:
        print(f"URL Error fetching releases: {e.reason}")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from GitHub API.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_ladder_zip_download_url(owner, repo):
    """
    Fetches the browser_download_url for 'ladder.zip' from the most recent release.
    Returns the URL as a string, or None if not found or an error occurs.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python-Release-Checker"
    }
    req = urllib.request.Request(api_url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                releases = json.load(response)
                if releases:
                    latest_release = releases[0] # Most recent is first
                    assets = latest_release.get('assets', [])
                    for asset in assets:
                        if asset.get('name') == 'ladder.zip':
                            return asset.get('browser_download_url')
                    print(f"Info: 'ladder.zip' asset not found in the latest release of {owner}/{repo}.")
                    return None
                else:
                    print(f"No releases found for {owner}/{repo}.")
                    return None
            else:
                print(f"Error fetching releases: HTTP {response.status}")
                return None
    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching releases: {e.code} {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"URL Error fetching releases: {e.reason}")
        return None
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from GitHub API.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching release info: {e}")
        return None

def update_dockerfile_ladder_url(dockerfile_path, new_url):
    """
    Updates the ARG LADDER_PLUGIN_URL in the specified Dockerfile.
    Returns True if the file was updated or already up-to-date, False otherwise.
    """
    if not new_url:
        print("No new URL provided, Dockerfile update skipped.")
        return False

    try:
        with open(dockerfile_path, 'r') as file:
            lines = file.readlines()

        updated_lines = []
        line_updated = False
        found_target_line = False
        for line in lines:
            match = re.match(r"^(ARG\s+LADDER_PLUGIN_URL=)(.*)$", line)
            if match:
                found_target_line = True
                old_url = match.group(2).strip() # Strip potential newline
                if old_url == new_url:
                    print(f"Dockerfile already contains the latest URL: {new_url}")
                    return True # No update needed, but considered success
                updated_lines.append(f"{match.group(1)}{new_url}\n")
                line_updated = True
            else:
                updated_lines.append(line)

        if not found_target_line:
            print(f"Warning: 'ARG LADDER_PLUGIN_URL=' line not found in '{dockerfile_path}'. No update made.")
            return False

        if line_updated:
            with open(dockerfile_path, 'w') as file:
                file.writelines(updated_lines)
            print(f"Dockerfile '{dockerfile_path}' updated successfully with URL: {new_url}")
            return True
        else:
            # This case should ideally be caught by "already contains the latest URL"
            # or "line not found", but as a fallback.
            return False


    except FileNotFoundError:
        print(f"Error: Dockerfile not found at '{dockerfile_path}'")
        return False
    except Exception as e:
        print(f"An error occurred while updating Dockerfile '{dockerfile_path}': {e}")
        return False

def run_git_command(command_list):
    """Runs a Git command and prints its output/error."""
    try:
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print(f"Successfully executed: {' '.join(command_list)}")
            if stdout: print(f"Stdout:\n{stdout}")
            return True
        else:
            print(f"Error executing: {' '.join(command_list)}")
            if stdout: print(f"Stdout:\n{stdout}")
            if stderr: print(f"Stderr:\n{stderr}")
            return False
    except FileNotFoundError:
        print(f"Error: Git command not found. Ensure Git is installed and in your PATH.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while running git command: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update.py \"<commit message>\"")
        sys.exit(1)
    
    commit_message = sys.argv[1]

    owner = "mgetf"
    repo = "MGEmod_tournament"
    
    dockerfile_path = "packages/tf2-ladder/Dockerfile" # Assuming script is run from workspace root

    print(f"Fetching latest ladder.zip URL for {owner}/{repo}...")
    new_ladder_url = get_ladder_zip_download_url(owner, repo)

    if new_ladder_url:
        print(f"Found latest URL: {new_ladder_url}")
        print(f"Attempting to update Dockerfile: {dockerfile_path}")
        dockerfile_updated_successfully = update_dockerfile_ladder_url(dockerfile_path, new_ladder_url)
        
        if dockerfile_updated_successfully:
            print("\nAttempting to commit and push changes...")
            # Check if there are changes to commit before attempting
            status_check_process = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            if not status_check_process.stdout.strip():
                print("No changes to commit. Dockerfile was likely already up-to-date.")
            else:
                if run_git_command(['git', 'add', '.']):
                    if run_git_command(['git', 'commit', '-am', commit_message]):
                        if run_git_command(['git', 'push']):
                            print("Successfully committed and pushed changes.")
                        else:
                            print("Failed to push changes.")
                    else:
                        print("Failed to commit changes.")
                else:
                    print("Failed to add changes to Git.")
        else:
            print("Dockerfile not updated. Git commit and push will be skipped.")
            
    else:
        print("Could not retrieve the new ladder.zip URL. Dockerfile not updated. Git operations skipped.")
