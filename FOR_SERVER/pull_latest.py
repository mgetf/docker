#!/usr/bin/env python3
import urllib.request
import json
import sys
import os

OWNER = "mgetf"
PACKAGE_NAME = "tf2-ladder/i386"
PACKAGE_TYPE = "container"

def get_latest_package_tag():
    """
    Fetches the latest tag for the specified GitHub container package.
    Requires a GITHUB_TOKEN environment variable with read:packages scope.
    Outputs the tag to stdout if successful, otherwise prints errors to stderr.
    """
    encoded_package_name = PACKAGE_NAME.replace("/", "%2F")
    api_url = f"https://api.github.com/users/{OWNER}/packages/{PACKAGE_TYPE}/{encoded_package_name}/versions"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python-Package-Tag-Fetcher"
    }

    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    else:
        print("Warning: GITHUB_TOKEN environment variable not set. API request may fail.", file=sys.stderr)

    req = urllib.request.Request(api_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                versions = json.load(response)
                if versions:
                    latest_version_obj = versions[0]
                    image_tags = []
                    package_metadata = latest_version_obj.get("metadata")
                    if package_metadata and package_metadata.get("package_type") == "container":
                        container_metadata = package_metadata.get("container")
                        if container_metadata:
                            image_tags = container_metadata.get("tags", [])

                    if image_tags:
                        actual_tag = image_tags[0]
                        return actual_tag
                    else:
                        name_field_as_tag = latest_version_obj.get("name")
                        if name_field_as_tag:
                            print(f"Warning: No tags found in metadata.container.tags. Using 'name' field as tag: {name_field_as_tag}", file=sys.stderr)
                            return name_field_as_tag
                        else:
                            print("Error: Could not find a usable tag in metadata or name field.", file=sys.stderr)
                            return None
                else:
                    print(f"Error: No versions found for package {OWNER}/{PACKAGE_NAME}.", file=sys.stderr)
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

if __name__ == "__main__":
    latest_tag = get_latest_package_tag()
    
    if latest_tag:
        print(latest_tag)
        sys.exit(0)
    else:
        sys.exit(1)
