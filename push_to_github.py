import os
import subprocess

# Replace these with your actual values
GITHUB_USERNAME = "mardoc2037"
REPO_NAME = "SENTINEL_PRIME"
ACCESS_TOKEN = "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" #Replace with your actual token
COMMIT_MESSAGE = "Initial commit from push_to_github.py"

# Set up remote URL with token
remote_url = f"https://{GITHUB_USERNAME}:{ACCESS_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)

def main():
    # Initialize git repo if not already
    if not os.path.exists(".git"):
        run_command("git init")

    # Add all files
    run_command("git add .")

    # Commit changes
    run_command(f'git commit -m "{COMMIT_MESSAGE}"')

    # Set branch to main
    run_command("git branch -M main")

    # Set remote URL (skip if already exists)
    run_command(f"git remote set-url origin {remote_url}")

    # Push to GitHub
    run_command("git push -u origin main")

if __name__ == "__main__":
    main()
