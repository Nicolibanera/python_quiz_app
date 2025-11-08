# view.py
import tkinter as tk
from tkinter import ttk, messagebox

class SoundManager:
    def __init__(self, root):
        self.root = root
    
    def play_sound(self, sound_type):
        if sound_type == 'click':
            self.root.bell()
        elif sound_type == 'correct':
            self.root.bell()
            self.root.after(100, self.root.bell)
        elif sound_type == 'wrong':
            self.root.bell()
            self.root.after(200, self.root.bell)

class BaseView(tk.Frame):
    def __init__(self, parent, controller, sound_manager):
        super().__init__(parent)
        self.controller = controller
        self.sound_manager = sound_manager
        
        self.colors = {
            'bg_dark': '#1c2333',
            'bg_medium': '#2e3a59',
            'accent': '#ff8c32',
            'text_light': '#ffffff',
            'text_muted': '#a9b4c2'
        }
        
        self.configure(bg=self.colors['bg_dark'])
        self.setup_fonts()
    
    def setup_fonts(self):
        try:
            self.title_font = ('Segoe UI', 24, 'bold')
            self.heading_font = ('Segoe UI', 18, 'bold')
            self.normal_font = ('Segoe UI', 12)
            self.small_font = ('Segoe UI', 10)
        except:
            self.title_font = ('Arial', 24, 'bold')
            self.heading_font = ('Arial', 18, 'bold')
            self.normal_font = ('Arial', 12)
            self.small_font = ('Arial', 10)
    
    def create_button(self, parent, text, command, width=20, height=2):
        button = tk.Button(
            parent,
            text=text,
            command=lambda: self.button_click(command),
            font=self.normal_font,
            bg=self.colors['bg_medium'],
            fg=self.colors['text_light'],
            activebackground=self.colors['accent'],
            activeforeground=self.colors['text_light'],
            relief='flat',
            width=width,
            height=height,
            cursor='hand2'
        )
        return button
    
    def button_click(self, command):
        self.sound_manager.play_sound('click')
        command()

class MainMenuView(BaseView):
    def __init__(self, parent, controller, sound_manager):
        super().__init__(parent, controller, sound_manager)
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self, bg=self.colors['bg_dark'])
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        title_label = tk.Label(
            main_frame,
            text="PyQuiz",
            font=self.title_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light']
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Test your programming knowledge",
            font=self.small_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_muted']
        )
        subtitle_label.pack(pady=(0, 30))
        
        instruction_label = tk.Label(
            main_frame,
            text="Choose a category to start",
            font=self.normal_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light']
        )
        instruction_label.pack(pady=(0, 20))
        
        categories = [
            ("Fundamental", self.controller.show_fundamentals),
            ("Intermediate Concepts", self.controller.show_intermediate),
            ("Databases & Standard Libraries", self.controller.show_databases),
            ("File formats, API & Advanced Python", self.controller.show_advanced)
        ]
        
        for category_text, command in categories:
            button = self.create_button(main_frame, category_text, command, width=40)
            button.pack(pady=10, fill='x')
        
        history_button = self.create_button(main_frame, "History", self.controller.show_history, width=40)
        history_button.pack(pady=(40, 10), fill='x')

class CategoryMenuView(BaseView):
    def __init__(self, parent, controller, sound_manager, title, subjects):
        super().__init__(parent, controller, sound_manager)
        self.title_text = title
        self.subjects = subjects
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self, bg=self.colors['bg_dark'])
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        title_label = tk.Label(
            main_frame,
            text=self.title_text,
            font=self.title_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light']
        )
        title_label.pack(pady=(0, 30))
        
        # Create a grid frame for buttons
        grid_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        grid_frame.pack(expand=True, fill='both')
        
        # Arrange buttons in 2 columns
        row, col = 0, 0
        max_cols = 2
        
        for subject in self.subjects:
            button = self.create_button(
                grid_frame, 
                subject, 
                lambda s=subject: self.controller.start_quiz(self.title_text, s),
                width=25,
                height=2
            )
            button.grid(row=row, column=col, padx=10, pady=8, sticky='ew')
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Configure grid weights for proper spacing
        for i in range(max_cols):
            grid_frame.grid_columnconfigure(i, weight=1)
        
        back_button = self.create_button(main_frame, "Back", self.controller.show_main_menu, width=25)
        back_button.pack(pady=(40, 10))

class FundamentalsMenuView(CategoryMenuView):
    def __init__(self, parent, controller, sound_manager):
        subjects = ["Intro", "Basics", "Data Type", "Control Flow", "Functions I", "Functions II", "Data Structure"]
        super().__init__(parent, controller, sound_manager, "Fundamental", subjects)

class IntermediateMenuView(CategoryMenuView):
    def __init__(self, parent, controller, sound_manager):
        subjects = ["Collection", "Exception", "File Handling", "PathLib", "PDM", "OOP I", "OOP II"]
        super().__init__(parent, controller, sound_manager, "Intermediate Concepts", subjects)

class DatabasesMenuView(CategoryMenuView):
    def __init__(self, parent, controller, sound_manager):
        subjects = ["MySQL", "MongoDB", "Math Random", "Datetime", "OS Sys Platform", "Arrays & Heapq", "Bisects & Collections", "Functools", "GUI"]
        super().__init__(parent, controller, sound_manager, "Databases & Standard Libraries", subjects)

class AdvancedMenuView(CategoryMenuView):
    def __init__(self, parent, controller, sound_manager):
        subjects = ["CSV & Excel", "JSON", "API", "Gen & Yields", "Comprehension", "Context Managers", "Modules Packaging"]
        super().__init__(parent, controller, sound_manager, "File formats, API & Advanced Python", subjects)

