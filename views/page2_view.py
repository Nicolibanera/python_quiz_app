import tkinter as tk
from tkinter import ttk

class Page2View(tk.Frame):
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
        
        # Header content
        header_content = tk.Frame(header_frame, bg="#31304C")
        header_content.pack(expand=True, fill=tk.BOTH, padx=20)
        
        # App title
        title_label = tk.Label(
            header_content,
            text="PyWizz",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#31304C"
        )
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_content,
            text="Challenge yourself",
            font=("Arial", 10),
            fg="#ECB45E",
            bg="#31304C"
        )
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Body container
        body_container = tk.Frame(self, bg="#E7DFD0")
        body_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Body header with History button
        body_header = tk.Frame(body_container, bg="#E7DFD0")
        body_header.pack(fill=tk.X, pady=(0, 15))
        
        categories_label = tk.Label(
            body_header,
            text="Explore Quizzes",
            font=("Arial", 16, "bold"),
            fg="#31304C",
            bg="#E7DFD0"
        )
        categories_label.pack(side=tk.LEFT)
        
        history_button = tk.Button(
            body_header,
            text="History",
            font=("Arial", 10),
            bg="#F3F1EB",
            fg="#31304C",
            relief=tk.FLAT,
            cursor="hand2"
        )
        history_button.pack(side=tk.RIGHT)
        self._apply_rounded_style(history_button)
        
        # Categories container
        categories_frame = tk.Frame(body_container, bg="#F3F1EB", relief=tk.FLAT)
        categories_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create category cards
        categories = [
            "Basics",
            "Advanced", 
            "Libraries",
            "APIs"
        ]
        
        for i, category in enumerate(categories):
            self.create_category_card(categories_frame, category, i)
    
    def create_category_card(self, parent, category_name, index):
        card_frame = tk.Frame(
            parent,
            bg="#F3F1EB",
            relief=tk.RAISED,
            bd=1,
            highlightbackground="#C1BBB3"
        )
        card_frame.pack(fill=tk.X, padx=15, pady=8, ipady=10)
        
        # Card content
        content_frame = tk.Frame(card_frame, bg="#F3F1EB")
        content_frame.pack(fill=tk.X, padx=15)
        
        # Category name
        name_label = tk.Label(
            content_frame,
            text=category_name,
            font=("Arial", 12, "bold"),
            fg="#31304C",
            bg="#F3F1EB",
            anchor="w"
        )
        name_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Clickable area (simulated button)
        click_label = tk.Label(
            content_frame,
            text="→",
            font=("Arial", 14, "bold"),
            fg="#ECB45E",
            bg="#F3F1EB",
            cursor="hand2"
        )
        click_label.pack(side=tk.RIGHT)
        click_label.bind("<Button-1>", lambda e, cat=category_name: self.controller.select_category(cat))
        
        # Make the whole card clickable
        for widget in [card_frame, content_frame, name_label]:
            widget.bind("<Button-1>", lambda e, cat=category_name: self.controller.select_category(cat))
            widget.configure(cursor="hand2")
    
    def _apply_rounded_style(self, widget):
        # Simulate rounded corners
        if isinstance(widget, tk.Button):
            widget.config(highlightthickness=1, highlightbackground="#C1BBB3")