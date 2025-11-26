import tkinter as tk
from models import QuizModel
from views.page1_view import Page1View
from views.page2_view import Page2View

class QuizController:
    def __init__(self, root):
        self.root = root
        self.model = QuizModel()
        self.current_view = None
        
        # Initializing the viewpages
        self.page1 = Page1View(root, self)
        self.page2 = Page2View(root, self)
        
    def run(self):
        self.show_page1()
    
    def show_page1(self):
        self._hide_all_views()
        self.page1.pack(fill=tk.BOTH, expand=True)
        self.current_view = self.page1
    
    def show_page2(self, user_name):
        self.model.user.set_name(user_name)
        self._hide_all_views()
        self.page2.pack(fill=tk.BOTH, expand=True)
        self.current_view = self.page2
    
    def select_category(self, category):
        self.model.user.set_category(category)
        print(f"User: {self.model.user.get_name()}")
        print(f"Selected category: {category}")
        # Here we would show the quiz questions page
        # For now,I'll just print the selection
    
    def _hide_all_views(self):
        for view in [self.page1, self.page2]:
            view.pack_forget()