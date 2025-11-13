# Animal Chess Game

A fun, cartoon-style chess game where pieces are represented as animals!

## Piece Mapping
- **Queen** = Cat (with crown)
- **King** = Dog (with crown)
- **Knight** = Horse
- **Pawn** = Duckling
- **Bishop** = Blobfish
- **Rook** = Book

## Features
- 2-player local chess game
- Drag and drop piece movement
- Visual indicators for valid moves
- Full chess rules including:
  - Check and checkmate detection
  - Castling (kingside and queenside)
  - En passant
  - Move validation with helpful error messages
- Sound effects for check and winning (when audio files are present)
- Bright, fun animal-themed background

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python main.py
```

## How to Play

1. White moves first
2. Click and drag a piece to move it
3. Valid move squares will be highlighted in green when you select a piece
4. If you try an invalid move, a popup will explain why
5. The game enforces all standard chess rules

## Optional: Adding Sound Effects

To enable sound effects, add the following WAV files to the `assets/sounds/` directory:
- `check.wav` - Played when a check occurs
- `win.wav` - Played when checkmate occurs

You can create these sounds or download them from free sound effect websites.

## Controls

- **Left Mouse Button**: Click and drag to move pieces
- **Close Window**: Exit the game

Enjoy your animal chess adventure!
