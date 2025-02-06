from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class MainWindow(QMainWindow):
    def __init__(self, github_handler):
        super().__init__()
        self.github_handler = github_handler
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('GitHub Project Uploader')
        self.setMinimumSize(600, 400)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # GitHub Token Section
        token_layout = QHBoxLayout()
        token_label = QLabel('GitHub Token:')
        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.EchoMode.Password)
        token_layout.addWidget(token_label)
        token_layout.addWidget(self.token_input)
        layout.addLayout(token_layout)

        # Project Path Section
        path_layout = QHBoxLayout()
        path_label = QLabel('Project Path:')
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        browse_btn = QPushButton('Browse')
        browse_btn.clicked.connect(self.browse_folder)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)

        # Repository Name Section
        repo_layout = QHBoxLayout()
        repo_label = QLabel('Repository Name:')
        self.repo_input = QLineEdit()
        repo_layout.addWidget(repo_label)
        repo_layout.addWidget(self.repo_input)
        layout.addLayout(repo_layout)

        # Description Section
        desc_layout = QHBoxLayout()
        desc_label = QLabel('Description:')
        self.desc_input = QLineEdit()
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        layout.addLayout(desc_layout)

        # Upload Button
        self.upload_btn = QPushButton('Upload to GitHub')
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.upload_btn.clicked.connect(self.upload_project)
        layout.addWidget(self.upload_btn)

        # Add stretching space
        layout.addStretch()

        # Style the window
        self.style_ui()

    def style_ui(self):
        # Set fonts
        default_font = QFont('Arial', 10)
        self.setFont(default_font)

        # Style labels
        for widget in self.findChildren(QLabel):
            widget.setMinimumWidth(100)

        # Style line edits
        for widget in self.findChildren(QLineEdit):
            widget.setMinimumHeight(30)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder_path:
            self.path_input.setText(folder_path)

    def upload_project(self):
        token = self.token_input.text()
        path = self.path_input.text()
        repo_name = self.repo_input.text()
        description = self.desc_input.text()

        if not all([token, path, repo_name]):
            QMessageBox.warning(self, "Error", "Please fill in all required fields!")
            return

        try:
            self.upload_btn.setEnabled(False)
            self.upload_btn.setText("Uploading...")
            
            self.github_handler.set_token(token)
            self.github_handler.create_repository(repo_name, description)
            self.github_handler.upload_files(path, repo_name)

            QMessageBox.information(self, "Success", 
                                 f"Project successfully uploaded to GitHub!\n"
                                 f"Repository: {repo_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        finally:
            self.upload_btn.setEnabled(True)
            self.upload_btn.setText("Upload to GitHub") 