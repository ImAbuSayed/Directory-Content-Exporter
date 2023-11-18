# Directory Content Exporter

![Directory Content Exporter GUI v.2 ](https://files.taskade.com/attachments/69ee0024-a152-475c-833f-42bde16a9886/original/Screenshot%202023-11-18%20004057.png)

The **Directory Content Exporter** is a Python tool that allows you to export the contents of a directory and its files into a text file or a PDF document. It provides a simple graphical user interface (GUI) built using the Tkinter library.

## Features

- Select a directory using the file browser.
- Choose the output format as either a text file or a PDF document.
- Export the directory and its files to the selected output format.
- Display the exported content in the GUI.
  
### Features Update
- 18/11/23
  -- Added Progress Bar on the GUI
  -- Added Exluded Options ( May not work Properly )

## Prerequisites

- Python 3.12.x installed on your system.
- Tkinter package installed (`pip install tkinter`) if not already available.
- "pdfkit" package installed (`pip install pdfkit`) for exporting to PDF.

## Usage

1. Clone the repository or download the source code.

```bash
git clone https://github.com/ImAbuSayed/directory-content-exporter.git
```

2. Open a terminal or command prompt and navigate to the project directory.

```bash
cd directory-content-exporter
```

3. Install the required packages.

```bash
pip install -r requirements.txt
```

4. Run the Python script.

```bash
python main.py
```

5. The application window will open.

![Directory Content Exporter GUI v.1 ](https://files.taskade.com/attachments/2b7691f8-480c-4dce-ae98-78a4875657a6/original/Screenshot%202023-11-18%20004057.png)

6. Select the directory you want to export by clicking the "Browse" button and navigating to the desired directory.

7. Choose the output format by entering either "txt" or "pdf" in the format entry field.

8. Click the "Export" button to start the export process.

9. A file dialog will prompt you to choose the location and name of the exported file. Select a suitable location and name with the appropriate extension based on the chosen format.

10. Once the export is complete, the exported content will be displayed in the text area below the export button. You can copy the content, close the application, or continue exporting content from different directories.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Credits

This project was created by [Abu Sayed](https://github.com/ImAbuSayed).

## Update

PDF Option is under development mode. ( This might not work properly )
