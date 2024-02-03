# Chess Outline

## Scope and Objectives
  - **Scope:**
    - Develope a playable chess game that opens in ~web browser~ PyGame.
    - This game will not have bot functionality.
    - This will be of modular design as a learning oppurtinity.

## Requirments
  - **Functional Requirments:**
    - Display pieces
    - Move pieces
    - Capture Pieces
    - Check detection
    - Checkmate detection
    - Pinned piece detection
    - Pawn promotion
  - **Non-Functional Requirments:**
    - Piece move annimation
    - Sound
    - Display piece possible moves
    - View previous moves
   
## Project Plan
  ### **Tasks:**
  1. Set up development environemnt
  2. Implement board size and square colors
  3. Add pieces to the board
  4. Implement piece movement
  5. Handle piece capture
  6. Handle check/checkmate
  7. Handle pinned peices
  8. Implement pawn promotion
   
## Technologies and Tools:
  - **Language:**
    - Python
    ~- JavaScript~
  - **Libraries:**
    - Pygame (Python)
    ~- Phaser (JavaScript~

# Classes, Methods and Attributes Outline

- Class Board
  -**Methods**
    - squares - Generates a list of lists for the number of rows and cols
- Class Piece
  - **Attributes:**
    - Color
    - Location
- Class Player
  - **Attributes:**
    - Color
- Class Square
  - **Attributes:**
    - Color
    - Location
- Class Game
- Class GUI
  -**Methods**
    -draw squares - draws a checkered pattern given list of list of points
- Class Move
