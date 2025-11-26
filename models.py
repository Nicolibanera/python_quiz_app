class User:
    def __init__(self):
        self.name = ""
        self.score = 0
        self.current_category = ""
    
    def set_name(self, name):
        self.name = name.strip()
    
    def get_name(self):
        return self.name
    
    def set_category(self, category):
        self.current_category = category
    
    def get_category(self):
        return self.current_category

class QuizModel:
    def __init__(self):
        self.user = User()
        self.categories = [
            "Fundamentals",
            "Intermediate Concepts", 
            "Databases & Standard Libraries",
            "File Formats, APIs & Advanced Python"
        ]