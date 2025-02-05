# Tic-Tac-Toe with Alpha-Beta Pruning

This project implements a Tic-Tac-Toe game powered by **Alpha-Beta Pruning**, a key AI algorithm for optimizing decision-making in games. It offers players a dynamic and interactive experience while simultaneously providing real-time insights into the performance of the AI agent.

## Features

- **Customizable Board Size**: Players can select a board size ranging from **3x3 to 10x10**, making the game scalable and challenging.
- **AI Modes**: Choose between:
  - **Sequential Alpha-Beta Pruning** for smaller boards.
  - **Parallel Alpha-Beta Pruning** for larger boards, leveraging advanced computing for improved performance.
- **Game Data Logging**:
  - After every game session, detailed data is logged, including:
    - `session_id`
    - `board_type` (e.g., 3x3, 5x5)
    - `pruning_type` (Sequential or Parallel)
    - `moves` made during the game
    - `time_taken` for each move
    - `memory_used` by the AI
    - `game_result` (Win/Loss/Draw)
  - This data is automatically stored in a **Google Sheet** for further analysis.
- **Real-Time Data Visualization**:
  - Game session data is visualized in **Google Looker Studio**, providing real-time analytics and insights into the AI agent's performance and efficiency.

## How It Works

1. **Select Game Settings**: Choose the board size and pruning mode (Sequential/Parallel).
2. **Play the Game**: The user plays against the AI, making moves turn by turn.
3. **Log and Visualize Data**: After the game, session details are stored in a Google Sheet and visualized through Looker Studio for real-time performance analysis.

## Purpose

This project demonstrates:
- The practical application of **Alpha-Beta Pruning** in decision-making algorithms.
- The power of **parallelization** in optimizing game-solving for larger grids.
- **Real-time analytics** integration to monitor and evaluate AI performance.

## Tools and Technologies Used

- **Programming Language**: Python
- **AI Algorithm**: Alpha-Beta Pruning (Sequential and Parallel)
- **Data Storage**: Google Sheets API
- **Data Visualization**: Google Looker Studio
- **Parallelization Framework**: CUDA (for Parallel Alpha-Beta Pruning)

## Real-Time Insights

By storing and analyzing data in real-time, this project enables users to observe how different configurations (board size, pruning type) affect:
- AI performance (time and memory efficiency)
- Game outcomes (winning strategies)
- Decision-making speed and accuracy.

This project serves as both an engaging game and a learning platform for understanding AI optimization and real-time analytics.
