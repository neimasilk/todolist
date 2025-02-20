import tkinter as tk
from tkinter import ttk, messagebox
from todo_engine import TodoList
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List Application")
        self.root.geometry("800x600")
        self.todo = TodoList()

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create search frame
        self.search_frame = ttk.LabelFrame(self.main_frame, text="Search", padding="5")
        self.search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Search widgets
        ttk.Label(self.search_frame, text="Text:").grid(row=0, column=0, padx=5)
        self.search_entry = ttk.Entry(self.search_frame, width=20)
        self.search_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.search_frame, text="Tags:").grid(row=0, column=2, padx=5)
        self.tags_entry = ttk.Entry(self.search_frame, width=20)
        self.tags_entry.grid(row=0, column=3, padx=5)

        ttk.Label(self.search_frame, text="Status:").grid(row=0, column=4, padx=5)
        self.status_var = tk.StringVar(value="All")
        self.status_combo = ttk.Combobox(self.search_frame, textvariable=self.status_var, values=["All", "Pending", "Completed"], width=10)
        self.status_combo.grid(row=0, column=5, padx=5)

        ttk.Button(self.search_frame, text="Search", command=self.search_tasks).grid(row=0, column=6, padx=5)
        ttk.Button(self.search_frame, text="Clear", command=self.clear_search).grid(row=0, column=7, padx=5)

        # Create and configure task list
        self.task_tree = ttk.Treeview(self.main_frame, columns=("ID", "Title", "Description", "Status", "Tags", "Created"), show="headings")
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("Title", text="Title")
        self.task_tree.heading("Description", text="Description")
        self.task_tree.heading("Status", text="Status")
        self.task_tree.heading("Tags", text="Tags")
        self.task_tree.heading("Created", text="Created")

        # Configure column widths
        self.task_tree.column("ID", width=50)
        self.task_tree.column("Title", width=150)
        self.task_tree.column("Description", width=200)
        self.task_tree.column("Status", width=100)
        self.task_tree.column("Tags", width=150)
        self.task_tree.column("Created", width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        # Create buttons frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Create buttons
        ttk.Button(self.button_frame, text="Add Task", command=self.show_add_task_dialog).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Mark Complete", command=self.mark_task_complete).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5)
        ttk.Button(self.button_frame, text="View Tags", command=self.show_tags).grid(row=0, column=3, padx=5)
        ttk.Button(self.button_frame, text="Refresh", command=self.refresh_task_list).grid(row=0, column=4, padx=5)

        # Layout
        self.task_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))

        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.search_frame.columnconfigure((1, 3), weight=1)

        # Initial refresh
        self.refresh_task_list()

    def show_add_task_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Task")
        dialog.geometry("400x300")
        dialog.transient(self.root)

        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")

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
                try:
                    self.todo.add_task(title, description)
                    self.refresh_task_list()
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "Title is required!")

        ttk.Button(frame, text="Save", command=save_task).grid(row=2, column=0, columnspan=2, pady=20)

        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def refresh_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # Sort tasks: Pending first, then by date (newest first)
        sorted_tasks = sorted(self.todo.tasks,
                             key=lambda x: (x['status'] == 'Completed',
                                         datetime.strptime(x['created_at'], '%Y-%m-%d %H:%M:%S').timestamp() * -1))

        for task in sorted_tasks:
            tags = ', '.join(task['tags']) if task['tags'] else 'No tags'
            self.task_tree.insert('', 'end', values=(task['id'], task['title'], task['description'],
                                                   task['status'], tags, task['created_at']))

    def mark_task_complete(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to mark as complete")
            return

        task_id = int(self.task_tree.item(selected_item[0])['values'][0])
        try:
            self.todo.update_task(task_id, "Completed")
            self.refresh_task_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            task_id = int(self.task_tree.item(selected_item[0])['values'][0])
            try:
                self.todo.delete_task(task_id)
                self.refresh_task_list()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def search_tasks(self):
        query = self.search_entry.get()
        tags = self.tags_entry.get()
        status = self.status_var.get()

        # Process search parameters
        tags = tags.split(',') if tags else None
        status = status if status != "All" else None

        try:
            results = self.todo.search_tasks(query=query if query else None,
                                           tags=tags,
                                           status=status)
            # Clear and update the tree view
            for item in self.task_tree.get_children():
                self.task_tree.delete(item)

            for task in results:
                tags = ', '.join(task['tags']) if task['tags'] else 'No tags'
                self.task_tree.insert('', 'end', values=(task['id'], task['title'], task['description'],
                                                       task['status'], tags, task['created_at']))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.tags_entry.delete(0, tk.END)
        self.status_var.set("All")
        self.refresh_task_list()

    def show_tags(self):
        try:
            tags = self.todo.get_all_tags()
            if tags:
                messagebox.showinfo("Available Tags", "\n".join(sorted(tags)))
            else:
                messagebox.showinfo("Tags", "No tags found")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()