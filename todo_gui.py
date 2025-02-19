import tkinter as tk
from tkinter import ttk, messagebox
from todo import TodoList

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List Application")
        self.root.geometry("600x400")
        self.todo = TodoList()

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create and configure task list
        self.task_tree = ttk.Treeview(self.main_frame, columns=("ID", "Title", "Description", "Status", "Created"), show="headings")
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Title", text="Title")
        self.task_tree.heading("Description", text="Description")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Created", text="Created")

        # Configure column widths
        self.task_tree.column("ID", width=50)
        self.task_tree.column("Title", width=100)
        self.task_tree.column("Description", width=150)
        self.task_tree.column("Status", width=100)
        self.task_tree.column("Created", width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        # Create buttons frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Create buttons
        ttk.Button(self.button_frame, text="Add Task", command=self.show_add_task_dialog).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Mark Complete", command=self.mark_task_complete).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5)
        ttk.Button(self.button_frame, text="Refresh", command=self.refresh_task_list).grid(row=0, column=3, padx=5)

        # Layout
        self.task_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Initial refresh
        self.refresh_task_list()

    def show_add_task_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Task")
        dialog.geometry("400x300")
        dialog.transient(self.root)

        # Center the dialog on the screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")

        # Create a frame with padding
        frame = ttk.Frame(dialog, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        title_entry = ttk.Entry(frame, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        desc_text = tk.Text(frame, width=30, height=8)
        desc_text.grid(row=1, column=1, padx=5, pady=5)

        def save_task():
            title = title_entry.get()
            description = desc_text.get("1.0", tk.END).strip()
            if title:
                self.todo.add_task(title, description)
                self.refresh_task_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Title is required!")

        ttk.Button(frame, text="Save", command=save_task).grid(row=2, column=0, columnspan=2, pady=20)

        # Configure grid weights for the frame
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def mark_task_complete(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to mark as complete!")
            return

        task_id = int(self.task_tree.item(selected_item[0])['values'][0])
        self.todo.update_task(task_id, "Completed")
        self.refresh_task_list()

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            task_id = int(self.task_tree.item(selected_item[0])['values'][0])
            self.todo.delete_task(task_id)
            self.refresh_task_list()

    def refresh_task_list(self):
        # Clear existing items
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Reload tasks
        for task in self.todo.tasks:
            self.task_tree.insert("", tk.END, values=(
                task['id'],
                task['title'],
                task['description'],
                task['status'],
                task['created_at']
            ))

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()