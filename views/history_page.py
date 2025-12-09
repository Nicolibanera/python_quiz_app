import customtkinter as ctk
from PIL import Image, ImageTk
import json
import os
import datetime
from collections import defaultdict

class HistoryPageView(ctk.CTkFrame):
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
            "accent_gold": "#ECB45E",
            "neutral_beige": "#C1BBB3",
            "button_primary": "#22223B",
            "button_secondary": "#F4EDE2",
            "podium_gold": "#FFD700",
            "podium_silver": "#C0C0C0",
            "podium_bronze": "#CD7F32"
        }
        
        # Data storage
        self.history_file = "quiz_history.json"
        self.history_data = self.load_history()
        self.current_tab = "All Scores"
        
        self.configure(fg_color=self.colors["soft_beige"], corner_radius=0)
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color=self.colors["soft_beige"])
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors["dark_navy"],
            height=80,
            corner_radius=0
        )
        header_frame.pack(fill="x", pady=0, padx=0)
        header_frame.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header_frame, fg_color=self.colors["dark_navy"])
        header_content.pack(expand=True, fill="both", padx=30)
        
        header_label = ctk.CTkLabel(
            header_content,
            text="Best Scores",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        header_label.pack(side="left")
        
        # Back button in header
        back_button = ctk.CTkButton(
            header_content,
            text="← Back",
            font=("Arial", 12),
            width=80,
            height=30,
            corner_radius=15,
            fg_color="transparent",
            hover_color="#3A3A5D",
            text_color="white",
            border_width=1,
            border_color="white",
            command=self.on_home
        )
        back_button.pack(side="right")
        
        # Content
        content_frame = ctk.CTkFrame(main_frame, fg_color=self.colors["soft_beige"])
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Tabs
        tabs_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["soft_beige"])
        tabs_frame.pack(fill="x", pady=(0, 20))
        
        self.tabs = []
        self.underlines = []
        tab_names = ["All Scores", "Last 30 Days", "Top 10"]
        
        for i, tab_name in enumerate(tab_names):
            tab_frame = ctk.CTkFrame(tabs_frame, fg_color=self.colors["soft_beige"])
            tab_frame.pack(side="left", padx=(0, 20))
            
            tab_label = ctk.CTkLabel(
                tab_frame,
                text=tab_name,
                font=("Arial", 14, "bold" if i == 0 else "normal"),
                text_color=self.colors["text_primary"] if i == 0 else self.colors["text_secondary"],
                cursor="hand2"
            )
            tab_label.pack()
            
            # Underline
            underline = ctk.CTkFrame(
                tab_frame,
                fg_color=self.colors["text_primary"] if i == 0 else "transparent",
                height=3,
                corner_radius=0
            )
            underline.pack(fill="x", pady=(2, 0))
            self.underlines.append(underline)
            
            tab_label.bind("<Button-1>", lambda e, idx=i: self.activate_tab(idx))
            self.tabs.append(tab_label)
        
        # Podium section
        self.podium_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["soft_beige"])
        self.podium_frame.pack(fill="x", pady=(0, 25))
        
        # Score list header
        list_header = ctk.CTkLabel(
            content_frame,
            text="Recent Scores",
            font=("Arial", 16, "bold"),
            text_color=self.colors["text_primary"],
            anchor="w"
        )
        list_header.pack(anchor="w", pady=(0, 10))
        
        # Scrollable list
        list_container = ctk.CTkFrame(content_frame, fg_color=self.colors["soft_beige"])
        list_container.pack(fill="both", expand=True)
        
        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            list_container,
            fg_color=self.colors["soft_beige"],
            scrollbar_button_color=self.colors["neutral_beige"],
            scrollbar_button_hover_color=self.colors["text_secondary"]
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["soft_beige"])
        nav_frame.pack(fill="x", pady=(20, 0))
        
        home_button = ctk.CTkButton(
            nav_frame,
            text="← Home",
            font=("Arial", 14),
            height=40,
            width=120,
            corner_radius=12,
            fg_color=self.colors["button_secondary"],
            hover_color=self.colors["white"],
            text_color=self.colors["text_primary"],
            border_width=1,
            border_color=self.colors["neutral_beige"],
            command=self.on_home
        )
        home_button.pack(side="left", padx=(0, 10))
        
        play_button = ctk.CTkButton(
            nav_frame,
            text="Play Again",
            font=("Arial", 14, "bold"),
            height=40,
            corner_radius=12,
            fg_color=self.colors["button_primary"],
            hover_color=self.colors["text_secondary"],
            text_color="white",
            command=self.on_play_again
        )
        play_button.pack(side="right")
        
        # Load initial data
        self.refresh_data()
    
    def load_history(self):
        """Load quiz history from JSON file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_history(self):
        """Save quiz history to JSON file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history_data, f, indent=2, default=str)
        except IOError:
            print("Warning: Could not save history data")
    
    def add_quiz_result(self, player_name, category, score, total, answer_history):
        """Add a new quiz result to history"""
        quiz_result = {
            'id': len(self.history_data) + 1,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'player_name': player_name,
            'category': category,
            'score': score,
            'total': total,
            'percentage': (score / total * 100) if total > 0 else 0,
            'answer_history': answer_history
        }
        
        self.history_data.append(quiz_result)
        self.save_history()
        return quiz_result
    
    def get_filtered_data(self):
        """Get data filtered by current tab"""
        if not self.history_data:
            return []
        
        now = datetime.datetime.now()
        
        if self.current_tab == "All Scores":
            return sorted(self.history_data, key=lambda x: x['date'], reverse=True)
        
        elif self.current_tab == "Last 30 Days":
            thirty_days_ago = now - datetime.timedelta(days=30)
            filtered = [
                result for result in self.history_data
                if datetime.datetime.strptime(result['date'], "%Y-%m-%d %H:%M") >= thirty_days_ago
            ]
            return sorted(filtered, key=lambda x: x['date'], reverse=True)
        
        elif self.current_tab == "Top 10":
            # Get top 10 by percentage
            sorted_data = sorted(self.history_data, key=lambda x: x['percentage'], reverse=True)
            return sorted_data[:10]
        
        return []
    
    def get_podium_data(self):
        """Get top 3 scores for podium"""
        if not self.history_data:
            return []
        
        # Group by player and get best score per player
        player_best = {}
        for result in self.history_data:
            player = result['player_name']
            percentage = result['percentage']
            if player not in player_best or percentage > player_best[player]['percentage']:
                player_best[player] = result
        
        # Get top 3 players
        top_players = sorted(player_best.values(), key=lambda x: x['percentage'], reverse=True)[:3]
        
        podium_data = []
        for i, player in enumerate(top_players):
            podium_data.append({
                "rank": str(i + 1),
                "score": f"{int(player['percentage'])}%",
                "player_name": player['player_name'],
                "initial": player['player_name'][0].upper() if player['player_name'] else "?",
                "category": player['category']
            })
        
        return podium_data
    
    def refresh_data(self):
        """Refresh all displayed data"""
        # Clear existing content
        for widget in self.podium_frame.winfo_children():
            widget.destroy()
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get filtered data
        filtered_data = self.get_filtered_data()
        
        # Update podium
        podium_data = self.get_podium_data()
        if podium_data:
            self.create_podium_section(podium_data)
        else:
            # Show placeholder if no data
            no_data_label = ctk.CTkLabel(
                self.podium_frame,
                text="No scores yet. Play a quiz to see results here!",
                font=("Arial", 14),
                text_color=self.colors["text_secondary"]
            )
            no_data_label.pack(pady=20)
        
        # Update score list
        if filtered_data:
            for result in filtered_data:
                self.add_score_entry(result)
        else:
            # Show placeholder if no data
            no_scores_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No scores found for this filter.",
                font=("Arial", 14),
                text_color=self.colors["text_secondary"]
            )
            no_scores_label.pack(pady=20)
    
    def create_podium_section(self, podium_data):
        """Create podium with top 3 scores"""
        podium_colors = [
            self.colors["podium_silver"],  # 2nd place
            self.colors["podium_gold"],    # 1st place
            self.colors["podium_bronze"]   # 3rd place
        ]
        
        for i, data in enumerate(podium_data):
            height_factors = [0.9, 1.0, 0.8]
            base_height = 120
            
            card_frame = ctk.CTkFrame(
                self.podium_frame,
                fg_color=self.colors["white"],
                height=int(base_height * height_factors[i]),
                corner_radius=15,
                border_width=1,
                border_color=self.colors["neutral_beige"]
            )
            
            if i == 1:  # 1st place (center)
                card_frame.pack(side="left", expand=True, fill="y", padx=5)
            else:
                card_frame.pack(side="left", expand=True, fill="y", padx=5, pady=(20, 0))
            
            card_frame.pack_propagate(False)
            
            content_frame = ctk.CTkFrame(card_frame, fg_color=self.colors["white"])
            content_frame.pack(expand=True, fill="both", padx=15, pady=15)
            
            # Crown icon for 1st place
            if i == 1:
                crown_label = ctk.CTkLabel(
                    content_frame,
                    text="👑",
                    font=("Arial", 20),
                    text_color=self.colors["podium_gold"]
                )
                crown_label.pack(pady=(0, 5))
            
            # Rank
            rank_label = ctk.CTkLabel(
                content_frame,
                text=f"#{data['rank']}",
                font=("Arial", 18, "bold"),
                text_color=self.colors["text_primary"]
            )
            rank_label.pack(pady=(0, 10))
            
            # Avatar
            avatar_size = 50 if i == 1 else 40
            
            avatar_frame = ctk.CTkFrame(
                content_frame,
                fg_color=self.get_avatar_color(data['initial']),
                width=avatar_size,
                height=avatar_size,
                corner_radius=avatar_size//2
            )
            avatar_frame.pack(pady=(0, 10))
            avatar_frame.pack_propagate(False)
            
            initial_label = ctk.CTkLabel(
                avatar_frame,
                text=data['initial'],
                font=("Arial", 18, "bold"),
                text_color="white"
            )
            initial_label.pack(expand=True)
            
            # Player name
            name_label = ctk.CTkLabel(
                content_frame,
                text=data['player_name'],
                font=("Arial", 12),
                text_color=self.colors["text_secondary"],
                wraplength=80
            )
            name_label.pack(pady=(0, 5))
            
            # Score
            score_label = ctk.CTkLabel(
                content_frame,
                text=data['score'],
                font=("Arial", 14, "bold"),
                text_color=podium_colors[i]
            )
            score_label.pack()
            
            # Category
            category_label = ctk.CTkLabel(
                content_frame,
                text=data['category'],
                font=("Arial", 10),
                text_color=self.colors["text_secondary"]
            )
            category_label.pack(pady=(5, 0))
    
    def add_score_entry(self, result):
        """Add a score entry to the list"""
        entry_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=self.colors["white"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["neutral_beige"]
        )
        entry_frame.pack(fill="x", pady=5, padx=5)
        
        content_frame = ctk.CTkFrame(entry_frame, fg_color=self.colors["white"])
        content_frame.pack(fill="both", expand=True, padx=15, pady=12)
        
        left_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["white"])
        left_frame.pack(side="left", fill="y")
        
        # Rank (based on percentage)
        rank = self.calculate_rank(result['percentage'])
        rank_label = ctk.CTkLabel(
            left_frame,
            text=f"#{rank}",
            font=("Arial", 16, "bold"),
            text_color=self.colors["text_primary"],
            width=30
        )
        rank_label.pack(side="left", padx=(0, 15))
        
        # Avatar
        avatar_frame = ctk.CTkFrame(
            left_frame,
            fg_color=self.get_avatar_color(result['player_name'][0].upper() if result['player_name'] else "?"),
            width=35,
            height=35,
            corner_radius=35//2
        )
        avatar_frame.pack(side="left")
        avatar_frame.pack_propagate(False)
        
        initial_label = ctk.CTkLabel(
            avatar_frame,
            text=result['player_name'][0].upper() if result['player_name'] else "?",
            font=("Arial", 12, "bold"),
            text_color="white"
        )
        initial_label.pack(expand=True)
        
        # Middle section
        middle_frame = ctk.CTkFrame(content_frame, fg_color=self.colors["white"])
        middle_frame.pack(side="left", fill="both", expand=True, padx=(15, 0))
        
        # Player name and date
        name_date_label = ctk.CTkLabel(
            middle_frame,
            text=f"{result['player_name']} • {result['date']}",
            font=("Arial", 12),
            text_color=self.colors["text_primary"],
            anchor="w"
        )
        name_date_label.pack(anchor="w")
        
        # Category
        category_label = ctk.CTkLabel(
            middle_frame,
            text=result['category'],
            font=("Arial", 11),
            text_color=self.colors["text_secondary"],
            anchor="w"
        )
        category_label.pack(anchor="w", pady=(2, 0))
        
        # Score details
        details_label = ctk.CTkLabel(
            middle_frame,
            text=f"{result.get('score', 0)}/{result.get('total', 10)} correct",
            font=("Arial", 11),
            text_color=self.colors["text_secondary"],
            anchor="w"
        )
        details_label.pack(anchor="w", pady=(2, 0))
        
        # Score pill with percentage
        percentage = result['percentage']
        score_color = self.get_score_color(percentage)
        
        score_pill = ctk.CTkFrame(
            content_frame,
            fg_color=score_color,
            corner_radius=10
        )
        score_pill.pack(side="right")
        
        score_label = ctk.CTkLabel(
            score_pill,
            text=f"{percentage:.0f}%",
            font=("Arial", 12, "bold"),
            text_color="white",
            padx=15,
            pady=5
        )
        score_label.pack()
    
    def calculate_rank(self, percentage):
        """Calculate rank based on percentage"""
        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 50:
            return "D"
        else:
            return "E"
    
    def get_avatar_color(self, initial):
        """Get color for avatar based on initial"""
        colors = {
            'A': '#FF6B6B', 'B': '#4ECDC4', 'C': '#FFD166', 'D': '#06D6A0',
            'E': '#118AB2', 'F': '#9D4EDD', 'G': '#F15BB5', 'H': '#FF9F1C',
            'I': '#2EC4B6', 'J': '#E71D36', 'K': '#011627', 'L': '#FD9F6D',
            'M': '#C5D86D', 'N': '#F7EF99', 'O': '#1B998B', 'P': '#ED217C',
            'Q': '#2D3047', 'R': '#419D78', 'S': '#E0A458', 'T': '#D33F49',
            'U': '#D7CDCC', 'V': '#59C9A5', 'W': '#FF6666', 'X': '#5B6C5D',
            'Y': '#2A2D43', 'Z': '#8D6A9F'
        }
        return colors.get(initial.upper(), '#4A4E69')
    
    def get_score_color(self, percentage):
        """Get color for score based on percentage"""
        if percentage >= 90:
            return self.colors["podium_gold"]
        elif percentage >= 80:
            return "#FFB347"  # Orange
        elif percentage >= 70:
            return "#4ECDC4"  # Teal
        elif percentage >= 60:
            return "#45B7D1"  # Blue
        elif percentage >= 50:
            return "#96CEB4"  # Green
        else:
            return "#FF6B6B"  # Red
    
    def activate_tab(self, index):
        """Activate a tab and update display"""
        self.current_tab = ["All Scores", "Last 30 Days", "Top 10"][index]
        
        # Update tab appearance
        for i, (tab, underline) in enumerate(zip(self.tabs, self.underlines)):
            is_active = (i == index)
            tab.configure(
                font=("Arial", 14, "bold" if is_active else "normal"),
                text_color=self.colors["text_primary"] if is_active else self.colors["text_secondary"]
            )
            underline.configure(fg_color=self.colors["text_primary"] if is_active else "transparent")
        
        # Update controller
        if index == 0:
            self.controller.on_all_scores()
        elif index == 1:
            self.controller.on_last_30_days()
        elif index == 2:
            self.controller.on_top_10()
        
        # Refresh data for this tab
        self.refresh_data()
    
    def update_history_data(self, new_data=None):
        """Update history data from controller"""
        if new_data:
            self.history_data = new_data
            self.save_history()
        self.refresh_data()
    
    # Controller callbacks
    def on_all_scores(self):
        self.controller.on_all_scores()
    
    def on_last_30_days(self):
        self.controller.on_last_30_days()
    
    def on_top_10(self):
        self.controller.on_top_10()
    
    def on_home(self):
        self.controller.on_home()
    
    def on_play_again(self):
        self.controller.on_play_again()