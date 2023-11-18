import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os


def browse_path():
    global path_entry
    path = filedialog.askdirectory(title="Select Directory")
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)


def export_content():
    global path_entry, format_entry, output_path, text_area
    path = path_entry.get()
    format = format_entry.get()
    output_path = filedialog.asksaveasfilename(title="Save Exported Content", filetypes=[("Text Files", "*.txt"), ("PDF Files", "*.pdf")])

    if path and format and output_path:
        export_directory_content(path, format, output_path)


def export_directory_content(path, format, output_path):
    global text_area
    content = ""
    content += "Directory Listing:\n"
    content += list_directory_tree(path, 0)

    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension not in [".jpg", ".svg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".mp4", ".avi", ".mov", ".wmv", ".mp3", ".wav", ".ogg"]:
                file_content = read_file_content(file_path)
                content += "\n\nFile: " + file_path + "\n"
                content += file_content

    if format == "txt":
        with open(output_path, "w") as file:
            file.write(content)
    elif format == "pdf":
        # Import PDF library to create PDF document
        import pdfkit

        pdfkit.from_string(content, output_path)

    text_area.delete(0.0, tk.END)
    text_area.insert(0.0, "Content exported successfully!")


def list_directory_tree(path, level):
    content = ""
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            indent = level * "   "
            content += indent + file_path + "\n"

    return content


def read_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
    return file_content


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Directory Content Exporter")

    path_label = ttk.Label(root, text="Select Directory:")
    path_label.pack()

    path_entry = ttk.Entry(root, width=50)
    path_entry.pack()

    browse_button = ttk.Button(root, text="Browse", command=browse_path)
    browse_button.pack()

    format_label = ttk.Label(root, text="Select Format (txt/pdf):")
    format_label.pack()

    format_entry = ttk.Entry(root, width=20)
    format_entry.pack()

    export_button = ttk.Button(root, text="Export", command=export_content)
    export_button.pack()

    text_area = tk.Text(root, height=10, width=80)
    text_area.pack()

    root.mainloop()
