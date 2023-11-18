import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import fnmatch
import pdfkit

class DirectoryContentExporter:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory Content Exporter")
        self.excluded_dirs = []
        self.excluded_files = set([".jpg", ".svg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".mp4", ".avi", ".mov", ".wmv", ".mp3", ".wav", ".ogg"])
        self.output_path = ""

        # GUI components for directory exclusion
        self.excluded_dirs_listbox = tk.Listbox(root)
        self.excluded_dirs_listbox.pack()

        self.exclude_dirs_button = ttk.Button(
            root, text="Browse", command=self.browse_exclude_dir)
        self.exclude_dirs_button.pack()

        self.remove_dir_button = ttk.Button(
            root, text="Remove", command=self.remove_excluded_dir)
        self.remove_dir_button.pack()

        self.exclude_all = tk.BooleanVar()
        self.exclude_all_checkbox = ttk.Checkbutton(
            root, variable=self.exclude_all, text="Exclude all under")
        self.exclude_all_checkbox.pack()

        # GUI components for directory export
        self.path_label = ttk.Label(root, text="Select Directory:")
        self.path_label.pack()

        self.path_entry = ttk.Entry(root, width=50)
        self.path_entry.pack()

        self.browse_button = ttk.Button(
            root, text="Browse", command=self.browse_path)
        self.browse_button.pack()

        self.format_label = ttk.Label(
            root, text="Select Format (txt/pdf):")
        self.format_label.pack()

        self.format_entry = ttk.Entry(root, width=20)
        self.format_entry.pack()

        # GUI components for exclusion patterns
        self.exclude_patterns_label = ttk.Label(
            root, text="Exclude Patterns (comma-separated):")
        self.exclude_patterns_label.pack()

        self.exclude_patterns_entry = ttk.Entry(root, width=50)
        self.exclude_patterns_entry.pack()

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            root, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.pack()

        self.export_button = ttk.Button(
            root, text="Export", command=self.export_content)
        self.export_button.pack()

        self.text_area = tk.Text(root, height=10, width=80)
        self.text_area.pack()

    def browse_exclude_dir(self):
        dirname = filedialog.askdirectory(
            title="Select directory to exclude")
        if dirname not in self.excluded_dirs:
            self.excluded_dirs.append(dirname)
            self.update_excluded_dirs_listbox()

    def update_excluded_dirs_listbox(self):
        self.excluded_dirs_listbox.delete(0, tk.END)
        for directory in self.excluded_dirs:
            self.excluded_dirs_listbox.insert(tk.END, directory)

    def remove_excluded_dir(self):
        selected_index = self.excluded_dirs_listbox.curselection()
        if selected_index:
            removed_dir = self.excluded_dirs_listbox.get(selected_index)
            self.excluded_dirs.remove(removed_dir)
            self.update_excluded_dirs_listbox()
        else:
            messagebox.showwarning("Warning", "No directory selected")

    def browse_path(self):
        path = filedialog.askdirectory(title="Select Directory")
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

    def update_progress_bar(self, count, total_files):
        progress_value = int((count / total_files) * 100)
        self.progress_bar["value"] = progress_value
        self.root.update()

    def export_content(self):
        self.excluded_dirs = ['node_modules']
        path = self.path_entry.get()
        file_format = self.format_entry.get()
        exclude_patterns = [pattern.strip()
                            for pattern in self.exclude_patterns_entry.get().split(",")]

        self.output_path = filedialog.asksaveasfilename(title="Save Exported Content", filetypes=[
            ("Text Files", ".txt"), ("PDF Files", ".pdf")])

        if path and file_format and self.output_path:
            exclude_all_val = self.exclude_all.get() == 1
            self.export_directory_content(
                path, file_format, exclude_all_val, exclude_patterns)

    def export_directory_content(self, path, file_format, exclude_all, exclude_patterns):
        content = ""
        total_files = self.count_files(path)
        contents = self.fetch_all_file_content(
            path, lambda countFile: self.update_progress_bar(countFile, total_files), self.excluded_dirs, exclude_patterns)

        # Create a table of contents
        content += "Table of Contents:\n"
        for idx, item in enumerate(contents, start=1):
            content += f"{idx}. {item['File_Path']}\n"

        # Add a separator
        content += "\n\n"

        # Add file content
        for item in contents:
            content += f"{item['File_Path']}\n\n{item['Content']}\n\n"

        if file_format == "txt":
            with open(self.output_path, "w", encoding="utf-8") as file:
                file.write(content)
        elif file_format == "pdf":
            pdfkit.from_string(content, self.output_path)

        self.text_area.delete(0.0, tk.END)
        self.text_area.insert(0.0, "Content exported successfully!")

    def fetch_all_file_content(self, directory, on_waking, exclude_dirs=[], exclude_patterns=[]):
        file_contents_list = []
        count_files = 0

        for root, dirs, files in os.walk(directory, topdown=True):
            # Exclude specific directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if all(not fnmatch.fnmatch(file, pattern) for pattern in exclude_patterns):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        try:
                            content = f.read().decode("utf-8")
                            file_contents_list.append(
                                {'File_Path': file_path, 'Content': content})
                            count_files += 1
                        except UnicodeDecodeError:
                            continue

                    on_waking(count_files)

        return file_contents_list

    def count_files(self, path):
        count = sum(len(files) for _, _, files in os.walk(path))
        return count


if __name__ == "__main__":
    root = tk.Tk()
    app = DirectoryContentExporter(root)
    root.mainloop()
