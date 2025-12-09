import customtkinter as ctk
from PIL import Image, ImageTk

class ResultsPageView(ctk.CTkFrame):
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
            "accent_gold": "#ECB45E",
            "neutral_beige": "#C1BBB3",
            "button_primary": "#22223B",
            "button_secondary": "#F4EDE2"
        }
        
        self.configure(fg_color=self.colors["soft_beige"], corner_radius=0)
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color=self.colors["soft_beige"])
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors["dark_navy"],
            height=80,
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=0, padx=0)
        header_frame.pack_propagate(False)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="Your Results",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        header_label.pack(expand=True)
        
        # Content
        content_frame = ctk.CTkFrame(main_frame, fg_color=self.colors["soft_beige"])
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Score section
        score_section = ctk.CTkFrame(content_frame, fg_color=self.colors["soft_beige"])
        score_section.pack(fill="x", pady=(0, 20))
        
        score_trophy_frame = ctk.CTkFrame(score_section, fg_color=self.colors["soft_beige"])
        score_trophy_frame.pack(fill="x", pady=(0, 10))
        
        self.score_label = ctk.CTkLabel(
            score_trophy_frame,
            text="1 / 1",
            font=("Arial", 32, "bold"),
            text_color=self.colors["text_primary"]
        )
        self.score_label.pack(side="left", expand=True)
        
        try:
            trophy_img = ctk.CTkImage(
                light_image=Image.open("trophy.png"),
                dark_image=Image.open("trophy.png"),
                size=(40, 40)
            )
            trophy_label = ctk.CTkLabel(
                score_trophy_frame,
                image=trophy_img,
                text=""
            )
            trophy_label.pack(side="right", padx=(10, 0))
        except:
            trophy_label = ctk.CTkLabel(
                score_trophy_frame,
                text="🏆",
                font=("Arial", 36),
                text_color=self.colors["accent_gold"]
            )
            trophy_label.pack(side="right", padx=(10, 0))
        
        self.message_label = ctk.CTkLabel(
            score_section,
            text="Perfect!",
            font=("Arial", 18),
            text_color=self.colors["text_secondary"]
        )
        self.message_label.pack()
        
        # Divider
        divider = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors["neutral_beige"],
            height=1
        )
        divider.pack(fill="x", pady=20)
        
        # Stats section
        stats_section = ctk.CTkFrame(content_frame, fg_color=self.colors["soft_beige"])
        stats_section.pack(fill="x", pady=(0, 30))
        
        stats_header = ctk.CTkLabel(
            stats_section,
            text="Correct / Wrong / Total Time",
            font=("Arial", 14, "bold"),
            text_color=self.colors["text_secondary"]
        )
        stats_header.pack(anchor="w", pady=(0, 15))
        
        stats_grid = ctk.CTkFrame(stats_section, fg_color=self.colors["soft_beige"])
        stats_grid.pack(fill="x")
        
        stats_data = [
            ("Correct", "self.correct_value"),
            ("Wrong", "self.wrong_value"),
            ("Total Time", "self.time_value")
        ]
        
        for i, (label_text, value_attr) in enumerate(stats_data):
            stat_frame = ctk.CTkFrame(stats_grid, fg_color=self.colors["soft_beige"])
            stat_frame.pack(side="left", expand=True, fill="both", padx=5)
            
            label = ctk.CTkLabel(
                stat_frame,
                text=label_text,
                font=("Arial", 12),
                text_color=self.colors["text_secondary"]
            )
            label.pack(pady=(0, 5))
            
            value_text = "1" if label_text == "Correct" else "0" if label_text == "Wrong" else "2:30"
            value = ctk.CTkLabel(
                stat_frame,
                text=value_text,
                font=("Arial", 20, "bold"),
                text_color=self.colors["text_primary"]
            )
            value.pack()
            
            if label_text == "Correct":
                self.correct_value = value
            elif label_text == "Wrong":
                self.wrong_value = value
            elif label_text == "Total Time":
                self.time_value = value
        
        # Divider 2
        divider2 = ctk.CTkFrame(
            content_frame,
            fg_color=self.colors["neutral_beige"],
            height=1
        )
        divider2.pack(fill="x", pady=20)
        
        # Buttons
        buttons_section = ctk.CTkFrame(content_frame, fg_color=self.colors["soft_beige"])
        buttons_section.pack(fill="x", pady=(0, 10))
        
        play_again_button = ctk.CTkButton(
            buttons_section,
            text="Play Again",
            font=("Arial", 16, "bold"),
            height=50,
            corner_radius=15,
            fg_color=self.colors["button_primary"],
            hover_color=self.colors["text_secondary"],
            text_color="white",
            command=self.on_play_again
        )
        play_again_button.pack(fill="x", pady=(0, 15))
        
        secondary_buttons_frame = ctk.CTkFrame(buttons_section, fg_color=self.colors["soft_beige"])
        secondary_buttons_frame.pack(fill="x")
        
        review_button = ctk.CTkButton(
            secondary_buttons_frame,
            text="Review Answers",
            font=("Arial", 14),
            height=40,
            corner_radius=12,
            fg_color=self.colors["button_secondary"],
            hover_color=self.colors["white"],
            text_color=self.colors["text_primary"],
            border_width=1,
            border_color=self.colors["neutral_beige"],
            command=self.on_review_answers
        )
        review_button.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        home_button = ctk.CTkButton(
            secondary_buttons_frame,
            text="Home",
            font=("Arial", 14),
            height=40,
            corner_radius=12,
            fg_color=self.colors["button_secondary"],
            hover_color=self.colors["white"],
            text_color=self.colors["text_primary"],
            border_width=1,
            border_color=self.colors["neutral_beige"],
            command=self.on_home
        )
        home_button.pack(side="right", expand=True, fill="x", padx=(10, 0))
        
        # History button
        history_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["soft_beige"])
        history_frame.pack(fill="x", pady=(20, 0))
        
        history_button = ctk.CTkButton(
            history_frame,
            text="History",
            font=("Arial", 12),
            height=35,
            width=100,
            corner_radius=10,
            fg_color=self.colors["button_secondary"],
            hover_color=self.colors["white"],
            text_color=self.colors["text_primary"],
            border_width=1,
            border_color=self.colors["neutral_beige"],
            command=self.on_history
        )
        history_button.pack(side="right")
    
    def update_results(self, score_correct, total_questions, correct_count, wrong_count, total_time, message):
        self.score_label.configure(text=f"{score_correct} / {total_questions}")
        self.message_label.configure(text=message)
        self.correct_value.configure(text=str(correct_count))
        self.wrong_value.configure(text=str(wrong_count))
        self.time_value.configure(text=total_time)
    
    def on_play_again(self):
        self.controller.on_play_again()
    
    def on_review_answers(self):
        self.controller.on_review_answers()
    
    def on_home(self):
        self.controller.on_home()
    
    def on_history(self):
        self.controller.on_history()