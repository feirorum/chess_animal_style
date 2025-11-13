#!/usr/bin/env python3
"""Test script to verify checkmate and stalemate detection"""

import sys
from unittest.mock import MagicMock

# Mock pygame to avoid initialization issues
sys.modules['pygame'] = MagicMock()
sys.modules['pygame.mixer'] = MagicMock()

from chess_logic import ChessGame

def test_stalemate():
    """Test a simple stalemate scenario"""
    game = ChessGame()

    # Create a stalemate position
    # Clear the board first
    game.board = [[None for _ in range(8)] for _ in range(8)]

    # Set up a stalemate position:
    # Black king on h7, White king on h5, Black queen on g5
    # White king cannot move (all squares attacked or occupied)
    game.board[2][7] = {'type': 'king', 'color': 'black'}  # h6
    game.board[3][7] = {'type': 'king', 'color': 'white'}  # h5
    game.board[3][6] = {'type': 'queen', 'color': 'black'}  # g5

    game.king_positions = {'white': (3, 7), 'black': (2, 7)}
    game.current_player = 'white'

    # Check for stalemate
    is_stalemate = game.is_stalemate('white')
    is_check = game.is_in_check('white')
    is_checkmate = game.is_checkmate('white')

    # Check what moves the king has
    king_moves = game.get_valid_moves(7, 0)

    print("Test Stalemate Scenario:")
    print(f"  Position: White King a1, Black Queen c2, Black King c1")
    print(f"  White King available moves: {king_moves}")
    print(f"  White in check: {is_check}")
    print(f"  White in checkmate: {is_checkmate}")
    print(f"  White in stalemate: {is_stalemate}")

    if is_stalemate and not is_check and not is_checkmate:
        print("  ✓ Stalemate detection works correctly!")
        return True
    else:
        print("  ✗ Stalemate detection failed!")
        return False

def test_checkmate():
    """Test a simple checkmate scenario"""
    game = ChessGame()

    # Clear the board
    game.board = [[None for _ in range(8)] for _ in range(8)]

    # Set up a checkmate position (back rank mate):
    # White king on h1, Black rook on h8 (giving check), Black king on f7
    game.board[7][7] = {'type': 'king', 'color': 'white'}  # h1
    game.board[0][7] = {'type': 'rook', 'color': 'black'}  # h8 (gives check)
    game.board[1][5] = {'type': 'king', 'color': 'black'}  # f7
    # Add white pawns to block escape
    game.board[6][6] = {'type': 'pawn', 'color': 'white'}  # g2
    game.board[6][7] = {'type': 'pawn', 'color': 'white'}  # h2

    game.king_positions = {'white': (7, 7), 'black': (1, 5)}
    game.current_player = 'white'

    # Check for checkmate
    is_checkmate = game.is_checkmate('white')
    is_check = game.is_in_check('white')
    is_stalemate = game.is_stalemate('white')

    # Check what moves the king has
    king_moves = game.get_valid_moves(7, 7)

    print("\nTest Checkmate Scenario:")
    print(f"  Position: White King h1, Black Rook h8, White Pawns g2 h2")
    print(f"  White King available moves: {king_moves}")
    print(f"  White in check: {is_check}")
    print(f"  White in checkmate: {is_checkmate}")
    print(f"  White in stalemate: {is_stalemate}")

    if is_checkmate and is_check and not is_stalemate:
        print("  ✓ Checkmate detection works correctly!")
        return True
    else:
        print("  ✗ Checkmate detection failed!")
        return False

def test_normal_position():
    """Test that a normal position is neither checkmate nor stalemate"""
    game = ChessGame()

    # Use the starting position
    game.current_player = 'white'

    is_checkmate = game.is_checkmate('white')
    is_stalemate = game.is_stalemate('white')
    is_check = game.is_in_check('white')

    print("\nTest Normal Starting Position:")
    print(f"  White in check: {is_check}")
    print(f"  White in checkmate: {is_checkmate}")
    print(f"  White in stalemate: {is_stalemate}")

    if not is_checkmate and not is_stalemate and not is_check:
        print("  ✓ Normal position detected correctly!")
        return True
    else:
        print("  ✗ Normal position test failed!")
        return False

if __name__ == "__main__":
    print("=== Testing Chess Endgame Detection ===\n")

    test1 = test_stalemate()
    test2 = test_checkmate()
    test3 = test_normal_position()

    print("\n=== Test Results ===")
    if test1 and test2 and test3:
        print("All tests passed! ✓")
    else:
        print("Some tests failed! ✗")
