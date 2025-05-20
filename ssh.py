import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import shutil
from pathlib import Path

class SSHKeyGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zhdanov SSH generator")
        self.root.geometry("500x500")

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.frame, text="Nazwa klucza SSH:").pack(pady=5)
        self.key_name_entry = tk.Entry(self.frame)
        self.key_name_entry.pack(pady=5, fill=tk.X)

        self.generate_button = tk.Button(
            self.frame,
            text="Generuj klucz SSH",
            command=self.generate_ssh_key,
            bg="#4CAF50",
            fg="white"
        )
        self.generate_button.pack(pady=10, fill=tk.X)

        self.copy_button = tk.Button(
            self.frame,
            text="Kopiuj klucze do Backup",
            command=self.copy_ssh_keys_to_backup,
            bg="#2196F3",
            fg="white"
        )
        self.copy_button.pack(pady=10, fill=tk.X)

        self.exit_button = tk.Button(
            self.frame,
            text="Wyjdź",
            command=root.quit,
            bg="#F44336",
            fg="white"
        )
        self.exit_button.pack(pady=10, fill=tk.X)
        self.ssh_dir = os.path.expanduser("~/.ssh")
        self.backup_dir = os.path.expanduser("~/Backup/ssh_keys")

    def generate_ssh_key(self):

        key_name = self.key_name_entry.get().strip()
        if not key_name:
            messagebox.showerror("Blad", "Podaj nazwe klucza!")
            return

        if not os.path.exists(self.ssh_dir):
            os.makedirs(self.ssh_dir, mode=0o700)

        private_key_path = os.path.join(self.ssh_dir, key_name)
        public_key_path = f"{private_key_path}.pub"

        try:
            subprocess.run(
                ["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", private_key_path, "-N", "", "-q"],
                check=True
            )
            messagebox.showinfo("Sukces", f"Klucz SSH '{key_name}' został wygenerowany!")
            
            self.update_ssh_config(key_name, public_key_path)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Blad", f"Nie udało sie wygenerowac klucza: {e}")

    def update_ssh_config(self, key_name, public_key_path):
        config_path = os.path.join(self.ssh_dir, "config")
        
        if not os.path.exists(config_path):
            with open(config_path, "w") as f:
                f.write("")


        with open(config_path, "r") as f:
            config_content = f.read()

        new_entry = (
            f"\nHost github.com-{key_name}\n"
            f"  HostName github.com\n"
            f"  User git\n"
            f"  IdentityFile ~/.ssh/{key_name}\n"
            f"  IdentitiesOnly yes\n"
        )

        if f"IdentityFile ~/.ssh/{key_name}" not in config_content:
            with open(config_path, "a") as f:
                f.write(new_entry)
            messagebox.showinfo("Sukces", f"Dodano wpis do ~/.ssh/config!")

    def copy_ssh_keys_to_backup(self):
        if not os.path.exists(self.ssh_dir):
            messagebox.showerror("Błąd", "Folder ~/.ssh/ nie istnieje!")
            return

        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir, mode=0o700)

        try:
            for file in os.listdir(self.ssh_dir):
                if file.endswith((".pub", "_rsa")) or file == "config":
                    src = os.path.join(self.ssh_dir, file)
                    dst = os.path.join(self.backup_dir, file)
                    shutil.copy2(src, dst)
            messagebox.showinfo("Sukces", f"Klucze skopiowane do {self.backup_dir}!")
        except Exception as e:
            messagebox.showerror("Blad", f"Nie udało sie skopiowac kluczy: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHKeyGeneratorApp(root)
    root.mainloop()