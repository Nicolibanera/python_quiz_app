# model.py
import json
import random
import os
from datetime import datetime

class QuizModel:
    def __init__(self):
        self.questions_data = {}
        self.history = []
        self.current_questions = []
        self.current_question_index = 0
        self.score = 0
        self.current_category = ""
        self.current_subject = ""
        
        self.load_questions()
        self.load_history()
    
    def load_questions(self):
        """Load questions from JSON file"""
        try:
            with open('data/questions.json', 'r', encoding='utf-8') as f:
                self.questions_data = json.load(f)
        except Exception as e:
            print(f"Error loading questions: {e}")
            self.questions_data = {}
    
    def load_history(self):
        """Load quiz history from JSON file"""
        try:
            if os.path.exists('data/history.json'):
                with open('data/history.json', 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except Exception:
            self.history = []
    
    def save_history(self):
        """Save quiz history to JSON file"""
        os.makedirs('data', exist_ok=True)
        with open('data/history.json', 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=4)
    
    def get_categories(self):
        return list(self.questions_data.keys())
    
    def get_subjects(self, category):
        return list(self.questions_data.get(category, {}).keys())
    
    def start_quiz(self, category, subject):
        self.current_category = category
        self.current_subject = subject
        self.current_question_index = 0
        self.score = 0
        
        questions = self.questions_data.get(category, {}).get(subject, [])
        random.shuffle(questions)
        self.current_questions = questions[:10]
        
        return len(self.current_questions)
    
    def get_current_question(self):
        if self.current_question_index < len(self.current_questions):
            return self.current_questions[self.current_question_index]
        return None
    
    def submit_answer(self, answer):
        current_question = self.get_current_question()
        if current_question:
            is_correct = answer == current_question["correct_answer"]
            if is_correct:
                self.score += 1
            
            self.current_question_index += 1
            
            if self.current_question_index >= len(self.current_questions):
                self.save_quiz_result()
            
            return is_correct, current_question["correct_answer"]
        return False, ""
    
    def save_quiz_result(self):
        result = {
            "category": self.current_category,
            "subject": self.current_subject,
            "score": self.score,
            "total": len(self.current_questions),
            "percentage": (self.score / len(self.current_questions)) * 100,
            "level": self.calculate_level(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(result)
        self.save_history()
    
    def calculate_level(self):
        percentage = (self.score / len(self.current_questions)) * 100
        if percentage >= 70:
            return "★★★"
        elif percentage >= 50:
            return "★★"
        else:
            return "★"
    
    def get_quiz_history(self):
        return self.history