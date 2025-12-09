import json
import os

class Player:
    def __init__(self):
        self.name = ""
        self.category = ""
        self.score = 0
        self.current_question_index = 0
    
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_category(self, category):
        self.category = category
    
    def get_category(self):
        return self.category
    
    def get_score(self):
        return self.score
    
    def increment_score(self):
        self.score += 1
    
    def reset_quiz(self):
        self.score = 0
        self.current_question_index = 0
    
    def next_question(self):
        self.current_question_index += 1

class QuizModel:
    def __init__(self):
        self.player = Player()
        self.questions_data = self.load_questions()
        self.quiz_history = self.load_quiz_history()
        self.answer_history = []  # NEW: Store answer history
    
    def load_questions(self):
        try:
            with open('questions.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: questions.json not found")
            return {}
        except json.JSONDecodeError:
            print("Error: Invalid JSON in questions.json")
            return {}
    
    def get_current_question(self, category):
        """Get current question for the selected category"""
        if category in self.questions_data:
            questions = self.questions_data[category]
            if 0 <= self.player.current_question_index < len(questions):
                return questions[self.player.current_question_index]
        return None
    
    def get_all_questions(self, category):
        """Get all questions for a category - NEW METHOD"""
        if category in self.questions_data:
            return self.questions_data[category]
        return []
    
    def get_total_questions(self, category):
        """Get total number of questions for a category"""
        if category in self.questions_data:
            return len(self.questions_data[category])
        return 0
    
    def check_answer(self, category, selected_index):
        """Check if selected answer is correct and update score"""
        current_question = self.get_current_question(category)
        if current_question:
            # Get correct answer index
            if "answer" in current_question:
                correct_index = current_question["answer"]
            elif "correct_answer" in current_question:
                correct_index = current_question["correct_answer"]
            else:
                correct_index = -1
            
            is_correct = selected_index == correct_index
            
            # Update score if correct
            if is_correct and selected_index != -1:
                self.player.increment_score()
            
            # Store answer in history - ENHANCED
            answer_data = {
                "selected_index": selected_index,
                "correct_index": correct_index,
                "is_correct": is_correct,
                "question_index": self.player.current_question_index,
                "question_text": current_question.get("question", ""),
                "options": current_question.get("options", []),
                "explanation": current_question.get("explanation", "")
            }
            
            # Add to history
            self.answer_history.append(answer_data)
            
            return is_correct
        return False
    
    def get_answer_history(self):
        """Get the answer history"""
        return self.answer_history
    
    def next_question(self):
        """Move to next question"""
        self.player.next_question()
    
    def load_quiz_history(self):
        """Load quiz history from file"""
        try:
            with open('quiz_history.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
    
    def save_quiz_history(self):
        """Save quiz history to file"""
        try:
            with open('quiz_history.json', 'w') as f:
                json.dump(self.quiz_history, f, indent=2)
        except Exception as e:
            print(f"Error saving quiz history: {e}")
    
    def clear_answer_history(self):
        """Clear answer history for new quiz"""
        self.answer_history = []