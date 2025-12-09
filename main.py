import customtkinter as ctk
from controller import QuizController

def main():
    # Set appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Create window
    root = ctk.CTk()
    root.title("PyWizz - Python Quiz App")
    root.geometry("400x700")
    root.resizable(True, True)
    
    # Center window
    window_width = 400
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Initialize app
    app = QuizController(root)
    app.run()
    
    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    main()