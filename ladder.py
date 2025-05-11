#!/usr/bin/env python3
import urllib.request
import json
import subprocess
import sys
import os

OWNER = "mgetf"
PACKAGE_NAME = "tf2-ladder/i386" # This is the name on ghcr.io, like mgetf/PACKAGE_NAME
PACKAGE_TYPE = "container"

def get_latest_package_tag():
    """
    Fetches the latest tag/digest for the specified GitHub container package.
    Requires a GITHUB_TOKEN environment variable with read:packages scope.
    """
    # The package name in the API URL needs to be URL-encoded if it contains slashes
    encoded_package_name = PACKAGE_NAME.replace("/", "%2F")
    api_url = f"https://api.github.com/users/{OWNER}/packages/{PACKAGE_TYPE}/{encoded_package_name}/versions"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python-Package-Puller"
    }

    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"
        print("Using GITHUB_TOKEN for authentication.")
    else:
        print("Warning: GITHUB_TOKEN environment variable not set. API request may fail.", file=sys.stderr)
        # Depending on the package visibility and GitHub's mood, this might still work for some public ones, but often fails.

    req = urllib.request.Request(api_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                versions = json.load(response)
                if versions:
                    # Assuming the first version in the list is the most recent
                    latest_version_name = versions[0].get("name")
                    if latest_version_name:
                        print(f"Found latest version tag: {latest_version_name}")
                        return latest_version_name
                    else:
                        print("Error: Could not find name for the latest version.", file=sys.stderr)
                        return None
                else:
                    print(f"No versions found for package {OWNER}/{PACKAGE_NAME}.", file=sys.stderr)
                    return None
            else:
                print(f"Error fetching package versions: HTTP {response.status} {response.reason}", file=sys.stderr)
                error_details = response.read().decode(errors='ignore')
                print(f"Details: {error_details}", file=sys.stderr)
                return None
    except urllib.error.HTTPError as e:
        print(f"HTTP Error fetching package versions: {e.code} {e.reason}", file=sys.stderr)
        try:
            error_body = e.read().decode(errors='ignore')
            print(f"Response body: {error_body}", file=sys.stderr)
        except Exception:
            pass
        return None
    except urllib.error.URLError as e:
        print(f"URL Error fetching package versions: {e.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response from GitHub API.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return None

def pull_docker_image(tag):
    """
    Pulls the Docker image for the given tag.
    """
    if not tag:
        return False
        
    image_name = f"ghcr.io/{OWNER}/{PACKAGE_NAME}:{tag}"
    print(f"Attempting to pull Docker image: {image_name}")
    
    try:
        # Using check=True to raise CalledProcessError on non-zero exit codes
        process = subprocess.run(["docker", "pull", image_name], check=True, text=True, capture_output=True)
        print(f"Successfully pulled {image_name}")
        if process.stdout:
            print("Docker stdout:\n", process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error pulling Docker image {image_name}.", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(f"Stdout:\n{e.stdout}", file=sys.stderr)
        if e.stderr:
            print(f"Stderr:\n{e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: Docker command not found. Ensure Docker is installed and in your PATH.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An unexpected error occurred while pulling the image: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    print(f"Fetching latest package information for {OWNER}/{PACKAGE_NAME}...")
    latest_tag = get_latest_package_tag()
    
    if latest_tag:
        if not pull_docker_image(latest_tag):
            sys.exit(1) # Exit with error if pull failed
    else:
        print("Could not determine the latest package tag. Docker pull skipped.", file=sys.stderr)
        sys.exit(1) # Exit with error if tag couldn't be fetched

    print("Script finished.")

