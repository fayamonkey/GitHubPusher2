import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui.main_window import MainWindow
from github_handler import GitHubHandler

class GitHubUploaderApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.github_handler = GitHubHandler()
        self.main_window = MainWindow(self.github_handler)
        
    def run(self):
        self.main_window.show()
        return self.app.exec()

if __name__ == "__main__":
    app = GitHubUploaderApp()
    sys.exit(app.run()) 