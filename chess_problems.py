# -*- coding: utf-8 -*-
"""Chess problems suitable for 8-year-olds"""

# Each problem has:
# - title: Swedish name of the problem
# - objective: What the player needs to achieve (in Swedish)
# - difficulty: 'easy', 'medium', or 'hard'
# - player_color: 'white' or 'black' (which color the player controls)
# - board: Initial board setup
# - solution_moves: List of moves that solve the problem (for hints/validation)
# - max_moves: Maximum number of moves to solve (None = unlimited)

CHESS_PROBLEMS = [
    {
        'id': 'checkmate_1',
        'title': 'Ta Kungen!',
        'objective': 'Gör schackmatt på ett drag',
        'difficulty': 'easy',
        'player_color': 'white',
        'max_moves': 1,
        'hint': 'Damen kan göra schackmatt!',
        'board': [
            # Row 0 (8)
            [{'type': 'king', 'color': 'black'}, None, None, None, None, None, None, {'type': 'rook', 'color': 'black'}],
            # Row 1 (7)
            [{'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None, None, None, None, None, None],
            # Row 2 (6)
            [None, None, None, None, None, None, None, None],
            # Row 3 (5)
            [None, None, None, None, None, None, None, None],
            # Row 4 (4)
            [None, None, None, None, None, None, None, None],
            # Row 5 (3)
            [None, None, None, None, None, None, None, None],
            # Row 6 (2)
            [None, None, None, None, None, None, None, None],
            # Row 7 (1)
            [None, None, None, None, None, None, None, {'type': 'queen', 'color': 'white'}]
        ],
        'king_positions': {'white': None, 'black': (0, 0)},  # No white king in this puzzle
        'solution_hint': 'Flytta damen till a8'
    },

    {
        'id': 'checkmate_2',
        'title': 'Tornen samarbetar',
        'objective': 'Gör schackmatt på två drag',
        'difficulty': 'easy',
        'player_color': 'white',
        'max_moves': 2,
        'hint': 'Använd båda tornen för att fånga kungen!',
        'board': [
            # Row 0 (8)
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            # Row 1 (7)
            [None, None, None, None, None, None, None, None],
            # Row 2 (6)
            [None, None, None, None, None, None, None, None],
            # Row 3 (5)
            [None, None, None, None, None, None, None, None],
            # Row 4 (4)
            [None, None, None, None, None, None, None, None],
            # Row 5 (3)
            [None, None, None, None, None, None, None, None],
            # Row 6 (2)
            [None, None, None, None, None, None, None, {'type': 'rook', 'color': 'white'}],
            # Row 7 (1)
            [None, None, None, None, None, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': None, 'black': (0, 4)},
        'solution_hint': 'Flytta ett torn till e7, sedan det andra till e8'
    },

    {
        'id': 'escape_check',
        'title': 'Fly från schack',
        'objective': 'Ta dig ur schack',
        'difficulty': 'easy',
        'player_color': 'white',
        'max_moves': 1,
        'hint': 'Flytta din kung till säkerheten!',
        'board': [
            # Row 0 (8)
            [None, None, None, None, None, None, None, {'type': 'rook', 'color': 'black'}],
            # Row 1 (7)
            [None, None, None, None, None, None, None, None],
            # Row 2 (6)
            [None, None, None, None, None, None, None, None],
            # Row 3 (5)
            [None, None, None, None, None, None, None, None],
            # Row 4 (4)
            [None, None, None, None, None, None, None, None],
            # Row 5 (3)
            [None, None, None, None, None, None, None, None],
            # Row 6 (2)
            [None, None, None, None, None, None, None, None],
            # Row 7 (1)
            [None, None, None, None, None, None, None, {'type': 'king', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 7), 'black': None},
        'solution_hint': 'Flytta kungen åt sidan, bort från tornet'
    },

    {
        'id': 'fork_attack',
        'title': 'Dubbelt hot',
        'objective': 'Attackera kung och torn samtidigt',
        'difficulty': 'medium',
        'player_color': 'white',
        'max_moves': 1,
        'hint': 'Springaren kan attackera två pjäser samtidigt!',
        'board': [
            # Row 0 (8)
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            # Row 1 (7)
            [None, None, None, None, None, None, None, None],
            # Row 2 (6)
            [None, None, None, None, None, None, {'type': 'rook', 'color': 'black'}, None],
            # Row 3 (5)
            [None, None, None, None, None, None, None, None],
            # Row 4 (4)
            [None, None, None, None, {'type': 'knight', 'color': 'white'}, None, None, None],
            # Row 5 (3)
            [None, None, None, None, None, None, None, None],
            # Row 6 (2)
            [None, None, None, None, None, None, None, None],
            # Row 7 (1)
            [None, None, None, None, None, None, None, None]
        ],
        'king_positions': {'white': None, 'black': (0, 4)},
        'solution_hint': 'Springaren till f6 eller d6 attackerar både kung och torn'
    },

    {
        'id': 'pawn_promotion',
        'title': 'Bonden blir dam',
        'objective': 'Befordra bonden och gör schackmatt',
        'difficulty': 'medium',
        'player_color': 'white',
        'max_moves': 2,
        'hint': 'Gör bonden till en dam först!',
        'board': [
            # Row 0 (8)
            [{'type': 'king', 'color': 'black'}, None, None, None, None, None, None, None],
            # Row 1 (7)
            [None, {'type': 'pawn', 'color': 'white'}, None, None, None, None, None, None],
            # Row 2 (6)
            [None, None, None, None, None, None, None, None],
            # Row 3 (5)
            [None, None, None, None, None, None, None, None],
            # Row 4 (4)
            [None, None, None, None, None, None, None, None],
            # Row 5 (3)
            [None, None, None, None, None, None, None, None],
            # Row 6 (2)
            [None, None, None, None, None, None, None, None],
            # Row 7 (1)
            [None, None, {'type': 'king', 'color': 'white'}, None, None, None, None, None]
        ],
        'king_positions': {'white': (7, 2), 'black': (0, 0)},
        'solution_hint': 'Flytta bonden till b8 och välj dam'
    },

    {
        'id': 'queen_checkmate',
        'title': 'Damen är stark',
        'objective': 'Använd damen för att göra schackmatt',
        'difficulty': 'easy',
        'player_color': 'white',
        'max_moves': 1,
        'hint': 'Damen kan flytta långt och blockera kungen!',
        'board': [
            # Row 0 (8)
            [None, None, None, None, None, None, None, {'type': 'king', 'color': 'black'}],
            # Row 1 (7)
            [None, None, None, None, None, None, {'type': 'pawn', 'color': 'black'}, None],
            # Row 2 (6)
            [None, None, None, None, None, None, None, None],
            # Row 3 (5)
            [None, None, None, None, None, None, None, None],
            # Row 4 (4)
            [None, None, None, None, None, None, None, None],
            # Row 5 (3)
            [None, None, None, None, None, None, None, None],
            # Row 6 (2)
            [None, None, None, None, None, None, None, None],
            # Row 7 (1)
            [{'type': 'queen', 'color': 'white'}, None, None, None, None, None, None, None]
        ],
        'king_positions': {'white': None, 'black': (0, 7)},
        'solution_hint': 'Flytta damen till g7 eller h8'
    },

    {
        'id': 'back_rank_mate',
        'title': 'Grundraden',
        'objective': 'Gör schackmatt på grundraden',
        'difficulty': 'medium',
        'player_color': 'white',
        'max_moves': 1,
        'hint': 'Kungen kan inte fly - bonderna blockerar!',
        'board': [
            # Row 0 (8)
            [None, None, None, None, None, {'type': 'king', 'color': 'black'}, None, None],
            # Row 1 (7)
            [None, None, None, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None],
            # Row 2 (6)
            [None, None, None, None, None, None, None, None],
            # Row 3 (5)
            [None, None, None, None, None, None, None, None],
            # Row 4 (4)
            [None, None, None, None, None, None, None, None],
            # Row 5 (3)
            [None, None, None, None, None, None, None, None],
            # Row 6 (2)
            [None, None, None, None, None, None, None, None],
            # Row 7 (1)
            [None, None, None, None, None, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': None, 'black': (0, 5)},
        'solution_hint': 'Flytta tornet till f8'
    },
]
