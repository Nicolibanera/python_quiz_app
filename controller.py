import customtkinter as ctk
from models import QuizModel
from views.page1_view import Page1View
from views.page2_view import Page2View
from views.page3_view import Page3View
from views.results_page import ResultsPageView
from views.history_page import HistoryPageView
from views.review_answers_page import ReviewAnswersPage  # NEW IMPORT
import datetime
import time

class QuizController:
    def __init__(self, root):
        self.root = root
        self.model = QuizModel()
        self.current_view = None
        
        # Time tracking
        self.quiz_start_time = 0
        self.total_quiz_time = 0
        self.question_times = []  # Track time spent on each question
        
        # Set window properties
        self.root.title("PyWizz - Python Quiz App")
        self.root.geometry("400x600")
        
        # Set window icon
        try:
            self.root.iconbitmap("brain.png")
        except:
            pass
        
        # Initialize all views
        self.page1 = Page1View(root, self)
        self.page2 = Page2View(root, self)
        self.page3 = Page3View(root, self)
        self.results_page = ResultsPageView(root, self)
        self.history_page = HistoryPageView(root, self)
        self.review_answers_page = ReviewAnswersPage(root, self)  # NEW VIEW
    
    def run(self):
        """Start the application"""
        self.show_page1()
        self.root.mainloop()
    
    def show_page1(self):
        """Show the welcome page"""
        self._hide_all_views()
        self.page1.pack(fill="both", expand=True)
        self.current_view = self.page1
        
        # Reset time tracking
        self.quiz_start_time = 0
        self.total_quiz_time = 0
        self.question_times = []
    
    def show_page2(self, user_name):
        """Show category selection page"""
        self.model.player.set_name(user_name)
        self._hide_all_views()
        self.page2.pack(fill="both", expand=True)
        self.current_view = self.page2
    
    def select_category(self, category):
        """Handle category selection"""
        self.model.player.set_category(category)
        self.model.player.reset_quiz()
        
        # Reset time tracking for new quiz
        self.quiz_start_time = time.time()
        self.question_times = []
        
        self.show_page3()
    
    def show_page3(self):
        """Show quiz question page"""
        self._hide_all_views()
        self.page3.pack(fill="both", expand=True)
        self.current_view = self.page3
        self.load_current_question()
    
    def load_current_question(self):
        """Load the current question"""
        category = self.model.player.get_category()
        question_data = self.model.get_current_question(category)
        total_questions = self.model.get_total_questions(category)
        current_q = self.model.player.current_question_index + 1
        
        if question_data:
            self.page3.update_question(
                question_data, 
                current_q, 
                total_questions,
                category
            )
        else:
            self.show_results()
    
    def submit_answer(self, selected_index, question_time=None):
        """Handle answer submission"""
        category = self.model.player.get_category()
        question_data = self.model.get_current_question(category)
        
        if question_data:
            # Get correct answer index - handle both "answer" and "correct_answer" keys
            if "answer" in question_data:
                correct_index = question_data["answer"]
            elif "correct_answer" in question_data:
                correct_index = question_data["correct_answer"]
            else:
                # Fallback if no correct answer key found
                print(f"ERROR: No correct answer key found in question data. Keys: {list(question_data.keys())}")
                correct_index = 0
            
            # Track time spent on this question
            if question_time is not None:
                self.question_times.append(question_time)
            
            # Check if answer is correct
            is_correct = self.model.check_answer(category, selected_index)
            
            # DEBUG: Print for troubleshooting
            print(f"Selected: {selected_index}, Correct: {correct_index}, Is correct: {is_correct}")
            
            # Show feedback on the page
            self.page3.show_answer_feedback(selected_index, correct_index)
            
            # Schedule next question after delay
            self.root.after(1500, self.next_question)
    
    def time_expired(self):
        """Handle timer expiration"""
        category = self.model.player.get_category()
        question_data = self.model.get_current_question(category)
        if question_data:
            # Get correct answer index
            if "answer" in question_data:
                correct_index = question_data["answer"]
            elif "correct_answer" in question_data:
                correct_index = question_data["correct_answer"]
            else:
                correct_index = 0
            
            # Record as wrong answer (no selection)
            self.model.check_answer(category, -1)  # -1 indicates no answer
            
            # Track time (use default or calculate)
            current_question_index = self.model.player.current_question_index
            if current_question_index < len(self.question_times):
                # Use existing time if available
                pass
            else:
                # Estimate time (could use a default)
                self.question_times.append(30)  # 30 seconds default
            
            self.page3.show_correct_answer_only(correct_index)
            self.root.after(1500, self.next_question)
    
    def next_question(self):
        """Move to the next question or show results"""
        # Move to next question index
        self.model.next_question()
        
        category = self.model.player.get_category()
        question_data = self.model.get_current_question(category)
        
        if question_data:
            # Reset for next question
            self.page3.reset_for_next_question()
            self.load_current_question()
        else:
            # Quiz finished - show results
            self.show_results()
    
    def show_results(self):
        """Show quiz results page"""
        # Calculate total quiz time
        if self.quiz_start_time:
            self.total_quiz_time = int(time.time() - self.quiz_start_time)
        
        # Fallback: sum of question times if available
        if self.total_quiz_time == 0 and self.question_times:
            self.total_quiz_time = sum(self.question_times)
        
        # Get quiz results
        score_correct = self.model.player.get_score()
        total_questions = self.model.get_total_questions(self.model.player.get_category())
        
        if total_questions == 0:
            # Handle edge case: no questions in category
            print("Error: No questions in category")
            self.show_page2(self.model.player.get_name())
            return
        
        correct_count = score_correct
        wrong_count = total_questions - score_correct
        
        # Format total time
        minutes = self.total_quiz_time // 60
        seconds = self.total_quiz_time % 60
        total_time = f"{minutes}:{seconds:02d}"
        
        # Get result message
        message = self._get_result_message(score_correct, total_questions)
        
        # Save quiz results to history
        quiz_result = self._save_quiz_result(score_correct, total_questions, self.total_quiz_time)
        
        # Update history page with new data
        self.history_page.update_history_data(self.model.quiz_history)
        
        # Show results page
        self._hide_all_views()
        self.results_page.pack(fill="both", expand=True)
        self.current_view = self.results_page
        
        # Update results page with data
        self.results_page.update_results(
            score_correct=score_correct,
            total_questions=total_questions,
            correct_count=correct_count,
            wrong_count=wrong_count,
            total_time=total_time,
            message=message
        )
        
        # Pass answer history for review
        self.results_page.set_answer_history(self.model.get_answer_history())
    
    def show_review_answers(self):
        """Show the review answers page"""
        self._hide_all_views()
        self.review_answers_page.pack(fill="both", expand=True)
        self.current_view = self.review_answers_page
        
        # Get answer history and questions data
        answer_history = self.model.get_answer_history()
        category = self.model.player.get_category()
        
        # Get all questions for the category
        questions_data = self.model.get_all_questions(category)
        
        # Set data for review
        self.review_answers_page.set_answer_data(answer_history, questions_data)
    
    def _save_quiz_result(self, score, total, quiz_time):
        """Save the current quiz result to history"""
        quiz_result = {
            'id': len(self.model.quiz_history) + 1,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'player_name': self.model.player.get_name(),
            'category': self.model.player.get_category(),
            'score': score,
            'total': total,
            'percentage': (score / total * 100) if total > 0 else 0,
            'time_seconds': quiz_time,
            'time_formatted': f"{quiz_time // 60}:{quiz_time % 60:02d}",
            'answer_history': self.model.get_answer_history(),
            'question_times': self.question_times
        }
        self.model.quiz_history.append(quiz_result)
        self.model.save_quiz_history()
        return quiz_result
    
    def show_history(self):
        """Show history page"""
        self._hide_all_views()
        self.history_page.pack(fill="both", expand=True)
        self.current_view = self.history_page
        
        # Get history data from model
        history_data = self.model.quiz_history
        
        if history_data:
            # Format data for display
            formatted_data = []
            for result in history_data:
                formatted_data.append({
                    'date': result['date'],
                    'player_name': result['player_name'],
                    'category': result['category'],
                    'score': f"{result['score']}/{result['total']}",
                    'percentage': result['percentage'],
                    'time': result.get('time_formatted', '0:00')
                })
            
            # Update history page with actual data
            self.history_page.update_history_data(formatted_data)
        else:
            # Show empty state
            self.history_page.update_history_data([])
    
    def _get_result_message(self, score, total):
        """Generate appropriate message based on score"""
        if total == 0:
            return "No questions answered"
        
        percentage = (score / total) * 100
        if percentage == 100:
            return "Perfect Score! 🎯"
        elif percentage >= 90:
            return "Excellent Work! 🌟"
        elif percentage >= 80:
            return "Great Job! 👍"
        elif percentage >= 70:
            return "Good Work! 💪"
        elif percentage >= 60:
            return "Not Bad! 😊"
        elif percentage >= 50:
            return "Keep Practicing! 📚"
        else:
            return "Try Again! 🔄"
    
    # Results page callbacks
    def on_play_again(self):
        """Play again button callback"""
        self.model.player.reset_quiz()
        self.show_page2(self.model.player.get_name())
    
    def on_review_answers(self):
        """Review answers button callback - NEW IMPLEMENTATION"""
        self.show_review_answers()
    
    def on_home(self):
        """Home button callback"""
        self.show_page1()
    
    def on_history(self):
        """History button callback"""
        self.show_history()
    
    def on_back_from_review(self):
        """Go back from review page to results page"""
        self.show_results()
    
    # History page callbacks
    def on_all_scores(self):
        """All Scores tab callback"""
        self.history_page.activate_tab(0)
    
    def on_last_30_days(self):
        """Last 30 Days tab callback"""
        self.history_page.activate_tab(1)
    
    def on_top_10(self):
        """Top 10 tab callback"""
        self.history_page.activate_tab(2)
    
    # Navigation
    def go_back(self):
        """Go back to previous page"""
        if self.current_view == self.page3:
            # Stop any pending timers before going back
            if hasattr(self.page3, 'stop_question_timer'):
                self.page3.stop_question_timer()
            self.show_page2(self.model.player.get_name())
        elif self.current_view == self.results_page:
            self.show_page1()
        elif self.current_view == self.history_page:
            self.show_page2(self.model.player.get_name())
        elif self.current_view == self.review_answers_page:  # NEW
            self.show_results()
    
    def _hide_all_views(self):
        """Hide all views"""
        for view in [self.page1, self.page2, self.page3, 
                    self.results_page, self.history_page, 
                    self.review_answers_page]:  # NEW VIEW ADDED
            view.pack_forget()
    
    def _show_message(self, title, message):
        """Show a message dialog"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Add message
        message_label = ctk.CTkLabel(
            dialog,
            text=message,
            font=("Arial", 14),
            wraplength=250
        )
        message_label.pack(expand=True, padx=20, pady=20)
        
        # Add OK button
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=100
        )
        ok_button.pack(pady=(0, 20))