import os
from pathlib import Path
import subprocess
import sys
import re


def get_repo_url() -> str:
    repository = os.getenv("GITHUB_REPOSITORY", "")
    if not repository:
        print("Error: GITHUB_REPOSITORY environment variable not set.")
        sys.exit(1)
    return f"https://github.com/{repository}"


def get_last_tag() -> str:
    try:
        result = subprocess.run(
            ["git", "tag", "--sort=creatordate"],
            capture_output=True,
            text=True,
            check=True,
        )
        tags = result.stdout.strip().splitlines()

        if len(tags) > 1:
            return tags[-2]
        else:
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error retrieving last tag: {e}")
        sys.exit(1)


def extract_changelog(tag: str) -> None:
    vtag = f"v{tag}"

    changelog_path = Path(os.getcwd(), "CHANGELOG.md")
    release_path = Path(os.getcwd(), "RELEASE_NOTES.md")

    repo_url = get_repo_url()
    last_tag = get_last_tag()

    if last_tag is None:
        commits_url = f"{repo_url}/commits/{vtag}"  # First tag
    else:
        commits_url = f"{repo_url}/compare/{last_tag}...{vtag}"

    with open(changelog_path, "r", encoding="utf8") as file:
        content = file.read()

    pattern = rf"## \[{tag}\](.*?)(## \[|$)"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print(f"No changelog entry found for tag: {vtag}")
        sys.exit(1)

    version_content = "\n".join(match.group(1).strip().split("\n")[1:])
    footer = (
        f"\n\nFor a full list of version changes, visit the [changelog]({repo_url}/blob/main/CHANGELOG.md)."
        f"\nFor commit history for this release, see [commits]({commits_url})."
    )
    changelog_entry = f"{version_content}{footer}\n"

    with open(release_path, "w", encoding="utf8") as file:
        file.write(changelog_entry)
    print(f"Changelog entry for tag {vtag} extracted successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ci/changelog.py <tag>")
        sys.exit(1)

    tag = sys.argv[1].lstrip("v")
    extract_changelog(tag)
