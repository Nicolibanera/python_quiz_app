# controller.py
from view import *
from model import QuizModel

class QuizController:
    def __init__(self, root):
        self.root = root
        self.model = QuizModel()
        self.sound_manager = SoundManager(self.root)
        
        self.setup_window()
        self.create_views()
        self.show_main_menu()
    
    def setup_window(self):
        """Setup the main window"""
        self.root.title("PyQuiz - Python Quiz Application")
        self.root.geometry("800x600")
        self.root.configure(bg='#1c2333')
        
        # Set window icon
        try:
            self.root.iconbitmap("pictures/brain.ico")
        except:
            pass  # Silently fail if icon not found
    
    def create_views(self):
        """Create all view components"""
        self.views = {}
        
        # Main menu
        self.views['main'] = MainMenuView(self.root, self, self.sound_manager)
        
        # Category menus with hardcoded subjects as per specifications
        self.views['fundamentals'] = FundamentalsMenuView(self.root, self, self.sound_manager)
        self.views['intermediate'] = IntermediateMenuView(self.root, self, self.sound_manager)
        self.views['databases'] = DatabasesMenuView(self.root, self, self.sound_manager)
        self.views['advanced'] = AdvancedMenuView(self.root, self, self.sound_manager)
        
        # Question and result views
        self.views['question'] = QuestionView(self.root, self, self.sound_manager)
        self.views['result'] = ResultView(self.root, self, self.sound_manager)
        self.views['history'] = HistoryView(self.root, self, self.sound_manager)
    
    def show_view(self, view_name):
        """Show a specific view"""
        for view in self.views.values():
            view.pack_forget()
        
        self.views[view_name].pack(fill='both', expand=True)
    
    def show_main_menu(self):
        """Show main menu"""
        self.show_view('main')
    
    def show_fundamentals(self):
        """Show fundamentals menu"""
        self.show_view('fundamentals')
    
    def show_intermediate(self):
        """Show intermediate menu"""
        self.show_view('intermediate')
    
    def show_databases(self):
        """Show databases menu"""
        self.show_view('databases')
    
    def show_advanced(self):
        """Show advanced menu"""
        self.show_view('advanced')
    
    def show_history(self):
        """Show history menu"""
        self.views['history'].display_history(self.model.get_quiz_history())
        self.show_view('history')
    
    def start_quiz(self, category, subject):
        """Start a new quiz for given category and subject"""
        total_questions = self.model.start_quiz(category, subject)
        
        if total_questions == 0:
            from tkinter import messagebox
            messagebox.showwarning("No Questions", f"No questions available for {subject}.")
            return
        
        self.show_question()
    
    def show_question(self):
        """Show current question"""
        question_data = self.model.get_current_question()
        
        if question_data:
            self.views['question'].display_question(
                question_data,
                self.model.current_question_index,
                len(self.model.current_questions)
            )
            self.show_view('question')
        else:
            self.show_result()
    
    def next_question(self):
        """Process answer and move to next question"""
        selected_answer = self.views['question'].get_selected_answer()
        
        if not selected_answer:
            from tkinter import messagebox
            messagebox.showwarning("No Answer", "Please select an answer before continuing.")
            return
        
        is_correct, correct_answer = self.model.submit_answer(selected_answer)
        
        # Play appropriate sound
        if is_correct:
            self.sound_manager.play_sound('correct')
        else:
            self.sound_manager.play_sound('wrong')
        
        # Show next question or results
        if self.model.current_question_index < len(self.model.current_questions):
            self.show_question()
        else:
            self.show_result()
    
    def show_result(self):
        """Show quiz results"""
        score = self.model.score
        total = len(self.model.current_questions)
        level = self.model.calculate_level()
        
        self.views['result'].display_result(
            score, total, level,
            self.model.current_category,
            self.model.current_subject
        )
        
        self.show_view('result')