import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

class Page1View(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Colors
        self.colors = {
            "dark_navy": "#22223B",
            "soft_beige": "#F4EDE2",
            "white": "#FFFFFF",
            "accent": "#4A4E69",
            "light_gray": "#E0E0E0",
            "placeholder_gray": "#666666",  # Darker gray for better visibility
            "border_focus": "#2C3E50"
        }
        
        self.configure(fg_color=self.colors["soft_beige"], corner_radius=0)
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors["dark_navy"],
            height=120,
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=0, padx=0)
        header_frame.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header_frame, fg_color=self.colors["dark_navy"])
        header_content.pack(expand=True, fill="both", padx=30)
        
        try:
            brain_img = ctk.CTkImage(
                light_image=Image.open("brain.png"),
                dark_image=Image.open("brain.png"),
                size=(50, 50)
            )
            brain_label = ctk.CTkLabel(
                header_content,
                image=brain_img,
                text=""
            )
            brain_label.pack(side="left", padx=(0, 15))
        except:
            brain_label = ctk.CTkLabel(
                header_content,
                text="🧠",
                font=("Arial", 40),
                text_color="white"
            )
            brain_label.pack(side="left", padx=(0, 15))
        
        title_label = ctk.CTkLabel(
            header_content,
            text="PyWizz",
            font=("Arial", 32, "bold"),
            text_color="white"
        )
        title_label.pack(side="left", fill="x", expand=True)
        
        # Main content container with proper margins
        main_container = ctk.CTkFrame(self, fg_color=self.colors["soft_beige"])
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Create outer frame with padding for scrollbar
        outer_frame = ctk.CTkFrame(main_container, fg_color=self.colors["soft_beige"])
        outer_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create scrollable frame
        content_frame = ctk.CTkScrollableFrame(
            outer_frame,
            fg_color=self.colors["soft_beige"],
            scrollbar_button_color=self.colors["light_gray"],
            scrollbar_button_hover_color=self.colors["accent"],
            border_width=0,
            corner_radius=10
        )
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Illustration with rounded frame
        illustration_frame = ctk.CTkFrame(
            content_frame, 
            fg_color=self.colors["soft_beige"]
        )
        illustration_frame.pack(fill="x", pady=(10, 30))
        
        # Create a container with white background and rounded corners
        image_container = ctk.CTkFrame(
            illustration_frame,
            fg_color=self.colors["white"],
            width=220,
            height=220,
            corner_radius=20
        )
        image_container.pack()
        image_container.pack_propagate(False)
        
        try:
            boy_img = ctk.CTkImage(
                light_image=Image.open("boy.png"),
                dark_image=Image.open("boy.png"),
                size=(200, 200)
            )
            boy_label = ctk.CTkLabel(
                image_container,
                image=boy_img,
                text="",
                fg_color=self.colors["white"]
            )
            boy_label.pack(expand=True, padx=10, pady=10)
        except:
            fallback_label = ctk.CTkLabel(
                image_container,
                text="🧑‍💻",
                font=("Arial", 80),
                text_color=self.colors["dark_navy"],
                fg_color=self.colors["white"]
            )
            fallback_label.pack(expand=True)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            content_frame,
            text="Welcome! Ready to test your Python skills?",
            font=("Arial", 18),
            text_color=self.colors["dark_navy"],
            wraplength=300
        )
        welcome_label.pack(pady=(0, 30))
        
        # Name entry - FIXED APPROACH
        self.name_var = ctk.StringVar(value="")
        
        # Create entry frame
        entry_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["soft_beige"])
        entry_frame.pack(pady=(0, 20))
        
        # Create the entry widget with ALTERNATIVE placeholder approach
        self.name_entry = ctk.CTkEntry(
            entry_frame,
            textvariable=self.name_var,
            font=("Arial", 14),
            height=50,
            width=300,
            corner_radius=15,
            fg_color=self.colors["white"],
            border_color=self.colors["accent"],
            border_width=2,
            text_color=self.colors["dark_navy"]
        )
        self.name_entry.pack()
        
        # Create a label that acts as a placeholder (but doesn't block clicks)
        self.placeholder_label = ctk.CTkLabel(
            entry_frame,
            text="Enter your name",
            font=("Arial", 14),
            text_color=self.colors["placeholder_gray"],
            fg_color=self.colors["soft_beige"]
        )
        
        # Position the placeholder label over the entry (but not blocking it)
        self.placeholder_label.place(in_=self.name_entry, relx=0.05, rely=0.5, anchor="w")
        
        # Track if we should show placeholder
        self.show_placeholder = True
        
        # Bind events
        self.name_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.name_entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.name_entry.bind("<KeyRelease>", self.on_key_release)
        
        # Monitor variable changes
        self.name_var.trace_add("write", self.on_name_change)
        
        # Start button
        start_button = ctk.CTkButton(
            content_frame,
            text="Take a Quiz Now",
            font=("Arial", 16, "bold"),
            height=55,
            width=300,
            corner_radius=15,
            fg_color=self.colors["dark_navy"],
            hover_color=self.colors["accent"],
            text_color="white",
            command=self.start_quiz
        )
        start_button.pack(pady=(0, 20))
        
        # Stats section
        stats_container = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors["soft_beige"]
        )
        stats_container.pack(fill="x", pady=(0, 20))
        
        stats_text = """🎯 Test your Python knowledge
📊 Track your progress
🏆 Earn achievements"""
        
        stats_label = ctk.CTkLabel(
            stats_container,
            text=stats_text,
            font=("Arial", 12),
            text_color=self.colors["accent"],
            justify="center"
        )
        stats_label.pack()
        
        # Footer with padding
        footer_frame = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors["soft_beige"],
            height=30
        )
        footer_frame.pack(fill="x", pady=(10, 0))
        
        # Add padding frame at the bottom for better spacing
        bottom_padding = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors["soft_beige"],
            height=20
        )
        bottom_padding.pack(fill="x")
    
    def on_entry_focus_in(self, event):
        """Handle focus in event for name entry"""
        self.name_entry.configure(border_color=self.colors["border_focus"])
        
        # Hide placeholder when focused
        if self.show_placeholder:
            self.placeholder_label.place_forget()
    
    def on_entry_focus_out(self, event):
        """Handle focus out event for name entry"""
        self.name_entry.configure(border_color=self.colors["accent"])
        
        # Show placeholder if field is empty
        if not self.name_var.get().strip():
            self.placeholder_label.place(in_=self.name_entry, relx=0.05, rely=0.5, anchor="w")
            self.show_placeholder = True
    
    def on_key_release(self, event):
        """Handle key release in entry field"""
        # Update placeholder visibility based on content
        if self.name_var.get().strip():
            self.placeholder_label.place_forget()
            self.show_placeholder = False
        else:
            if not self.name_entry.focus_get():  # Only show if not focused
                self.placeholder_label.place(in_=self.name_entry, relx=0.05, rely=0.5, anchor="w")
                self.show_placeholder = True
    
    def on_name_change(self, *args):
        """Handle changes to the name variable"""
        # This is a backup to ensure placeholder visibility is correct
        if self.name_var.get().strip():
            self.placeholder_label.place_forget()
            self.show_placeholder = False
        elif not self.name_entry.focus_get():
            self.placeholder_label.place(in_=self.name_entry, relx=0.05, rely=0.5, anchor="w")
            self.show_placeholder = True
    
    def start_quiz(self):
        name = self.name_var.get().strip()
        
        if name:
            self.controller.show_page2(name)
        else:
            # Show error message box
            messagebox.showwarning(
                "Name Required",
                "Please enter your name to start the quiz.",
                parent=self
            )
            # Focus on the entry field
            self.name_entry.focus_set()