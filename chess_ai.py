# -*- coding: utf-8 -*-
"""Simple chess AI engine for playing against the computer"""

import random
import copy

class ChessAI:
    """Rudimentary chess playing engine with configurable skill levels"""

    def __init__(self, skill_level='easy'):
        """
        Initialize the chess AI
        skill_level: 'easy', 'medium', or 'hard'
        """
        self.skill_level = skill_level

        # Piece values for evaluation (standard chess values)
        self.piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0  # King is invaluable, but we don't count it in material
        }

    def get_best_move(self, game):
        """
        Get the best move for the current player based on skill level
        Returns: (from_row, from_col, to_row, to_col) or None if no moves available
        """
        all_moves = self.get_all_valid_moves(game, game.current_player)

        if not all_moves:
            return None

        if self.skill_level == 'easy':
            return self.get_easy_move(game, all_moves)
        elif self.skill_level == 'medium':
            return self.get_medium_move(game, all_moves)
        else:  # hard
            return self.get_hard_move(game, all_moves)

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

    def get_easy_move(self, game, all_moves):
        """
        Easy AI: 70% random moves, 30% captures
        Makes mistakes frequently
        """
        # Find all capture moves
        captures = []
        for from_row, from_col, to_row, to_col in all_moves:
            if game.board[to_row][to_col] is not None:
                captures.append((from_row, from_col, to_row, to_col))

        # 30% chance to prefer captures (if available)
        if captures and random.random() < 0.3:
            return random.choice(captures)

        # Otherwise, random move
        return random.choice(all_moves)

    def get_medium_move(self, game, all_moves):
        """
        Medium AI: Prefers good moves but still makes mistakes
        - Always takes free pieces
        - Sometimes makes tactical moves
        - 50% random otherwise
        """
        # Evaluate all moves
        scored_moves = []
        for move in all_moves:
            score = self.evaluate_move(game, move)
            scored_moves.append((move, score))

        # Sort by score (best first)
        scored_moves.sort(key=lambda x: x[1], reverse=True)

        # 50% chance to play the best move, 50% to play a random decent move
        if random.random() < 0.5:
            return scored_moves[0][0]  # Best move
        else:
            # Pick from top 5 moves (or fewer if not available)
            top_moves = scored_moves[:min(5, len(scored_moves))]
            return random.choice(top_moves)[0]

    def get_hard_move(self, game, all_moves):
        """
        Hard AI: Looks ahead and plays strong moves
        - Always takes best material
        - Looks for checkmate
        - Considers position
        """
        # Check for checkmate moves first
        for move in all_moves:
            if self.is_checkmate_move(game, move):
                return move

        # Evaluate all moves with deeper analysis
        scored_moves = []
        for move in all_moves:
            score = self.evaluate_move_deep(game, move)
            scored_moves.append((move, score))

        # Sort by score (best first)
        scored_moves.sort(key=lambda x: x[1], reverse=True)

        # Play best move (with 10% randomness for variety)
        if random.random() < 0.9:
            return scored_moves[0][0]
        else:
            # Pick from top 3 moves
            top_moves = scored_moves[:min(3, len(scored_moves))]
            return random.choice(top_moves)[0]

    def evaluate_move(self, game, move):
        """
        Simple move evaluation
        Returns a score for the move (higher is better)
        """
        from_row, from_col, to_row, to_col = move
        score = 0

        # Bonus for capturing pieces
        target = game.board[to_row][to_col]
        if target:
            score += self.piece_values[target['type']] * 10

        # Small bonus for center control (e4, d4, e5, d5)
        if 3 <= to_row <= 4 and 3 <= to_col <= 4:
            score += 1

        # Bonus for developing pieces (moving from starting position)
        piece = game.board[from_row][from_col]
        if piece['type'] in ['knight', 'bishop']:
            if piece['color'] == 'white' and from_row == 7:
                score += 2
            elif piece['color'] == 'black' and from_row == 0:
                score += 2

        return score

    def evaluate_move_deep(self, game, move):
        """
        Deeper move evaluation for hard AI
        Simulates the move and evaluates the resulting position
        """
        from_row, from_col, to_row, to_col = move

        # Start with simple evaluation
        score = self.evaluate_move(game, move)

        # Simulate the move
        temp_game = self.simulate_move(game, move)
        if temp_game is None:
            return -1000  # Invalid move

        # Evaluate the position after the move
        material_score = self.evaluate_material(temp_game, game.current_player)
        score += material_score

        # Check if this move gives check
        opponent = 'black' if game.current_player == 'white' else 'white'
        if temp_game.is_in_check(opponent):
            score += 5

        # Look ahead one move for opponent's response
        opponent_moves = self.get_all_valid_moves(temp_game, opponent)
        if opponent_moves:
            # Find opponent's best counter
            best_counter_score = -1000
            for opp_move in opponent_moves[:10]:  # Limit to 10 moves for speed
                counter_score = self.evaluate_move(temp_game, opp_move)
                best_counter_score = max(best_counter_score, counter_score)

            # Subtract opponent's best response from our score
            score -= best_counter_score * 0.5

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

    def simulate_move(self, game, move):
        """
        Simulate a move and return a new game state
        Returns None if move is invalid
        """
        from_row, from_col, to_row, to_col = move

        # Create a deep copy of the game
        temp_game = copy.deepcopy(game)

        # Try to make the move
        result = temp_game.make_move(from_row, from_col, to_row, to_col)

        if result.get('valid'):
            # Handle promotion automatically (choose queen)
            if result.get('promotion'):
                temp_game.promote_pawn(to_row, to_col, 'queen')
            return temp_game

        return None

    def is_checkmate_move(self, game, move):
        """Check if a move leads to checkmate"""
        temp_game = self.simulate_move(game, move)
        if temp_game is None:
            return False

        opponent = 'black' if game.current_player == 'white' else 'white'
        return temp_game.is_checkmate(opponent)
