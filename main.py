import tkinter as tk
from tkinter import scrolledtext, ttk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import random

# Expanded movie data (could be loaded from a CSV in a real application)
movie_data = {
    'title': ['The Matrix', 'Inception', 'Interstellar', 'The Dark Knight', 'Pulp Fiction',
              'Fight Club', 'The Godfather', 'Forrest Gump', 'The Shawshank Redemption', 'Titanic',
              'Avatar', 'The Avengers', 'Jurassic Park', 'The Lion King', 'Star Wars: A New Hope'],
    'genre': ['Sci-Fi Action', 'Sci-Fi Thriller', 'Sci-Fi Drama', 'Action Crime', 'Crime Drama',
              'Drama Thriller', 'Crime Drama', 'Drama Romance', 'Drama', 'Romance Drama',
              'Sci-Fi Adventure', 'Action Sci-Fi', 'Sci-Fi Adventure', 'Animation Drama', 'Sci-Fi Adventure'],
    'description': [
        'A hacker discovers a simulated reality and fights against machines.',
        'A thief enters dreams to steal secrets and uncovers layered realities.',
        'Astronauts travel through a wormhole to find a new home for humanity.',
        'A vigilante battles a psychopathic criminal in Gotham City.',
        'Interconnected stories of crime and redemption unfold.',
        'An insomniac forms an underground fight club with a mysterious stranger.',
        'A powerful mafia family faces betrayal and power struggles.',
        'A man with a low IQ experiences key historical events.',
        'Two prisoners form a bond over years seeking redemption.',
        'A tragic love story unfolds aboard a doomed ship.',
        'A marine explores a lush alien world and fights for its survival.',
        'Superheroes team up to save Earth from an alien invasion.',
        'Scientists recreate dinosaurs, leading to chaos on an island.',
        'A young lion prince flees after his father’s murder and returns to reclaim his throne.',
        'A farm boy joins a rebellion against an evil empire in a galaxy far away.'
    ],
    'year': [1999, 2010, 2014, 2008, 1994, 1999, 1972, 1994, 1994, 1997, 2009, 2012, 1993, 1994, 1977],
    'rating': [8.7, 8.8, 8.6, 9.0, 8.9, 8.8, 9.2, 8.8, 9.3, 7.8, 7.9, 8.0, 7.9, 8.5, 8.6]
}

# Create DataFrame
movies_df = pd.DataFrame(movie_data)

# Preprocess data for recommendation
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_df['genre'] + " " + movies_df['description'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get movie recommendations
def get_recommendations(movie_title=None, genre=None, min_year=None, min_rating=None, num_recommendations=3):
    filtered_df = movies_df.copy()
    
    if movie_title:
        movie_title = movie_title.lower().strip()
        if movie_title not in filtered_df['title'].str.lower().values:
            return f"Sorry, I couldn't find '{movie_title}' in my database. Try another movie!"
        idx = filtered_df[filtered_df['title'].str.lower() == movie_title].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        movie_indices = [i[0] for i in sim_scores[1:]]  # Exclude the movie itself
        filtered_df = filtered_df.iloc[movie_indices]
    
    if genre:
        filtered_df = filtered_df[filtered_df['genre'].str.lower().str.contains(genre.lower())]
    if min_year:
        filtered_df = filtered_df[filtered_df['year'] >= min_year]
    if min_rating:
        filtered_df = filtered_df[filtered_df['rating'] >= min_rating]
    
    if filtered_df.empty:
        return "Sorry, no movies match your criteria. Try adjusting your request!"
    
    recommendations = filtered_df.sample(min(num_recommendations, len(filtered_df)))
    return "Here are your movie recommendations:\n" + "\n".join(
        f"- {row['title']} ({row['year']}) - {row['genre']} (Rating: {row['rating']})"
        for _, row in recommendations.iterrows()
    )

# Chatbot response logic
def chatbot_response(user_input):
    user_input = user_input.lower().strip()
    
    # Greetings
    greetings = ['hi', 'hello', 'hey']
    if any(greet in user_input for greet in greetings):
        return random.choice([
            "Hi there! Ready to find some great movies?",
            "Hello! I'm your movie guru. What’s on your mind?",
            "Hey! Let’s talk movies—what do you want to watch?"
        ])
    
    # Recommendation request detection
    patterns = {
        'like_movie': r'(?:recommend|movies\s+like|similar.*to|based.*on)\s+(.+)',
        'genre': r'recommend.*(?:in|for)\s+(.+?)(?:\s+genre|\s+movies|$)',
        'year': r'recommend.*after\s+(\d{4})',
        'rating': r'recommend.*rating.*above\s+(\d\.?\d?)'
    }
    
    params = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, user_input)
        if match:
            if key == 'like_movie':
                params['movie_title'] = match.group(1).strip()
            elif key == 'genre':
                params['genre'] = match.group(1).strip()
            elif key == 'year':
                params['min_year'] = int(match.group(1))
            elif key == 'rating':
                params['min_rating'] = float(match.group(1))
    
    if params:
        return get_recommendations(**params)
    
    # Help message
    if 'help' in user_input:
        return ("I can recommend movies! Try:\n"
                "- 'Movies like The Matrix'\n"
                "- 'Recommend sci-fi movies'\n"
                "- 'Movies after 2000'\n"
                "- 'Recommend movies with rating above 8.5'")
    
    # Default response
    return random.choice([
        "Not sure what you mean. Want some movie ideas? Ask me anything!",
        "I’m here to help with movie picks. Try 'movies like Inception' or 'sci-fi recommendations'!",
        "Hmm, let’s find you a movie. What are you in the mood for?"
    ])

# Professional Tkinter GUI
class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommender Chatbot")
        self.root.geometry("600x700")
        self.root.configure(bg="#2c3e50")  # Dark blue background

        # Style configuration
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=5)
        style.configure("TLabel", font=("Helvetica", 14, "bold"), background="#2c3e50", foreground="#ecf0f1")

        # Header
        self.header = ttk.Label(root, text="Movie Recommender Chatbot", style="TLabel")
        self.header.pack(pady=10)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=60, height=30, font=("Helvetica", 11),
            bg="#34495e", fg="#ecf0f1", insertbackground="white"
        )
        self.chat_display.pack(padx=20, pady=10)

        # Input frame
        self.input_frame = tk.Frame(root, bg="#2c3e50")
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.input_field = tk.Entry(
            self.input_frame, width=45, font=("Helvetica", 12),
            bg="#ecf0f1", fg="#2c3e50", relief="flat"
        )
        self.input_field.pack(side=tk.LEFT, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = ttk.Button(
            self.input_frame, text="Send", command=self.send_message, style="TButton"
        )
        self.send_button.pack(side=tk.LEFT)

        # Initial greeting
        self.chat_display.insert(tk.END, "Chatbot: Hi there! Ready to find some great movies?\n")
        self.chat_display.tag_config("bot", foreground="#1abc9c")  # Teal for bot messages
        self.chat_display.tag_config("user", foreground="#f1c40f")  # Yellow for user messages

    def send_message(self, event=None):
        user_message = self.input_field.get().strip()
        if user_message:
            # Display user message
            self.chat_display.insert(tk.END, f"You: {user_message}\n", "user")
            # Get and display chatbot response
            response = chatbot_response(user_message)
            self.chat_display.insert(tk.END, f"Chatbot: {response}\n", "bot")
            # Clear input field
            self.input_field.delete(0, tk.END)
            # Auto-scroll to bottom
            self.chat_display.see(tk.END)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()