class QuestionView(BaseView):
    def __init__(self, parent, controller, sound_manager):
        super().__init__(parent, controller, sound_manager)
        self.selected_answer = tk.StringVar()
        self.answer_buttons = []
        self.create_widgets()
    
    def create_widgets(self):
        self.main_frame = tk.Frame(self, bg=self.colors['bg_dark'])
        self.main_frame.pack(expand=True, fill='both', padx=50, pady=30)
        
        self.progress_label = tk.Label(
            self.main_frame,
            text="",
            font=self.small_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_muted']
        )
        self.progress_label.pack(anchor='w', pady=(0, 20))
        
        self.question_label = tk.Label(
            self.main_frame,
            text="",
            font=self.normal_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light'],
            wraplength=600,
            justify='left'
        )
        self.question_label.pack(fill='x', pady=(0, 30))
        
        self.answers_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        self.answers_frame.pack(fill='x', pady=(0, 30))
        
        self.next_button = self.create_button(
            self.main_frame, 
            "Next", 
            self.controller.next_question,
            width=15
        )
        self.next_button.pack()
        self.next_button.config(state='disabled')
    
    def display_question(self, question_data, current_index, total_questions):
        self.progress_label.config(text=f"Question {current_index + 1} of {total_questions}")
        self.question_label.config(text=question_data['question'])
        
        for button in self.answer_buttons:
            button.destroy()
        self.answer_buttons = []
        
        for i, option in enumerate(question_data['options']):
            button = tk.Radiobutton(
                self.answers_frame,
                text=option,
                variable=self.selected_answer,
                value=option,
                font=self.normal_font,
                bg=self.colors['bg_dark'],
                fg=self.colors['text_light'],
                selectcolor=self.colors['bg_medium'],
                activebackground=self.colors['bg_dark'],
                activeforeground=self.colors['text_light'],
                cursor='hand2',
                command=self.enable_next_button
            )
            button.pack(anchor='w', pady=5)
            self.answer_buttons.append(button)
        
        self.selected_answer.set("")
        self.next_button.config(state='disabled')
    
    def enable_next_button(self):
        self.next_button.config(state='normal')
    
    def get_selected_answer(self):
        return self.selected_answer.get()

class ResultView(BaseView):
    def __init__(self, parent, controller, sound_manager):
        super().__init__(parent, controller, sound_manager)
        self.create_widgets()
    
    def create_widgets(self):
        self.main_frame = tk.Frame(self, bg=self.colors['bg_dark'])
        self.main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        self.title_label = tk.Label(
            self.main_frame,
            text="",
            font=self.title_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light']
        )
        self.title_label.pack(pady=(0, 20))
        
        self.message_label = tk.Label(
            self.main_frame,
            text="",
            font=self.normal_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light']
        )
        self.message_label.pack(pady=(0, 10))
        
        self.score_label = tk.Label(
            self.main_frame,
            text="",
            font=self.heading_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['accent']
        )
        self.score_label.pack(pady=(0, 10))
        
        self.level_label = tk.Label(
            self.main_frame,
            text="",
            font=self.heading_font,
            bg=self.colors['bg_dark'],
            fg='gold'
        )
        self.level_label.pack(pady=(0, 20))
        
        self.additional_message_label = tk.Label(
            self.main_frame,
            text="",
            font=self.normal_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_muted']
        )
        self.additional_message_label.pack(pady=(0, 30))
        
        retry_button = self.create_button(
            self.main_frame, 
            "Take another quiz", 
            self.controller.show_main_menu,
            width=25
        )
        retry_button.pack()
    
    def display_result(self, score, total, level, category, subject):
        percentage = (score / total) * 100
        
        if percentage >= 70:
            self.title_label.config(text="Congratulations! 🎉")
            self.additional_message_label.config(text="Check if you're as good in other areas")
        elif percentage >= 50:
            self.title_label.config(text="Sigh 🤔")
            self.additional_message_label.config(text="Could do better")
        else:
            self.title_label.config(text="Aww 😔")
            self.additional_message_label.config(text="You could try again")
        
        self.score_label.config(text=f"You scored: {score}/{total} ({percentage:.1f}%)")
        self.level_label.config(text=f"Level: {level}")
        self.message_label.config(text=f"Category: {category} - {subject}")

class HistoryView(BaseView):
    def __init__(self, parent, controller, sound_manager):
        super().__init__(parent, controller, sound_manager)
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self, bg=self.colors['bg_dark'])
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        title_label = tk.Label(
            main_frame,
            text="Quiz History",
            font=self.title_font,
            bg=self.colors['bg_dark'],
            fg=self.colors['text_light']
        )
        title_label.pack(pady=(0, 30))
        
        history_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        history_frame.pack(fill='both', expand=True)
        
        self.history_text = tk.Text(
            history_frame,
            wrap=tk.WORD,
            width=60,
            height=15,
            font=self.small_font,
            bg=self.colors['bg_medium'],
            fg=self.colors['text_light'],
            state='disabled'
        )
        
        scrollbar = tk.Scrollbar(history_frame, orient='vertical', command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        
        self.history_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        back_button = self.create_button(main_frame, "Back", self.controller.show_main_menu, width=20)
        back_button.pack(pady=(20, 10))
    
    def display_history(self, history):
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        
        if not history:
            self.history_text.insert(tk.END, "No history yet.")
        else:
            for i, record in enumerate(reversed(history)):
                self.history_text.insert(tk.END, 
                    f"{i+1}. {record['category']} - {record['subject']} - "
                    f"{record['score']}/{record['total']} - {record['level']}\n"
                    f"   Date: {record['date']}\n\n"
                )
        
        self.history_text.config(state='disabled')