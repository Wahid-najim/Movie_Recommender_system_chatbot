Movie Recommender Chatbot
Movie Chatbot GUI
![image](https://github.com/user-attachments/assets/f65c1655-3a0a-4f6b-a025-4e6efac7a0ae)

A Python-based movie recommender chatbot with a sleek Tkinter GUI. This chatbot provides movie recommendations based on a hardcoded dataset, using content-based filtering with genres, descriptions, years, and ratings. It supports natural language input and features a modern, dark-themed interface.
Features
Content-Based Recommendations: Suggests movies similar to a given title or filtered by genre, year, or rating.
Natural Language Interaction: Responds to greetings, help requests, and recommendation queries with varied phrasing.
Flexible Filtering: Supports queries like "sci-fi movies after 2000" or "movies with rating above 8.5".
Professional GUI: Dark-themed interface with color-coded chat (teal for bot, yellow for user) and a responsive design.
Sample Dataset: Includes 15 popular movies with titles, genres, descriptions, years, and ratings.
Prerequisites
Python 3.7+
Installation
Clone the Repository:
bash
git clone https://github.com/yourusername/movie-recommender-chatbot.git
cd movie-recommender-chatbot
Install Dependencies:
bash
pip install pandas scikit-learn
Note: Tkinter comes with Python by default.
Usage
Run the Application:
bash
python movie_chatbot.py
Interact with the Chatbot:
Launch the GUI and start chatting!
Example inputs:
"Hi" (triggers a greeting)
"Movies like The Matrix" (recommends similar movies)
"Recommend sci-fi movies" (filters by genre)
"Movies after 2000" (filters by year)
"Recommend movies with rating above 8.5" (filters by rating)
"Help" (shows usage examples)
View Recommendations:
Recommendations appear in the chat with movie details (title, year, genre, rating).
