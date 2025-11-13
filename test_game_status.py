#!/usr/bin/env python3
"""
Test script for game status detection
Tests various endgame scenarios to ensure the game correctly identifies:
- Ongoing games
- Checkmate (white won / black won)
- Stalemate (draw)
- King captured (special mode)
"""

import sys
import os
from chess_logic import ChessGame, GameOptions

def create_stalemate_board():
    """Create a board in stalemate position (white to move, no legal moves, not in check)"""
    game = ChessGame()
    # Clear the board
    game.board = [[None for _ in range(8)] for _ in range(8)]

    # Stalemate position:
    # White king at a1 (row=7, col=0)
    game.board[7][0] = {'type': 'king', 'color': 'white'}
    game.king_positions['white'] = (7, 0)

    # Black king at b3 (row=5, col=1) - controls a2 (6,0), a3 (5,0), a4 (4,0), b2 (6,1), b1 (7,1), b4 (4,1), c2 (6,2), c3 (5,2), c4 (4,2)
    game.board[5][1] = {'type': 'king', 'color': 'black'}
    game.king_positions['black'] = (5, 1)

    # Black queen at c1 (row=7, col=2) - on same row as white king
    # Gives check? No wait, same row means it controls b1 (7,1) and attacks a1 (7,0)!
    # Let me place queen elsewhere...

    # Black rook at a2... no that gives check vertically.
    # Black rook at b1 - that occupies (7,1), blocks it from white king
    game.board[7][1] = {'type': 'rook', 'color': 'black'}

    # Now white king at a1 (7,0) cannot move to:
    # (7,1) = b1 - occupied by black rook
    # (6,0) = a2 - controlled by black king at (5,1)
    # (6,1) = b2 - controlled by black king at (5,1)
    # And white king is NOT in check because no piece attacks (7,0)

    # White's turn - NOT in check but no legal moves = STALEMATE
    game.current_player = 'white'

    return game

def create_checkmate_board():
    """Create a board in checkmate position (white checkmated, black wins)"""
    game = ChessGame()
    # Clear the board
    game.board = [[None for _ in range(8)] for _ in range(8)]

    # White king in corner (7,7), will be in check from queen
    game.board[7][7] = {'type': 'king', 'color': 'white'}
    game.king_positions['white'] = (7, 7)

    # Black queen at (7,5) - gives check to white king on same row
    game.board[7][5] = {'type': 'queen', 'color': 'black'}

    # Black king at (5,6) - controls escape squares (6,6), (6,7)
    game.board[5][6] = {'type': 'king', 'color': 'black'}
    game.king_positions['black'] = (5, 6)

    # Black rook at (6,5) - protects the queen and controls (7,5)
    game.board[6][5] = {'type': 'rook', 'color': 'black'}

    # This is checkmate: white king is in check from queen and cannot escape
    # (7,6) - still in check from queen
    # (6,7) - controlled by black king
    # (6,6) - controlled by black king
    # Can't capture queen at (7,5) because it's protected by rook at (6,5)

    # White's turn (in checkmate)
    game.current_player = 'white'

    return game

def create_ongoing_board():
    """Create a normal ongoing game board"""
    game = ChessGame()
    # Use default starting position
    return game

def create_check_but_not_mate_board():
    """Create a board where white is in check but can escape"""
    game = ChessGame()
    # Clear the board
    game.board = [[None for _ in range(8)] for _ in range(8)]

    # White king in center, in check but can move
    game.board[4][4] = {'type': 'king', 'color': 'white'}
    game.king_positions['white'] = (4, 4)

    # Black rook checking white king
    game.board[4][0] = {'type': 'rook', 'color': 'black'}

    # Black king
    game.board[0][0] = {'type': 'king', 'color': 'black'}
    game.king_positions['black'] = (0, 0)

    # White's turn (in check but can escape)
    game.current_player = 'white'

    return game

def test_stalemate_detection():
    """Test stalemate detection in normal mode"""
    print("\n=== Test 1: Stalemate Detection (Normal Mode) ===")
    options = GameOptions()
    options.capture_king_on_checkmate = False  # Normal mode

    game = create_stalemate_board()
    game.options = options

    print("Board setup: White king trapped in corner, no legal moves, not in check")
    print(f"Current player: {game.current_player}")
    print(f"Is in check: {game.is_in_check('white')}")
    print(f"Has valid moves: {game.has_any_valid_moves('white')}")
    print(f"Is stalemate: {game.is_stalemate('white')}")

    # Debug: show valid moves for white king
    white_king_moves = game.get_valid_moves(0, 0)
    print(f"White king valid moves: {white_king_moves}")

    # Debug: show all white pieces on board
    white_pieces = []
    for row in range(8):
        for col in range(8):
            piece = game.board[row][col]
            if piece and piece['color'] == 'white':
                moves = game.get_valid_moves(row, col)
                white_pieces.append(f"  {piece['type']} at ({row},{col}): {len(moves)} moves = {moves}")
    print("All white pieces:")
    for p in white_pieces:
        print(p)

    # Check game status
    game.check_game_status()
    print(f"\nGame status: {game.game_status}")
    print(f"Game result: {game.game_result}")

    if game.game_status == 'finished' and game.game_result == 'draw':
        print("✓ PASS: Stalemate correctly detected as draw")
        return True
    else:
        print("✗ FAIL: Stalemate not detected")
        return False

