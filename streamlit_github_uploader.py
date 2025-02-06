import streamlit as st
import os
import tempfile
import zipfile
import shutil
from github import Github
from pathlib import Path

class GitHubUploader:
    def __init__(self):
        self.github = None
        self.user = None
        
    def set_token(self, token):
        self.github = Github(token)
        self.user = self.github.get_user()
        
    def create_repository(self, name, description=""):
        return self.user.create_repo(name, description=description)
        
    def upload_files(self, local_path, repo_name):
        repo = self.user.get_repo(repo_name)
        uploaded_files = []
        errors = []
        
        for root, dirs, files in os.walk(local_path):
            for file in files:
                if '.git' in root:
                    continue
                    
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, local_path)
                
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    
                    repo.create_file(
                        path=relative_path,
                        message=f"Add {relative_path}",
                        content=content
                    )
                    uploaded_files.append(relative_path)
                except Exception as e:
                    errors.append(f"Error uploading {relative_path}: {str(e)}")
                    
        return uploaded_files, errors

def unzip_to_temp(zip_file):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        return temp_dir
    except Exception as e:
        shutil.rmtree(temp_dir)
        raise e

def main():
    st.set_page_config(
        page_title="GitHub Project Uploader",
        page_icon="🚀",
        layout="centered"
    )
    
    st.title("🚀 GitHub Project Uploader")
    st.markdown("Upload your projects directly to GitHub repositories!")

    # Initialize session state
    if 'uploader' not in st.session_state:
        st.session_state.uploader = GitHubUploader()
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # GitHub Token Input
    with st.expander("🔑 GitHub Authentication", expanded=not st.session_state.authenticated):
        token = st.text_input("GitHub Token", type="password", 
                            help="Enter your GitHub Personal Access Token")
        if st.button("Authenticate"):
            try:
                st.session_state.uploader.set_token(token)
                st.session_state.authenticated = True
                st.success("Successfully authenticated with GitHub!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Authentication failed: {str(e)}")

    if st.session_state.authenticated:
        st.markdown("### 📂 Project Upload")
        
        # Upload method selection
        upload_method = st.radio(
            "Choose upload method:",
            ["Select Folder", "Upload ZIP File"],
            help="Choose how you want to upload your project"
        )

        # Repository details
        col1, col2 = st.columns(2)
        with col1:
            repo_name = st.text_input("Repository Name", 
                                    help="Name for the new GitHub repository")
        with col2:
            repo_desc = st.text_input("Repository Description (optional)", 
                                    help="Brief description of your repository")

        # Handle different upload methods
        if upload_method == "Select Folder":
            folder_path = st.text_input("Project Folder Path", 
                                      help="Full path to your project folder")
            
        else:  # ZIP File upload
            uploaded_file = st.file_uploader("Upload ZIP File", 
                                           type=['zip'],
                                           help="Upload a ZIP file containing your project")

        # Upload button
        if st.button("Upload to GitHub", type="primary"):
            if not repo_name:
                st.error("Please enter a repository name!")
                return

            try:
                with st.spinner("Creating repository..."):
                    st.session_state.uploader.create_repository(repo_name, repo_desc)

                with st.spinner("Uploading files..."):
                    if upload_method == "Select Folder":
                        if not folder_path or not os.path.exists(folder_path):
                            st.error("Please enter a valid folder path!")
                            return
                        project_path = folder_path
                    else:
                        if not uploaded_file:
                            st.error("Please upload a ZIP file!")
                            return
                        # Save and extract ZIP file
                        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
                        temp_zip.write(uploaded_file.getvalue())
                        temp_zip.close()
                        project_path = unzip_to_temp(temp_zip.name)

                    uploaded_files, errors = st.session_state.uploader.upload_files(
                        project_path, repo_name)

                    # Clean up temporary files if using ZIP
                    if upload_method == "Upload ZIP File":
                        os.unlink(temp_zip.name)
                        shutil.rmtree(project_path)

                # Show results
                st.success(f"Successfully created repository: {repo_name}")
                
                if uploaded_files:
                    with st.expander("📄 Uploaded Files"):
                        for file in uploaded_files:
                            st.text(f"✓ {file}")
                
                if errors:
                    with st.expander("⚠️ Errors"):
                        for error in errors:
                            st.error(error)

                # Show repository link
                repo_url = f"https://github.com/{st.session_state.uploader.user.login}/{repo_name}"
                st.markdown(f"### 🔗 [View Your Repository]({repo_url})")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

        # Help section
        with st.expander("ℹ️ Help"):
            st.markdown("""
            ### How to use this app:
            1. Enter your GitHub Personal Access Token
            2. Choose your upload method (folder or ZIP file)
            3. Enter repository details
            4. Click Upload to GitHub
            
            ### Getting a GitHub Token:
            1. Go to GitHub.com → Settings → Developer Settings
            2. Select Personal Access Tokens → Tokens (classic)
            3. Generate new token with 'repo' scope
            """)

if __name__ == "__main__":
    main() 