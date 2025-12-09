import customtkinter as ctk
from PIL import Image, ImageTk

class Page2View(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.colors = {
            "dark_navy": "#22223B",
            "soft_beige": "#F4EDE2",
            "white": "#FFFFFF",
            "card_bg": "#FFFFFF",
            "text_primary": "#22223B",
            "text_secondary": "#4A4E69",
            "accent": "#4A4E69",
            "button_bg": "#22223B",
            "highlight": "#ECB45E",
            "category_colors": {
                "Core": "#FF6B6B",
                "Advanced": "#4ECDC4",
                "Modules": "#45B7D1",
                "Techniques": "#96CEB4"
            }
        }
        
        self.configure(fg_color=self.colors["soft_beige"], corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.create_widgets()
    
    def create_widgets(self):
        # Main container that fills entire window
        main_container = ctk.CTkFrame(self, fg_color=self.colors["soft_beige"])
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(
            main_container,
            fg_color=self.colors["soft_beige"],
            scrollbar_button_color="#CCCCCC",
            scrollbar_button_hover_color="#999999",
            border_width=0
        )
        scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Configure scrollable frame to expand
        scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # HEADER SECTION - Full width
        header_frame = ctk.CTkFrame(
            scrollable_frame,
            fg_color=self.colors["dark_navy"],
            height=200,
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=0, padx=0)
        header_frame.pack_propagate(False)
        
        # Header content with padding
        header_content = ctk.CTkFrame(header_frame, fg_color=self.colors["dark_navy"])
        header_content.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Text section (left)
        text_frame = ctk.CTkFrame(header_content, fg_color=self.colors["dark_navy"])
        text_frame.pack(side="left", fill="both", expand=True)
        
        title_label = ctk.CTkLabel(
            text_frame,
            text="PyWizz",
            font=("Arial", 32, "bold"),
            text_color="white"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            text_frame,
            text="Challenge yourself",
            font=("Arial", 16),
            text_color=self.colors["highlight"]
        )
        subtitle_label.pack(anchor="w", pady=(8, 0))
        
        # Character illustration (right) - transparent background
        try:
            character_img = ctk.CTkImage(
                light_image=Image.open("boy_yellow.png"),
                dark_image=Image.open("boy_yellow.png"),
                size=(140, 140)
            )
            character_label = ctk.CTkLabel(
                header_content,
                image=character_img,
                text="",
                fg_color=self.colors["dark_navy"]  # Match header background
            )
            character_label.pack(side="right")
        except:
            character_label = ctk.CTkLabel(
                header_content,
                text="🧑‍💻",
                font=("Arial", 60),
                text_color=self.colors["highlight"],
                fg_color=self.colors["dark_navy"]  # Match header background
            )
            character_label.pack(side="right")
        
        # Decorative line
        line_frame = ctk.CTkFrame(
            scrollable_frame,
            fg_color=self.colors["accent"],
            height=2,
            corner_radius=1
        )
        line_frame.pack(fill="x", padx=40, pady=(25, 30))
        line_frame.pack_propagate(False)
        
        # BODY CONTENT
        body_frame = ctk.CTkFrame(scrollable_frame, fg_color=self.colors["soft_beige"])
        body_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Configure body frame columns
        body_frame.grid_columnconfigure(0, weight=1)
        
        # Explore Quizzes header
        explore_header = ctk.CTkFrame(body_frame, fg_color=self.colors["soft_beige"], height=50)
        explore_header.pack(fill="x", pady=(0, 20))
        explore_header.pack_propagate(False)
        
        explore_header.grid_columnconfigure(0, weight=1)
        
        explore_label = ctk.CTkLabel(
            explore_header,
            text="Explore Quizzes",
            font=("Arial", 24, "bold"),
            text_color=self.colors["text_primary"]
        )
        explore_label.grid(row=0, column=0, sticky="w")
        
        history_button = ctk.CTkButton(
            explore_header,
            text="History",
            font=("Arial", 14),
            width=100,
            height=40,
            corner_radius=20,
            fg_color=self.colors["white"],
            hover_color="#F0F0F0",
            text_color=self.colors["text_primary"],
            border_width=2,
            border_color=self.colors["accent"],
            command=self.controller.show_history
        )
        history_button.grid(row=0, column=1, sticky="e")
        
        # CATEGORIES GRID - Using grid for equal sizing
        categories_frame = ctk.CTkFrame(body_frame, fg_color=self.colors["soft_beige"])
        categories_frame.pack(fill="both", expand=True)
        
        # Configure grid with equal columns
        categories_frame.grid_columnconfigure(0, weight=1)
        categories_frame.grid_columnconfigure(1, weight=1)
        categories_frame.grid_rowconfigure(0, weight=1)
        categories_frame.grid_rowconfigure(1, weight=1)
        
        # Category descriptions
        category_info = {
            "Core": "Basic Python concepts",
            "Advanced": "Complex Python features", 
            "Modules": "Standard libraries & packages",
            "Techniques": "Programming techniques"
        }
        
        # Create category cards in grid
        categories = ["Core", "Advanced", "Modules", "Techniques"]
        for i, category in enumerate(categories):
            row = i // 2
            col = i % 2
            
            # Create card container with fixed minimum size
            card_container = ctk.CTkFrame(
                categories_frame,
                fg_color=self.colors["white"],
                corner_radius=20,
                border_width=0
            )
            card_container.grid(row=row, column=col, padx=(0, 15) if col == 0 else (15, 0), pady=(0, 15) if row == 0 else 15, sticky="nsew")
            
            # Make card clickable
            card_container.bind("<Button-1>", lambda e, cat=category: self.controller.select_category(cat))
            card_container.configure(cursor="hand2")
            
            # Create the card content
            self.create_category_card(card_container, category, category_info[category])
        
        # Add bottom padding
        bottom_padding = ctk.CTkFrame(scrollable_frame, fg_color=self.colors["soft_beige"], height=40)
        bottom_padding.pack(fill="x")
    
    def create_category_card(self, parent, category, description):
        color = self.colors["category_colors"][category]
        
        # Configure parent to expand
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Main content frame
        content_frame = ctk.CTkFrame(parent, fg_color=self.colors["white"])
        content_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=20)
        
        # Left section (icon and text)
        left_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["white"])
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Icon with background color
        icon_frame = ctk.CTkFrame(
            left_frame,
            fg_color=color,
            width=60,
            height=60,
            corner_radius=15
        )
        icon_frame.pack(anchor="w")
        icon_frame.pack_propagate(False)
        
        # Category emojis
        category_emojis = {
            "Core": "🐍",
            "Advanced": "🚀", 
            "Modules": "📦",
            "Techniques": "💡"
        }
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text=category_emojis.get(category, "📚"),
            font=("Arial", 28),
            text_color="white",
            fg_color=color
        )
        icon_label.pack(expand=True)
        
        # Category name - MAKE SURE IT SHOWS
        category_label = ctk.CTkLabel(
            left_frame,
            text=category,
            font=("Arial", 18, "bold"),
            text_color=self.colors["text_primary"],
            anchor="w"
        )
        category_label.pack(anchor="w", pady=(15, 5))
        
        # Description - MAKE SURE IT SHOWS
        desc_label = ctk.CTkLabel(
            left_frame,
            text=description,
            font=("Arial", 12),
            text_color=self.colors["text_secondary"],
            anchor="w"
        )
        desc_label.pack(anchor="w")
        
        # Right section (arrow)
        right_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["white"], width=40)
        right_frame.pack(side="right")
        right_frame.pack_propagate(False)
        
        arrow_label = ctk.CTkLabel(
            right_frame,
            text="→",
            font=("Arial", 28, "bold"),
            text_color=color,
            fg_color=self.colors["white"]
        )
        arrow_label.pack(expand=True)
        arrow_label.bind("<Button-1>", lambda e, cat=category: self.controller.select_category(cat))