# SearchWindows

**SearchWindows** is a fast and efficient IOC, file, and folder name search tool designed specifically for Windows. It lets users quickly search through mounted drives or directories for specific file or folder names. This may be useful for **digital forensics**, **incident response**, and **general file management**.


---

## Features
- **IOC Search Capabilities**: Quickly locate files or folders matching known indicators of compromise.
- **Fast Results**: Optimized for speed with multithreading for processing large datasets.
- **GUI Application**: Simple and intuitive user interface built with PyQt5.
- **Save Search Results**: Export search results to a text file for further analysis or reporting.
- **Standalone Executable**: Includes a pre-compiled `.exe` for direct use on Windows systems.

---

## Use Cases
- **Digital Forensics**: Locate suspicious files or directories during evidence analysis.
- **Incident Response**: Search for files related to known malware or attack signatures during post-breach investigations.
- **IOC Searches**: Match file or folder names against a list of known malicious indicators provided by threat intelligence feeds.
- **File Management**: Quickly locate files or directories in large datasets or mounted drives.

---

## Requirements
To run the Python script (`searchOG.py`), you need:
- **Python 3.7+**
- **Dependencies**:
  - PyQt5
  - tqdm

Install the dependencies using:
```bash
pip install PyQt5 tqdm
```

For the standalone executable (`searchWindows.exe`), no setup is required.

---

## How to Use

### Running the Python Script
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/searchWindows.git
   cd searchWindows
   ```
2. Run the script:
   ```bash
   python searchOG.py
   ```
3. Use the GUI to:
   - Enter the directory or mounted drive to search.
   - Specify the file or folder name (or IOC) to search for.
   - View the search results and optionally save them to a file.

### Running the Executable
1. Download `searchWindows.exe` from the repository.
2. Double-click the executable to launch the application.
3. Follow the GUI instructions to perform your search.

---

## Performance Notes
- **Optimized Searching**: The application uses multithreading to enhance performance during searches.
- **Considerations**: For very large directories or mounted drives, the search time may vary depending on system resources and the number of files.

---

## Screenshots
![Screenshot 2024-12-21 134615](https://github.com/user-attachments/assets/17b9abed-0ab8-4763-8caf-d8bb9035b971)

![Screenshot 2024-12-21 134822](https://github.com/user-attachments/assets/2275e91b-501e-4be9-be50-680a868ac3f9)

---
