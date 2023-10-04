import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import os


class AliasManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Alias Manager")

        self.ensure_bash_aliases_imported()
        self.aliases = self.load_aliases()

        # Layout
        self.alias_listbox = scrolledtext.ScrolledText(
            root, width=50, height=15)
        self.alias_listbox.pack(pady=20)
        self.alias_listbox.config(state=tk.DISABLED)

        self.add_button = tk.Button(
            root, text="Adicionar Alias", command=self.add_alias)
        self.add_button.pack(pady=10)

        self.remove_button = tk.Button(
            root, text="Remover Alias Selecionado", command=self.remove_selected_alias)
        self.remove_button.pack(pady=10)

        self.update_display()

    def ensure_bash_aliases_imported(self):
        bashrc_path = os.path.expanduser("~/.bashrc")
        with open(bashrc_path, 'a+') as f:
            f.seek(0)
            content = f.read()
            if "source ~/.bash_aliases" not in content:
                f.write("\nsource ~/.bash_aliases\n")

    def load_aliases(self):
        aliases = {}
        alias_path = os.path.expanduser("~/.bash_aliases")
        try:
            with open(alias_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("alias "):
                        parts = line.split("=")
                        alias_name = parts[0][6:].strip()
                        alias_command = parts[1].strip().replace("'", "")
                        aliases[alias_name] = alias_command
        except FileNotFoundError:
            pass
        return aliases

    def reload_aliases(self):
        os.system("source ~/.bash_aliases")

    def update_display(self):
        self.alias_listbox.config(state=tk.NORMAL)
        self.alias_listbox.delete(1.0, tk.END)
        for alias, command in self.aliases.items():
            self.alias_listbox.insert(tk.END, f"{alias} -> {command}\n")
        self.alias_listbox.config(state=tk.DISABLED)

    def add_alias(self):
        alias_name = simpledialog.askstring(
            "Nome do Alias", "Digite o nome do alias:")
        alias_command = simpledialog.askstring(
            "Comando Alias", "Digite o comando do alias:")
        if alias_name and alias_command:
            self.aliases[alias_name] = alias_command
            self.save_aliases()
            self.update_display()

    def remove_selected_alias(self):
        self.alias_listbox.config(state=tk.NORMAL)
        selected_text = self.alias_listbox.get(
            tk.SEL_FIRST, tk.SEL_LAST).strip()
        self.alias_listbox.config(state=tk.DISABLED)
        if " -> " in selected_text:
            alias_name = selected_text.split(" -> ")[0]
            if alias_name in self.aliases:
                del self.aliases[alias_name]
                self.save_aliases()
                self.update_display()

    def save_aliases(self):
        alias_path = os.path.expanduser("~/.bash_aliases")
        try:
            with open(alias_path, "w") as f:
                for alias, command in self.aliases.items():
                    f.write(f"alias {alias}='{command}'\n")

            self.reload_aliases()

            messagebox.showinfo("Sucesso", "Aliases salvos com sucesso!")
        except IOError as e:
            messagebox.showerror("Erro", f"Erro ao salvar os aliases! {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar os aliases! {e}")


if __name__ == "__main__":
    root = tk.Tk()
    manager = AliasManager(root)
    root.mainloop()
