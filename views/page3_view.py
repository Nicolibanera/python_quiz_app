import customtkinter as ctk
import time

class Page3View(ctk.CTkFrame):
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
            "selected_blue": "#2196F3"
        }
        
        self.configure(fg_color=self.colors["soft_beige"], corner_radius=0)
        self.create_widgets()
    
    def create_widgets(self):
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
        
        self.category_label = ctk.CTkLabel(
            top_content,
            text="Intermediate Concepts",
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        self.category_label.pack(side="left", fill="x", expand=True)
        
        # Timer display (shows time spent on current question)
        self.timer_frame = ctk.CTkFrame(top_content, fg_color=self.colors["dark_navy"])
        self.timer_frame.pack(side="right")
        
        self.timer_label = ctk.CTkLabel(
            self.timer_frame,
            text="0s",
            font=("Arial", 14),
            text_color="#FFD700"
        )
        self.timer_label.pack()
        
        # Progress
        progress_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors["soft_beige"],
            height=40
        )
        progress_frame.pack(fill="x", padx=25, pady=(15, 10))
        progress_frame.pack_propagate(False)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Question 1 of 1",
            font=("Arial", 14),
            text_color=self.colors["text_primary"]
        )
        self.progress_label.pack(side="left")
        
        # Question container
        question_container = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors["soft_beige"]
        )
        question_container.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        
        # Question card
        self.question_card = ctk.CTkFrame(
            question_container,
            fg_color=self.colors["white"],
            corner_radius=20,
            border_width=2,
            border_color=self.colors["neutral_gray"]
        )
        self.question_card.pack(fill="both", expand=True, pady=(0, 20))
        
        self.question_label = ctk.CTkLabel(
            self.question_card,
            text="What does the @staticmethod decorator do?",
            font=("Arial", 16),
            text_color=self.colors["text_primary"],
            wraplength=500,
            justify="left"
        )
        self.question_label.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Answers container
        answers_container = ctk.CTkFrame(question_container, fg_color=self.colors["soft_beige"])
        answers_container.pack(fill="both", expand=True)
        
        self.answer_buttons = []
        for i in range(4):
            answer_frame = ctk.CTkFrame(answers_container, fg_color=self.colors["soft_beige"])
            answer_frame.pack(fill="x", pady=8)
            
            btn = ctk.CTkButton(
                answer_frame,
                text="",
                font=("Arial", 14),
                height=60,
                corner_radius=15,
                fg_color=self.colors["white"],
                hover_color=self.colors["neutral_gray"],
                text_color=self.colors["text_primary"],
                border_width=2,
                border_color=self.colors["neutral_gray"],
                anchor="w",
                command=lambda idx=i: self.on_answer_selected(idx)
            )
            btn.pack(fill="x", padx=0)
            self.answer_buttons.append(btn)
        
        # Next button
        bottom_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors["soft_beige"],
            height=80
        )
        bottom_frame.pack(fill="x", side="bottom", padx=25, pady=(0, 20))
        bottom_frame.pack_propagate(False)
        
        self.next_button = ctk.CTkButton(
            bottom_frame,
            text="Next",
            font=("Arial", 16, "bold"),
            height=50,
            corner_radius=15,
            fg_color=self.colors["dark_navy"],
            hover_color=self.colors["accent"],
            text_color="white",
            command=self.on_next_button_clicked
        )
        self.next_button.pack(fill="x")
        
        # State variables
        self.selected_answer = None
        self.answer_submitted = False
        self.correct_answer_index = None
        
        # Time tracking
        self.question_start_time = 0
        self.question_time = 0  # Time spent on current question in seconds
        self.quiz_start_time = 0  # Overall quiz start time
        self.total_quiz_time = 0  # Total time spent on quiz so far
    
    def adjust_font_size(self, text, max_width=320):
        avg_char_width = 9
        text_width = len(text) * avg_char_width
        
        if text_width > max_width * 1.5:
            font_size = 14
        elif text_width > max_width:
            font_size = 15
        else:
            font_size = 16
        
        return font_size
    
    def on_answer_selected(self, index):
        if self.answer_submitted:
            return  # Don't allow selection after submission
        
        self.selected_answer = index
        
        # Reset all buttons to default state
        for i, btn in enumerate(self.answer_buttons):
            if i == index:
                # Highlight selected button
                btn.configure(
                    fg_color=self.colors["selected_blue"],
                    text_color="white",
                    border_color=self.colors["selected_blue"]
                )
            else:
                # Reset other buttons
                btn.configure(
                    fg_color=self.colors["white"],
                    border_color=self.colors["neutral_gray"],
                    text_color=self.colors["text_primary"]
                )
    
    def submit_answer(self):
        """Submit the selected answer"""
        if self.selected_answer is None:
            return  # No answer selected
        
        # Stop timer for this question
        self.stop_question_timer()
        
        self.answer_submitted = True
        
        # Disable all buttons
        for btn in self.answer_buttons:
            btn.configure(state="disabled")
        
        # Highlight correct and incorrect answers
        for i, btn in enumerate(self.answer_buttons):
            if i == self.correct_answer_index:
                # Correct answer - green
                btn.configure(
                    fg_color=self.colors["correct_green"],
                    text_color="white",
                    border_color=self.colors["correct_green"]
                )
            elif i == self.selected_answer and i != self.correct_answer_index:
                # Wrong answer selected - red
                btn.configure(
                    fg_color=self.colors["incorrect_red"],
                    text_color="white",
                    border_color=self.colors["incorrect_red"]
                )
            else:
                # Other options - gray out
                btn.configure(
                    fg_color="#F5F5F5",
                    border_color="#E0E0E0",
                    text_color="#999999"
                )
        
        # Notify controller with time spent on this question
        self.controller.submit_answer(self.selected_answer, self.question_time)
    
    def on_next_button_clicked(self):
        """Handle next button click"""
        if self.answer_submitted:
            # Move to next question
            self.controller.next_question()
        elif self.selected_answer is not None:
            # Submit current answer
            self.submit_answer()
    
    def update_question(self, question_data, current_question, total_questions, category_name):
        # Reset state
        self.selected_answer = None
        self.answer_submitted = False
        
        # FIX: Handle both "answer" and "correct_answer" keys
        if "answer" in question_data:
            self.correct_answer_index = question_data["answer"]
        elif "correct_answer" in question_data:
            self.correct_answer_index = question_data["correct_answer"]
        else:
            # Fallback if no correct answer key found
            print(f"ERROR: No correct answer key found. Keys: {list(question_data.keys())}")
            self.correct_answer_index = 0
        
        # Start timer for this question
        self.start_question_timer()
        
        # Update display
        self.category_label.configure(text=category_name)
        self.progress_label.configure(text=f"Question {current_question} of {total_questions}")
        
        # Update question text
        question_text = question_data["question"]
        font_size = self.adjust_font_size(question_text)
        self.question_label.configure(
            text=question_text,
            font=("Arial", font_size)
        )
        
        # Update options
        for i, option in enumerate(question_data["options"]):
            btn = self.answer_buttons[i]
            btn.configure(
                text=option,
                fg_color=self.colors["white"],
                text_color=self.colors["text_primary"],
                border_color=self.colors["neutral_gray"],
                state="normal",
                hover_color=self.colors["neutral_gray"]
            )
        
        # Update next button text
        if current_question == total_questions:
            self.next_button.configure(text="Finish Quiz")
        else:
            self.next_button.configure(text="Next")
    
    def start_question_timer(self):
        """Start timing the current question"""
        self.question_start_time = time.time()
        self.question_time = 0
        self.update_timer_display()
    
    def stop_question_timer(self):
        """Stop timing the current question"""
        if self.question_start_time:
            self.question_time = int(time.time() - self.question_start_time)
            self.question_start_time = 0
    
    def update_timer_display(self):
        """Update the timer display"""
        if self.question_start_time:
            current_time = int(time.time() - self.question_start_time)
            self.timer_label.configure(text=f"{current_time}s")
            self.after(1000, self.update_timer_display)
    
    def start_quiz_timer(self):
        """Start the overall quiz timer"""
        self.quiz_start_time = time.time()
    
    def get_total_quiz_time(self):
        """Get total time spent on quiz"""
        if self.quiz_start_time:
            return int(time.time() - self.quiz_start_time)
        return self.total_quiz_time
    
    def show_answer_feedback(self, selected_index, correct_index):
        """Show feedback for submitted answer (called by controller)"""
        self.answer_submitted = True
        
        for i, btn in enumerate(self.answer_buttons):
            btn.configure(state="disabled")
            if i == correct_index:
                # Correct answer - green
                btn.configure(
                    fg_color=self.colors["correct_green"],
                    text_color="white",
                    border_color=self.colors["correct_green"]
                )
            elif i == selected_index:
                # User's answer - red if wrong
                btn.configure(
                    fg_color=self.colors["incorrect_red"],
                    text_color="white",
                    border_color=self.colors["incorrect_red"]
                )
    
    def show_correct_answer_only(self, correct_index):
        """Show only the correct answer"""
        self.answer_submitted = True
        
        for btn in self.answer_buttons:
            btn.configure(state="disabled")
        
        self.answer_buttons[correct_index].configure(
            fg_color=self.colors["correct_green"],
            text_color="white",
            border_color=self.colors["correct_green"]
        )
    
    def reset_for_next_question(self):
        """Reset for the next question"""
        self.selected_answer = None
        self.answer_submitted = False
        
        for btn in self.answer_buttons:
            btn.configure(
                fg_color=self.colors["white"],
                text_color=self.colors["text_primary"],
                border_color=self.colors["neutral_gray"],
                state="normal",
                hover_color=self.colors["neutral_gray"]
            )