import tkinter as tk
from tkinter import ttk

class Page1View(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(bg="#E7DFD0")
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self, bg="#31304C", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="PyWizz",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#31304C"
        )
        header_label.pack(expand=True)
        
        # Welcome section
        welcome_frame = tk.Frame(self, bg="#E7DFD0")
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=40)
        
        # Welcome message
        welcome_label = tk.Label(
            welcome_frame,
            text="Welcome! Ready to test your Python skills?",
            font=("Arial", 14),
            fg="#31304C",
            bg="#E7DFD0",
            wraplength=300
        )
        welcome_label.pack(pady=(0, 30))
        
        # Name entry
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(
            welcome_frame,
            textvariable=self.name_var,
            font=("Arial", 12),
            bg="#F3F1EB",
            fg="#31304C",
            relief=tk.FLAT,
            justify=tk.CENTER
        )
        name_entry.pack(fill=tk.X, pady=(0, 20), ipady=8)
        name_entry.insert(0, "Enter your name")
        
        # Bind events for placeholder behavior
        name_entry.bind('<FocusIn>', self._on_entry_focus_in)
        name_entry.bind('<FocusOut>', self._on_entry_focus_out)
        
        # Start quiz button
        start_button = tk.Button(
            welcome_frame,
            text="Take a Quiz Now",
            font=("Arial", 12, "bold"),
            bg="#31304C",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_quiz
        )
        start_button.pack(fill=tk.X, ipady=10)
        
        # Apply rounded corners effect
        self._apply_rounded_style(name_entry)
        self._apply_rounded_style(start_button)
    
    def _on_entry_focus_in(self, event):
        if event.widget.get() == "Enter your name":
            event.widget.delete(0, tk.END)
            event.widget.config(fg="#31304C")
    
    def _on_entry_focus_out(self, event):
        if not event.widget.get():
            event.widget.insert(0, "Enter your name")
            event.widget.config(fg="#837D83")
    
    def _apply_rounded_style(self, widget):
        # Simulate rounded corners with a styled frame (Tkinter workaround)
        if isinstance(widget, tk.Entry):
            widget.config(highlightthickness=1, highlightbackground="#C1BBB3")
        elif isinstance(widget, tk.Button):
            widget.config(highlightthickness=1, highlightbackground="#31304C")
    
    def start_quiz(self):
        name = self.name_var.get().strip()
        if name and name != "Enter your name":
            self.controller.show_page2(name)
        else:
            # Show error or highlight field
            pass
    
    def get_name(self):
        return self.name_var.get().strip()