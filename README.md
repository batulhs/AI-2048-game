# AI-2048-game
An AI-powered 2048 game uses artificial intelligence to automatically combine numbered tiles on a 4x4 grid, optimizing moves to reach the 2048 tile or achieve the highest possible score. The AI analyzes the board and makes the most strategic moves to maximize results.
# 2048 with AI (Pygame + NumPy)

A clone of the classic **2048 puzzle game**, built with **Pygame** for graphics and **NumPy** for grid operations.  
You can play manually using the arrow keys, or toggle an **AI mode** that plays automatically using a heuristic evaluation strategy.

---

## 📸 Screenshots / Demo
<p align="center">
  <img src="screenshots/gameplay.png" alt="Gameplay Screenshot" width="300"/>
  <!-- You can replace this with an actual GIF if you capture gameplay -->
</p>

---

## 🤖 AI Details
The AI chooses moves by simulating each possible direction and evaluating the resulting grid.  
Its scoring function considers:
- **Empty Cells** → prefers boards with more available moves.  
- **Max Tile in Corner** → rewards keeping the largest tile in a corner.  
- **Smoothness** → penalizes large differences between neighboring tiles.  

This helps the AI survive longer and reach higher tiles.

---

## 🚀 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/2048-AI-Game.git
   cd 2048-AI-Game