def test_checkmate_detection():
    """Test checkmate detection in normal mode"""
    print("\n=== Test 2: Checkmate Detection (Normal Mode) ===")
    options = GameOptions()
    options.capture_king_on_checkmate = False  # Normal mode

    game = create_checkmate_board()
    game.options = options

    print("Board setup: White king checkmated by two black rooks")
    print(f"Current player: {game.current_player}")
    print(f"Is in check: {game.is_in_check('white')}")
    print(f"Has valid moves: {game.has_any_valid_moves('white')}")
    print(f"Is checkmate: {game.is_checkmate('white')}")

    # Check game status
    game.check_game_status()
    print(f"\nGame status: {game.game_status}")
    print(f"Game result: {game.game_result}")

    if game.game_status == 'finished' and game.game_result == 'black_won':
        print("✓ PASS: Checkmate correctly detected, black wins")
        return True
    else:
        print("✗ FAIL: Checkmate not detected correctly")
        return False

def test_ongoing_game():
    """Test that a normal ongoing game is detected correctly"""
    print("\n=== Test 3: Ongoing Game Detection ===")
    options = GameOptions()
    options.capture_king_on_checkmate = False  # Normal mode

    game = create_ongoing_board()
    game.options = options

    print("Board setup: Starting position")
    print(f"Current player: {game.current_player}")
    print(f"Is in check: {game.is_in_check('white')}")
    print(f"Has valid moves: {game.has_any_valid_moves('white')}")

    # Check game status
    game.check_game_status()
    print(f"\nGame status: {game.game_status}")
    print(f"Game result: {game.game_result}")

    if game.game_status == 'ongoing' and game.game_result is None:
        print("✓ PASS: Ongoing game correctly detected")
        return True
    else:
        print("✗ FAIL: Ongoing game not detected correctly")
        return False

def test_check_but_not_mate():
    """Test that check without mate is detected as ongoing"""
    print("\n=== Test 4: Check But Not Checkmate ===")
    options = GameOptions()
    options.capture_king_on_checkmate = False  # Normal mode

    game = create_check_but_not_mate_board()
    game.options = options

    print("Board setup: White king in check but can escape")
    print(f"Current player: {game.current_player}")
    print(f"Is in check: {game.is_in_check('white')}")
    print(f"Has valid moves: {game.has_any_valid_moves('white')}")
    print(f"Is checkmate: {game.is_checkmate('white')}")

    # Check game status
    game.check_game_status()
    print(f"\nGame status: {game.game_status}")
    print(f"Game result: {game.game_result}")

    if game.game_status == 'ongoing' and game.game_result is None:
        print("✓ PASS: Check (but not mate) correctly detected as ongoing")
        return True
    else:
        print("✗ FAIL: Game status incorrect for check position")
        return False

def test_stalemate_special_mode():
    """Test that stalemate is NOT detected as draw in special mode"""
    print("\n=== Test 5: Stalemate in Special Mode (Should be Ongoing) ===")
    options = GameOptions()
    options.capture_king_on_checkmate = True  # Special mode

    game = create_stalemate_board()
    game.options = options

    print("Board setup: White king trapped, but in SPECIAL MODE")
    print(f"Current player: {game.current_player}")
    print(f"Is in check: {game.is_in_check('white')}")
    print(f"Has valid moves: {game.has_any_valid_moves('white')}")

    # Check game status
    game.check_game_status()
    print(f"\nGame status: {game.game_status}")
    print(f"Game result: {game.game_result}")

    if game.game_status == 'ongoing':
        print("✓ PASS: In special mode, stalemate doesn't end game (can pass)")
        return True
    else:
        print("✗ FAIL: Special mode should allow game to continue")
        return False

def test_save_load_stalemate():
    """Test that loading a saved game with stalemate correctly detects the draw"""
    print("\n=== Test 6: Save and Load Stalemate Game ===")

    # Ensure games directory exists
    if not os.path.exists('games'):
        os.makedirs('games')

    # Create and save a stalemate game
    options = GameOptions()
    options.capture_king_on_checkmate = False  # Normal mode

    game = create_stalemate_board()
    game.options = options
    game.check_game_status()

    print("Original game:")
    print(f"  Status: {game.game_status}")
    print(f"  Result: {game.game_result}")

    # Save the game
    filepath = game.save_game("test_stalemate")
    print(f"\nSaved game to: {filepath}")

    # Load the game
    loaded_game = ChessGame(options)
    loaded_game.load_game(filepath)

    print("\nLoaded game:")
    print(f"  Status: {loaded_game.game_status}")
    print(f"  Result: {loaded_game.game_result}")
    print(f"  Current player: {loaded_game.current_player}")
    print(f"  Is in check: {loaded_game.is_in_check(loaded_game.current_player)}")
    print(f"  Has valid moves: {loaded_game.has_any_valid_moves(loaded_game.current_player)}")

    # Clean up
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"\nCleaned up test file: {filepath}")

    if loaded_game.game_status == 'finished' and loaded_game.game_result == 'draw':
        print("\n✓ PASS: Loaded game correctly identified as stalemate/draw")
        return True
    else:
        print("\n✗ FAIL: Loaded game not correctly identified")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("GAME STATUS DETECTION TESTS")
    print("=" * 60)

    tests = [
        test_stalemate_detection,
        test_checkmate_detection,
        test_ongoing_game,
        test_check_but_not_mate,
        test_stalemate_special_mode,
        test_save_load_stalemate
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n✗ EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {total - passed} TEST(S) FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
