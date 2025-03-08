import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class GazeboLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Gazebo Scene Launcher")

        self.label = tk.Label(root, text="Select an SDF file to launch in Gazebo")
        self.label.pack(pady=10)

        self.file_path = tk.StringVar()
        self.file_label = tk.Label(root, textvariable=self.file_path, wraplength=300)
        self.file_label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select SDF File", command=self.select_file)
        self.select_button.pack(pady=5)

        self.launch_button = tk.Button(root, text="Launch in Gazebo", command=self.launch_gazebo, state=tk.DISABLED)
        self.launch_button.pack(pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            initialdir="/root/Worlds",
            title="Select SDF File",
            filetypes=(("SDF files", "*.sdf"), ("All files", "*.*"))
        )
        if file_path:
            self.file_path.set(file_path)
            self.launch_button.config(state=tk.NORMAL)

    def launch_gazebo(self):
        file_path = self.file_path.get()
        if file_path:
            try:
                subprocess.Popen(["ign", "gazebo", file_path])
                messagebox.showinfo("Launch Successful", f"Launched {file_path} in Gazebo")
            except Exception as e:
                messagebox.showerror("Launch Failed", f"Failed to launch Gazebo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GazeboLauncher(root)
    root.mainloop()
