import os
import time
import threading

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit,
    QPushButton, QTextEdit, QWidget, QFileDialog, QMessageBox, QProgressBar
)


class WindowsSearch:
    @staticmethod
    def search_files(directory, keyword):
        results = []

        def deep_search(search_dir, depth=10):
            if depth <= 0:
                return []

            found_results = []
            try:
                for entry in os.scandir(search_dir):
                    try:
                        # Check for exact and partial matches
                        if (keyword.lower() in entry.name.lower() or 
                            entry.name.lower().startswith(keyword.lower())):
                            found_results.append(entry.path)

                        # Recursive search for directories
                        if entry.is_dir(follow_symlinks=False):
                            try:
                                sub_results = deep_search(entry.path, depth - 1)
                                found_results.extend(sub_results)
                            except (PermissionError, OSError):
                                pass
                    except Exception:
                        pass

            except (PermissionError, OSError):
                pass

            return found_results

        # Try multiple search methods
        try:
            # First, try deep search from the given directory
            results = deep_search(directory)

            # If no results, try searching from root of the drive
            if not results:
                drive_root = os.path.splitdrive(directory)[0] + '\\'
                results = deep_search(drive_root)

        except Exception as e:
            print(f"Search error: {e}")

        return results


class SearchThread(QThread):
    search_progress = pyqtSignal(int)
    search_complete = pyqtSignal(list)
    search_error = pyqtSignal(str)

    def __init__(self, directory, keyword):
        super().__init__()
        self.directory = directory
        self.keyword = keyword

    def run(self):
        try:
            # Comprehensive search method
            results = WindowsSearch.search_files(self.directory, self.keyword)

            # Remove duplicates while preserving order
            results = list(dict.fromkeys(results))

            self.search_complete.emit(results)
        except Exception as e:
            self.search_error.emit(str(e))


class FastSearch(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FTK Search by Ankit")
        self.setGeometry(300, 300, 800, 600)

        # Layout and widgets
        layout = QVBoxLayout()

        self.directory_input = QLineEdit(self)
        self.directory_input.setPlaceholderText("Enter starting directory (e.g., C:\\)")
        layout.addWidget(self.directory_input)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_directory)
        layout.addWidget(self.browse_button)

        self.keyword_input = QLineEdit(self)
        self.keyword_input.setPlaceholderText("Enter filename (partial match supported)")
        layout.addWidget(self.keyword_input)

        self.search_button = QPushButton("Deep Search", self)
        self.search_button.clicked.connect(self.start_search)
        layout.addWidget(self.search_button)

        self.result_box = QTextEdit(self)
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.save_button = QPushButton("Save Results", self)
        self.save_button.clicked.connect(self.save_results)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.results = []
        self.search_thread = None

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Starting Directory")
        if directory:
            self.directory_input.setText(directory)

    def start_search(self):
        directory = self.directory_input.text()
        keyword = self.keyword_input.text().strip()

        if not os.path.exists(directory):
            QMessageBox.critical(self, "Error", "Invalid directory")
            return

        if not keyword:
            QMessageBox.warning(self, "Warning", "Enter a search term")
            return

        # Prepare UI
        self.result_box.clear()
        self.result_box.append(f"Searching for '{keyword}' in {directory}...")
        self.progress_bar.setValue(50)  # Indeterminate progress
        self.search_button.setEnabled(False)
        self.save_button.setEnabled(False)

        # Start search thread
        self.search_thread = SearchThread(directory, keyword)
        self.search_thread.search_complete.connect(self.handle_search_complete)
        self.search_thread.search_error.connect(self.handle_search_error)
        
        # Start timing
        self.start_time = time.time()
        self.search_thread.start()

    def handle_search_complete(self, matches):
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        self.result_box.clear()
        self.result_box.append(f"Search completed in {elapsed_time:.2f} seconds")
        
        if matches:
            self.result_box.append(f"\nFound {len(matches)} items:")
            for match in matches[:1000]:
                self.result_box.append(match)
            
            if len(matches) > 1000:
                self.result_box.append(f"\n... and {len(matches) - 1000} more.")

            self.results = matches
            self.save_button.setEnabled(True)
        else:
            self.result_box.append("No matching files found.")

        self.progress_bar.setValue(100)
        self.search_button.setEnabled(True)

    def handle_search_error(self, error):
        QMessageBox.critical(self, "Search Error", str(error))
        self.search_button.setEnabled(True)
        self.progress_bar.setValue(0)

    def save_results(self):
        if not self.results:
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Save Results", "search_results.txt", "Text Files (*.txt)")
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                for item in self.results:
                    f.write(item + '\n')
            QMessageBox.information(self, "Success", f"Saved {len(self.results)} results")


if __name__ == "__main__":
    app = QApplication([])
    window = FastSearch()
    window.show()
    app.exec_()