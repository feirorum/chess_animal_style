# -*- coding: utf-8 -*-
"""Optimized chess AI engine with 1-10 difficulty levels"""

import random

class ChessAI:
    """Fast chess engine with difficulty levels 1-10"""

    def __init__(self, skill_level=5):
        """
        Initialize the chess AI
        skill_level: 1-10 (1=easiest/fastest, 10=hardest/slowest)
        """
        # Convert old string levels to numeric if needed
        if isinstance(skill_level, str):
            skill_level = {'easy': 3, 'medium': 6, 'hard': 9}.get(skill_level, 5)

        self.skill_level = max(1, min(10, skill_level))

        # Piece values for evaluation (standard chess values)
        self.piece_values = {
            'pawn': 100,
            'knight': 320,
            'bishop': 330,
            'rook': 500,
            'queen': 900,
            'king': 20000
        }

        # Position value tables for better play (scaled down for speed)
        self.position_bonus = {
            'pawn': [
                [0,  0,  0,  0,  0,  0,  0,  0],
                [5,  5,  5,  5,  5,  5,  5,  5],
                [1,  1,  2,  3,  3,  2,  1,  1],
                [0,  0,  1,  2,  2,  1,  0,  0],
                [0,  0,  0,  2,  2,  0,  0,  0],
                [0,  0, -1,  0,  0, -1,  0,  0],
                [0,  0,  0, -2, -2,  0,  0,  0],
                [0,  0,  0,  0,  0,  0,  0,  0]
            ],
            'knight': [
                [-5, -4, -3, -3, -3, -3, -4, -5],
                [-4, -2,  0,  0,  0,  0, -2, -4],
                [-3,  0,  1,  1,  1,  1,  0, -3],
                [-3,  0,  1,  2,  2,  1,  0, -3],
                [-3,  0,  1,  2,  2,  1,  0, -3],
                [-3,  0,  1,  1,  1,  1,  0, -3],
                [-4, -2,  0,  0,  0,  0, -2, -4],
                [-5, -4, -3, -3, -3, -3, -4, -5]
            ]
        }

    def get_best_move(self, game):
        """
        Get the best move based on difficulty level (1-10)
        Level 1-2: Random/mostly random (instant)
        Level 3-4: Simple captures and threats
        Level 5-6: Material evaluation
        Level 7-8: Material + position
        Level 9-10: Full evaluation with lookahead
        """
        all_moves = self.get_all_valid_moves(game, game.current_player)
        if not all_moves:
            return None

        # Level 1: Pure random (fastest)
        if self.skill_level == 1:
            return random.choice(all_moves)

        # Level 2: 80% random, 20% captures
        if self.skill_level == 2:
            if random.random() < 0.2:
                captures = self.get_capture_moves(game, all_moves)
                if captures:
                    return random.choice(captures)
            return random.choice(all_moves)

        # Level 3-4: Prefer captures and checks
        if self.skill_level <= 4:
            return self.get_tactical_move(game, all_moves)

        # Level 5-6: Material evaluation
        if self.skill_level <= 6:
            return self.get_material_move(game, all_moves)

        # Level 7-8: Material + position
        if self.skill_level <= 8:
            return self.get_positional_move(game, all_moves)

        # Level 9-10: Full evaluation
        return self.get_best_evaluated_move(game, all_moves)

    def get_all_valid_moves(self, game, color):
        """Get all valid moves for a given color"""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = game.board[row][col]
                if piece and piece['color'] == color:
                    valid_moves = game.get_valid_moves(row, col)
                    for to_row, to_col in valid_moves:
                        moves.append((row, col, to_row, to_col))
        return moves

    def get_capture_moves(self, game, all_moves):
        """Get all moves that capture pieces"""
        captures = []
        for from_row, from_col, to_row, to_col in all_moves:
            if game.board[to_row][to_col] is not None:
                captures.append((from_row, from_col, to_row, to_col))
        return captures

    def get_tactical_move(self, game, all_moves):
        """Level 3-4: Simple tactical play - captures and checks"""
        # Check for checkmate
        for move in all_moves:
            if self.is_checkmate_move_fast(game, move):
                return move

        # Prefer captures
        captures = self.get_capture_moves(game, all_moves)
        if captures:
            # Pick best capture by piece value
            best_capture = max(captures, key=lambda m: self.piece_values.get(
                game.board[m[2]][m[3]]['type'], 0))
            if random.random() < 0.7:  # 70% take best capture
                return best_capture
            return random.choice(captures)

        # Otherwise random
        return random.choice(all_moves)

    def get_material_move(self, game, all_moves):
        """Level 5-6: Fast material evaluation"""
        scored_moves = []

        for move in all_moves:
            score = self.evaluate_move_fast(game, move)
            scored_moves.append((move, score))

        scored_moves.sort(key=lambda x: x[1], reverse=True)

        # Pick from top 3 moves with some randomness
        top_n = min(3, len(scored_moves))
        if self.skill_level == 6 or random.random() < 0.7:
            return scored_moves[0][0]
        return scored_moves[random.randint(0, top_n-1)][0]

    def get_positional_move(self, game, all_moves):
        """Level 7-8: Material + position evaluation"""
        scored_moves = []

        for move in all_moves:
            score = self.evaluate_move_positional(game, move)
            scored_moves.append((move, score))

        scored_moves.sort(key=lambda x: x[1], reverse=True)

        # Pick best or second best
        if self.skill_level >= 8 or random.random() < 0.8:
            return scored_moves[0][0]
        return scored_moves[min(1, len(scored_moves)-1)][0]

    def get_best_evaluated_move(self, game, all_moves):
        """Level 9-10: Full evaluation with limited lookahead"""
        # Check for immediate checkmate
        for move in all_moves:
            if self.is_checkmate_move_fast(game, move):
                return move

        scored_moves = []
        # Limit moves to evaluate for speed
        moves_to_eval = all_moves
        if len(all_moves) > 20:
            # Pre-filter to best 20 moves using fast evaluation
            quick_scores = [(m, self.evaluate_move_fast(game, m)) for m in all_moves]
            quick_scores.sort(key=lambda x: x[1], reverse=True)
            moves_to_eval = [m for m, _ in quick_scores[:20]]

        for move in moves_to_eval:
            score = self.evaluate_move_deep_optimized(game, move)
            scored_moves.append((move, score))

        scored_moves.sort(key=lambda x: x[1], reverse=True)
        return scored_moves[0][0]

    def evaluate_move_fast(self, game, move):
        """Fast material-only evaluation"""
        from_row, from_col, to_row, to_col = move
        score = 0

        # Capture value
        target = game.board[to_row][to_col]
        if target:
            score += self.piece_values[target['type']]

        # Center control bonus
        if 3 <= to_row <= 4 and 3 <= to_col <= 4:
            score += 20

        return score

    def evaluate_move_positional(self, game, move):
        """Material + simple position evaluation"""
        from_row, from_col, to_row, to_col = move
        score = self.evaluate_move_fast(game, move)

        piece = game.board[from_row][from_col]

        # Position bonus
        if piece['type'] in self.position_bonus:
            bonus_table = self.position_bonus[piece['type']]
            if piece['color'] == 'white':
                score += bonus_table[to_row][to_col] * 2
            else:
                score += bonus_table[7-to_row][to_col] * 2

        # Piece development
        if piece['type'] in ['knight', 'bishop']:
            if (piece['color'] == 'white' and from_row == 7) or \
               (piece['color'] == 'black' and from_row == 0):
                score += 30

        return score

    def evaluate_move_deep_optimized(self, game, move):
        """Optimized deep evaluation - no deep copy"""
        from_row, from_col, to_row, to_col = move

        # Start with positional score
        score = self.evaluate_move_positional(game, move)

        # Manually simulate without deep copy
        piece = game.board[from_row][from_col]
        captured = game.board[to_row][to_col]

        # Make move
        game.board[to_row][to_col] = piece
        game.board[from_row][from_col] = None

        # Evaluate resulting position
        opponent = 'black' if game.current_player == 'white' else 'white'

        # Check if gives check (bonus)
        if hasattr(game, 'is_in_check') and game.is_in_check(opponent):
            score += 50

        # Quick material count
        material_diff = 0
        for row in range(8):
            for col in range(8):
                p = game.board[row][col]
                if p:
                    val = self.piece_values[p['type']]
                    material_diff += val if p['color'] == game.current_player else -val
        score += material_diff * 0.1

        # Undo move
        game.board[from_row][from_col] = piece
        game.board[to_row][to_col] = captured

        return score

    def evaluate_material(self, game, color):
        """
        Evaluate material balance for a given color
        Returns positive score if color is ahead, negative if behind
        """
        my_material = 0
        opp_material = 0
        opponent = 'black' if color == 'white' else 'white'

        for row in range(8):
            for col in range(8):
                piece = game.board[row][col]
                if piece:
                    value = self.piece_values[piece['type']]
                    if piece['color'] == color:
                        my_material += value
                    else:
                        opp_material += value

        return my_material - opp_material

    def is_checkmate_move_fast(self, game, move):
        """Fast checkmate detection without deep copy"""
        from_row, from_col, to_row, to_col = move

        # Manually simulate
        piece = game.board[from_row][from_col]
        captured = game.board[to_row][to_col]
        old_player = game.current_player

        # Make move
        game.board[to_row][to_col] = piece
        game.board[from_row][from_col] = None
        if piece['type'] == 'king':
            old_king_pos = game.king_positions[piece['color']]
            game.king_positions[piece['color']] = (to_row, to_col)

        game.current_player = 'black' if old_player == 'white' else 'white'

        # Check for checkmate
        is_mate = False
        if hasattr(game, 'is_checkmate'):
            is_mate = game.is_checkmate(game.current_player)

        # Undo move
        game.board[from_row][from_col] = piece
        game.board[to_row][to_col] = captured
        if piece['type'] == 'king':
            game.king_positions[piece['color']] = old_king_pos
        game.current_player = old_player

        return is_mate
