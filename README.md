# Ultimate Tic Tac Toe AI 

This project is a **web-based Ultimate Tic Tac Toe game** built with **Flask (Python)** for the backend and **HTML, CSS, JavaScript** for the frontend. It features an **AI opponent powered by Minimax with Alpha-Beta Pruning**, allowing you to play against the computer or reset the game at any time.

---

# Features

* Play **Ultimate Tic Tac Toe** in your browser.
* Intelligent **AI opponent** with adjustable search depth.
* Real-time move validation and board updates.
* Game state reset functionality.
* Win, tie, and majority-based scoring rules.

---

# Project Structure

```
├── app.py                # Flask server and API routes
├── game_logic.py         # Core game logic and AI implementation
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Client-side game logic
└── __pycache__/          # Compiled Python files
```

---

# Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ultimate-tic-tac-toe-ai.git
   cd ultimate-tic-tac-toe-ai
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install flask
   ```

4. Run the Flask app:

   ```bash
   python app.py
   ```

5. Open the game in your browser:

   ```
   http://127.0.0.1:5000
   ```

---

# AI Logic

* The AI uses **Minimax with Alpha-Beta Pruning** for decision making.
* Evaluation includes:

  * Checking immediate wins and threats.
  * Assessing potential in small and big boards.
  * Simulated win probabilities based on board scores.

---

# Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

## 📜 License

This project is licensed under the **MIT License**.
