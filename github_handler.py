from github import Github
import os
import base64

class GitHubHandler:
    def __init__(self):
        self.github = None
        self.user = None

    def set_token(self, token):
        self.github = Github(token)
        self.user = self.github.get_user()

    def create_repository(self, name, description=""):
        self.user.create_repo(name, description=description)

    def upload_files(self, local_path, repo_name):
        repo = self.user.get_repo(repo_name)
        
        for root, dirs, files in os.walk(local_path):
            for file in files:
                # Skip .git folder and its contents
                if '.git' in root:
                    continue
                    
                file_path = os.path.join(root, file)
                
                # Calculate relative path for GitHub
                relative_path = os.path.relpath(file_path, local_path)
                
                # Read file content
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                try:
                    # Try to create the file in the repository
                    repo.create_file(
                        path=relative_path,
                        message=f"Add {relative_path}",
                        content=content
                    )
                except Exception as e:
                    print(f"Error uploading {relative_path}: {str(e)}") 