# views/review_answers_page.py
import customtkinter as ctk
from tkinter import messagebox

class ReviewAnswersPage(ctk.CTkFrame):
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
            "correct_green": "#4CAF50",
            "incorrect_red": "#F44336",
            "neutral_gray": "#E0E0E0",
            "selected_blue": "#2196F3",
            "light_green": "#E8F5E9",
            "light_red": "#FFEBEE"
        }
        
        self.configure(fg_color=self.colors["soft_beige"], corner_radius=0)
        
        # Store answer history and questions
        self.answer_history = []
        self.questions_data = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color=self.colors["soft_beige"])
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Top bar
        top_bar = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors["dark_navy"],
            height=70,
            corner_radius=0
        )
        top_bar.pack(fill="x", pady=0, padx=0)
        top_bar.pack_propagate(False)
        
        top_content = ctk.CTkFrame(top_bar, fg_color=self.colors["dark_navy"])
        top_content.pack(expand=True, fill="both", padx=25)
        
        # Title
        title_label = ctk.CTkLabel(
            top_content,
            text="Review Answers",
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        title_label.pack(side="left", fill="x", expand=True)
        
        # Back button
        back_button = ctk.CTkButton(
            top_content,
            text="← Back",
            font=("Arial", 14),
            width=80,
            height=35,
            fg_color="transparent",
            hover_color="#4A4E69",
            text_color="white",
            border_width=1,
            border_color="white",
            command=self.controller.on_back_from_review
        )
        back_button.pack(side="right")
        
        # Scrollable frame for questions
        self.scrollable_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=self.colors["soft_beige"]
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Summary frame
        self.summary_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors["white"],
            corner_radius=15,
            border_width=2,
            border_color=self.colors["neutral_gray"]
        )
        self.summary_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.summary_label = ctk.CTkLabel(
            self.summary_frame,
            text="",
            font=("Arial", 14),
            text_color=self.colors["text_primary"]
        )
        self.summary_label.pack(padx=20, pady=15)
    
    def set_answer_data(self, answer_history, questions_data):
        """Set the answer history and questions data for review"""
        self.answer_history = answer_history
        self.questions_data = questions_data
        self.display_review()
    
    def display_review(self):
        """Display all questions with answers"""
        # Clear existing content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.answer_history or not self.questions_data:
            no_data_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No answer data available for review.",
                font=("Arial", 16),
                text_color=self.colors["text_secondary"]
            )
            no_data_label.pack(pady=50)
            return
        
        total_questions = len(self.questions_data)
        correct_count = 0
        
        for i, (question_data, answer_data) in enumerate(zip(self.questions_data, self.answer_history)):
            # Create question card
            question_card = ctk.CTkFrame(
                self.scrollable_frame,
                fg_color=self.colors["white"],
                corner_radius=15,
                border_width=2,
                border_color=self.colors["neutral_gray"]
            )
            question_card.pack(fill="x", pady=10, padx=5)
            
            # Question header
            header_frame = ctk.CTkFrame(question_card, fg_color=self.colors["white"])
            header_frame.pack(fill="x", padx=20, pady=(15, 10))
            
            # Question number and status
            is_correct = answer_data.get("is_correct", False)
            if is_correct:
                correct_count += 1
                status_text = "✓ Correct"
                status_color = self.colors["correct_green"]
                card_bg = self.colors["light_green"]
            else:
                status_text = "✗ Incorrect"
                status_color = self.colors["incorrect_red"]
                card_bg = self.colors["light_red"]
            
            # Set card background color based on correctness
            question_card.configure(fg_color=card_bg)
            
            # Question number
            question_num_label = ctk.CTkLabel(
                header_frame,
                text=f"Question {i + 1}",
                font=("Arial", 16, "bold"),
                text_color=self.colors["text_primary"]
            )
            question_num_label.pack(side="left")
            
            # Status indicator
            status_label = ctk.CTkLabel(
                header_frame,
                text=status_text,
                font=("Arial", 14, "bold"),
                text_color=status_color
            )
            status_label.pack(side="right")
            
            # Question text
            question_frame = ctk.CTkFrame(question_card, fg_color=card_bg)
            question_frame.pack(fill="x", padx=20, pady=(0, 10))
            
            question_text_label = ctk.CTkLabel(
                question_frame,
                text=question_data["question"],
                font=("Arial", 14),
                text_color=self.colors["text_primary"],
                wraplength=550,
                justify="left"
            )
            question_text_label.pack(anchor="w")
            
            # Answers section
            answers_frame = ctk.CTkFrame(question_card, fg_color=card_bg)
            answers_frame.pack(fill="x", padx=20, pady=(0, 15))
            
            # User's answer
            user_answer_frame = ctk.CTkFrame(answers_frame, fg_color=card_bg)
            user_answer_frame.pack(fill="x", pady=(0, 10))
            
            user_label = ctk.CTkLabel(
                user_answer_frame,
                text="Your Answer:",
                font=("Arial", 13, "bold"),
                text_color=self.colors["text_secondary"]
            )
            user_label.pack(anchor="w", pady=(0, 5))
            
            selected_index = answer_data.get("selected_index", -1)
            if 0 <= selected_index < len(question_data["options"]):
                user_answer_text = question_data["options"][selected_index]
                user_answer_color = status_color
            else:
                user_answer_text = "No answer selected"
                user_answer_color = self.colors["text_secondary"]
            
            user_answer_label = ctk.CTkLabel(
                user_answer_frame,
                text=user_answer_text,
                font=("Arial", 13),
                text_color=user_answer_color,
                wraplength=500,
                justify="left"
            )
            user_answer_label.pack(anchor="w", padx=20)
            
            # Correct answer
            correct_answer_frame = ctk.CTkFrame(answers_frame, fg_color=card_bg)
            correct_answer_frame.pack(fill="x")
            
            correct_label = ctk.CTkLabel(
                correct_answer_frame,
                text="Correct Answer:",
                font=("Arial", 13, "bold"),
                text_color=self.colors["text_secondary"]
            )
            correct_label.pack(anchor="w", pady=(0, 5))
            
            correct_index = question_data.get("answer", question_data.get("correct_answer", 0))
            if 0 <= correct_index < len(question_data["options"]):
                correct_answer_text = question_data["options"][correct_index]
            else:
                correct_answer_text = "Error: No correct answer found"
            
            correct_answer_label = ctk.CTkLabel(
                correct_answer_frame,
                text=correct_answer_text,
                font=("Arial", 13),
                text_color=self.colors["correct_green"],
                wraplength=500,
                justify="left"
            )
            correct_answer_label.pack(anchor="w", padx=20)
            
            # Explanation (if available)
            if "explanation" in question_data:
                explanation_frame = ctk.CTkFrame(question_card, fg_color=card_bg)
                explanation_frame.pack(fill="x", padx=20, pady=(0, 15))
                
                explanation_label = ctk.CTkLabel(
                    explanation_frame,
                text="Explanation:",
                    font=("Arial", 13, "bold"),
                    text_color=self.colors["text_secondary"]
                )
                explanation_label.pack(anchor="w", pady=(0, 5))
                
                explanation_text_label = ctk.CTkLabel(
                    explanation_frame,
                    text=question_data["explanation"],
                    font=("Arial", 12),
                    text_color=self.colors["text_primary"],
                    wraplength=500,
                    justify="left"
                )
                explanation_text_label.pack(anchor="w", padx=20)
            
            # Separator
            if i < total_questions - 1:
                separator = ctk.CTkFrame(
                    self.scrollable_frame,
                    height=2,
                    fg_color=self.colors["neutral_gray"]
                )
                separator.pack(fill="x", pady=5, padx=20)
        
        # Update summary
        percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        self.summary_label.configure(
            text=f"Score: {correct_count}/{total_questions} ({percentage:.1f}%)"
        )