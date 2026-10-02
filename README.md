# Chess Game Using Alpha-Beta Pruning

A basic Python implementation of a chess game that applies the **Minimax algorithm with Alpha-Beta Pruning** using the **python-chess** library to demonstrate adversarial search and decision-making in game-playing AI.

---

## Overview
This project allows a human player to play chess against an AI opponent.  
The AI evaluates possible moves using Minimax with Alpha-Beta Pruning and selects optimal moves based on a simple material-based heuristic.

---

## Key Features
- Human vs AI chess gameplay
- Minimax algorithm with Alpha-Beta Pruning
- Material-based board evaluation
- Adjustable search depth
- Console-based interaction

---

## Tech Stack
- Python
- python-chess
- Streamlit
- Minimax with Alpha-Beta Pruning

## Run the Streamlit app

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

Push this repository to GitHub, then create an app at [share.streamlit.io](https://share.streamlit.io/) using the repository's branch and `app.py` as the main file. Streamlit installs the dependencies from `requirements.txt`.

---

## How It Works
The player enters moves in standard chess notation.  
The AI explores possible game states using Alpha-Beta Pruning and selects the best move based on heuristic evaluation.

---

