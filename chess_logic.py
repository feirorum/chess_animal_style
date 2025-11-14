import copy
import pygame
import json
import os
from datetime import datetime
import swedish_text as txt

class GameOptions:
    """Manages game options and settings"""
    OPTIONS_FILE = "options.txt"

    def __init__(self):
        self.capture_king_on_checkmate = False  # OFF by default
        self.animations_enabled = True  # ON by default
        self.animation_duration = 4.5  # 4.5 seconds by default
        self.game_mode = '2_player'  # '1_player' or '2_player'
        self.player_color = 'white'  # 'white' or 'black' (for 1-player mode)
        self.ai_skill_level = 5  # 1-10 (1=easiest/fastest, 10=hardest/slowest)
        self.load_options()

    def load_options(self):
        """Load options from file"""
        try:
            if os.path.exists(self.OPTIONS_FILE):
                with open(self.OPTIONS_FILE, 'r') as f:
                    data = json.load(f)
                    self.capture_king_on_checkmate = data.get('capture_king_on_checkmate', False)
                    self.animations_enabled = data.get('animations_enabled', True)
                    self.animation_duration = data.get('animation_duration', 4.5)
                    self.game_mode = data.get('game_mode', '2_player')
                    self.player_color = data.get('player_color', 'white')
                    # Convert old string levels to numeric
                    ai_level = data.get('ai_skill_level', 5)
                    if isinstance(ai_level, str):
                        ai_level = {'easy': 3, 'medium': 6, 'hard': 9}.get(ai_level, 5)
                    self.ai_skill_level = max(1, min(10, ai_level))
        except:
            # If file doesn't exist or is corrupted, use defaults
            self.capture_king_on_checkmate = False
            self.animations_enabled = True
            self.animation_duration = 4.5
            self.game_mode = '2_player'
            self.player_color = 'white'
            self.ai_skill_level = 5

    def save_options(self):
        """Save options to file"""
        data = {
            'capture_king_on_checkmate': self.capture_king_on_checkmate,
            'animations_enabled': self.animations_enabled,
            'animation_duration': self.animation_duration,
            'game_mode': self.game_mode,
            'player_color': self.player_color,
            'ai_skill_level': self.ai_skill_level
        }
        with open(self.OPTIONS_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    def toggle_capture_king(self):
        """Toggle the capture king on checkmate option"""
        self.capture_king_on_checkmate = not self.capture_king_on_checkmate
        self.save_options()

    def toggle_animations(self):
        """Toggle animations on/off"""
        self.animations_enabled = not self.animations_enabled
        self.save_options()

    def set_animation_duration(self, duration):
        """Set animation duration in seconds"""
        self.animation_duration = max(1.0, min(10.0, duration))  # Clamp between 1 and 10 seconds
        self.save_options()

    def set_game_mode(self, mode):
        """Set game mode ('1_player' or '2_player')"""
        self.game_mode = mode
        self.save_options()

    def set_player_color(self, color):
        """Set player color for 1-player mode ('white' or 'black')"""
        self.player_color = color
        self.save_options()

    def set_ai_skill_level(self, level):
        """Set AI skill level (1-10)"""
        self.ai_skill_level = max(1, min(10, level))
        self.save_options()

class ChessGame:
    def __init__(self, options=None):
        self.board = self.create_initial_board()
        self.current_player = 'white'
        self.move_history = []
        self.en_passant_target = None  # (row, col) of en passant target square
        self.castling_rights = {
            'white': {'kingside': True, 'queenside': True},
            'black': {'kingside': True, 'queenside': True}
        }
        self.king_positions = {'white': (7, 4), 'black': (0, 4)}
        self.options = options if options else GameOptions()
        self.king_captured = False  # Track if king was captured
        self.in_checkmate_capture_mode = False  # Track if in capture king mode after checkmate
        self.game_status = 'ongoing'  # Status: 'ongoing', 'finished'
        self.game_result = None  # Result: 'white_won', 'black_won', 'draw', None
        self.check_sound = None
        self.win_sound = None
        self.load_sounds()

    def load_sounds(self):
        """Load sound effects"""
        try:
            self.check_sound = pygame.mixer.Sound('assets/sounds/check.wav')
            self.win_sound = pygame.mixer.Sound('assets/sounds/win.wav')
        except:
            print("Sound files not found. Continuing without sound effects.")

    def create_initial_board(self):
        """Create the initial chess board with animal pieces"""
        board = [[None for _ in range(8)] for _ in range(8)]

        # Piece mapping: Queen=Cat, King=Dog, Knight=Horse, Pawn=Duckling, Bishop=Blobfish, Rook=Book
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']

        # Set up black pieces (top)
        for col in range(8):
            board[0][col] = {'type': piece_order[col], 'color': 'black'}
            board[1][col] = {'type': 'pawn', 'color': 'black'}

        # Set up white pieces (bottom)
        for col in range(8):
            board[6][col] = {'type': 'pawn', 'color': 'white'}
            board[7][col] = {'type': piece_order[col], 'color': 'white'}

        return board

    def get_valid_moves(self, row, col):
        """Get all valid moves for a piece at the given position"""
        piece = self.board[row][col]
        if not piece or piece['color'] != self.current_player:
            return []

        # Get pseudo-legal moves (moves that follow piece movement rules)
        pseudo_moves = self.get_pseudo_legal_moves(row, col)

        # In checkmate capture mode, all pseudo-legal moves are valid (can leave king in check)
        if self.in_checkmate_capture_mode:
            return pseudo_moves

        # Filter out moves that would leave the king in check
        valid_moves = []
        for to_row, to_col in pseudo_moves:
            if self.is_legal_move(row, col, to_row, to_col):
                valid_moves.append((to_row, to_col))

        return valid_moves

    def get_pseudo_legal_moves(self, row, col):
        """Get moves that follow piece movement rules (may leave king in check)"""
        piece = self.board[row][col]
        if not piece:
            return []

        piece_type = piece['type']

        if piece_type == 'pawn':
            return self.get_pawn_moves(row, col)
        elif piece_type == 'knight':
            return self.get_knight_moves(row, col)
        elif piece_type == 'bishop':
            return self.get_bishop_moves(row, col)
        elif piece_type == 'rook':
            return self.get_rook_moves(row, col)
        elif piece_type == 'queen':
            return self.get_queen_moves(row, col)
        elif piece_type == 'king':
            return self.get_king_moves(row, col)

        return []

    def get_pawn_moves(self, row, col):
        """Get all pawn moves (duckling moves)"""
        moves = []
        piece = self.board[row][col]
        direction = -1 if piece['color'] == 'white' else 1
        start_row = 6 if piece['color'] == 'white' else 1

        # Forward move
        if 0 <= row + direction < 8:
            if self.board[row + direction][col] is None:
                moves.append((row + direction, col))

                # Double move from starting position
                if row == start_row and self.board[row + 2 * direction][col] is None:
                    moves.append((row + 2 * direction, col))

        # Captures
        for dc in [-1, 1]:
            new_row, new_col = row + direction, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target and target['color'] != piece['color']:
                    moves.append((new_row, new_col))

        # En passant
        if self.en_passant_target:
            ep_row, ep_col = self.en_passant_target
            if row + direction == ep_row and abs(col - ep_col) == 1:
                moves.append((ep_row, ep_col))

        return moves

    def get_knight_moves(self, row, col):
        """Get all knight moves (horse moves)"""
        moves = []
        piece = self.board[row][col]
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if not target or target['color'] != piece['color']:
                    moves.append((new_row, new_col))

        return moves

    def get_bishop_moves(self, row, col):
        """Get all bishop moves (blobfish moves)"""
        return self.get_sliding_moves(row, col, [(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def get_rook_moves(self, row, col):
        """Get all rook moves (book moves)"""
        return self.get_sliding_moves(row, col, [(-1, 0), (1, 0), (0, -1), (0, 1)])

    def get_queen_moves(self, row, col):
        """Get all queen moves (cat moves)"""
        return self.get_sliding_moves(row, col, [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)])

    def get_king_moves(self, row, col):
        """Get all king moves (dog moves) including castling"""
        moves = []
        piece = self.board[row][col]

        # Normal king moves
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if not target or target['color'] != piece['color']:
                        moves.append((new_row, new_col))

        # Castling
        color = piece['color']
        if not self.is_square_attacked(row, col, 'white' if color == 'black' else 'black'):
            # Kingside castling
            if self.castling_rights[color]['kingside']:
                if self.board[row][5] is None and self.board[row][6] is None:
                    if not self.is_square_attacked(row, 5, 'white' if color == 'black' else 'black'):
                        if not self.is_square_attacked(row, 6, 'white' if color == 'black' else 'black'):
                            moves.append((row, 6))

            # Queenside castling
            if self.castling_rights[color]['queenside']:
                if self.board[row][1] is None and self.board[row][2] is None and self.board[row][3] is None:
                    if not self.is_square_attacked(row, 3, 'white' if color == 'black' else 'black'):
                        if not self.is_square_attacked(row, 2, 'white' if color == 'black' else 'black'):
                            moves.append((row, 2))

        return moves

    def get_sliding_moves(self, row, col, directions):
        """Get moves for sliding pieces (bishop, rook, queen)"""
        moves = []
        piece = self.board[row][col]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if not target:
                    moves.append((new_row, new_col))
                elif target['color'] != piece['color']:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row, new_col = new_row + dr, new_col + dc

        return moves

    def is_square_attacked(self, row, col, by_color):
        """Check if a square is attacked by the given color"""
        # Check all pieces of the attacking color
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece['color'] == by_color:
                    # Get moves for this piece (without checking for check)
                    moves = self.get_pseudo_legal_moves_no_castling(r, c)
                    if (row, col) in moves:
                        return True
        return False

    def get_pseudo_legal_moves_no_castling(self, row, col):
        """Get pseudo-legal moves without castling (to avoid infinite recursion)"""
        piece = self.board[row][col]
        if not piece:
            return []

        piece_type = piece['type']

        if piece_type == 'pawn':
            return self.get_pawn_moves(row, col)
        elif piece_type == 'knight':
            return self.get_knight_moves(row, col)
        elif piece_type == 'bishop':
            return self.get_bishop_moves(row, col)
        elif piece_type == 'rook':
            return self.get_rook_moves(row, col)
        elif piece_type == 'queen':
            return self.get_queen_moves(row, col)
        elif piece_type == 'king':
            # King moves without castling
            moves = []
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        target = self.board[new_row][new_col]
                        if not target or target['color'] != piece['color']:
                            moves.append((new_row, new_col))
            return moves

        return []

    def is_in_check(self, color):
        """Check if the given color's king is in check"""
        king_pos = self.king_positions[color]
        opponent_color = 'black' if color == 'white' else 'white'
        return self.is_square_attacked(king_pos[0], king_pos[1], opponent_color)

    def is_legal_move(self, from_row, from_col, to_row, to_col):
        """Check if a move is legal (doesn't leave king in check)"""
        # Make a copy of the board and simulate the move
        temp_board = copy.deepcopy(self.board)
        temp_king_pos = copy.deepcopy(self.king_positions)

        piece = temp_board[from_row][from_col]
        temp_board[to_row][to_col] = piece
        temp_board[from_row][from_col] = None

        # Update king position if king moved
        if piece['type'] == 'king':
            temp_king_pos[piece['color']] = (to_row, to_col)

        # Temporarily update board state
        original_board = self.board
        original_king_pos = self.king_positions
        self.board = temp_board
        self.king_positions = temp_king_pos

        # Check if king is in check
        in_check = self.is_in_check(piece['color'])

        # Restore original board
        self.board = original_board
        self.king_positions = original_king_pos

        return not in_check

    def make_move(self, from_row, from_col, to_row, to_col):
        """Attempt to make a move and return result"""
        piece = self.board[from_row][from_col]

        if not piece or piece['color'] != self.current_player:
            return {'valid': False, 'reason': txt.ERROR_NOT_YOUR_PIECE}

        # In checkmate capture mode, skip check validation
        if self.in_checkmate_capture_mode:
            valid_moves = self.get_valid_moves(from_row, from_col)
            if (to_row, to_col) not in valid_moves:
                return {'valid': False, 'reason': txt.ERROR_INVALID_MOVE}
        # Check if in check
        elif self.is_in_check(self.current_player):
            # Must block or move out of check
            if not self.is_legal_move(from_row, from_col, to_row, to_col):
                return {'valid': False, 'reason': txt.ERROR_IN_CHECK}

            # Check if move is in valid moves
            valid_moves = self.get_valid_moves(from_row, from_col)
            if (to_row, to_col) not in valid_moves:
                return {'valid': False, 'reason': txt.ERROR_IN_CHECK}
        else:
            # Normal move validation
            valid_moves = self.get_valid_moves(from_row, from_col)
            if (to_row, to_col) not in valid_moves:
                # Determine specific reason
                if piece['type'] == 'king' and abs(to_col - from_col) == 2:
                    if to_col > from_col:
                        return {'valid': False, 'reason': txt.ERROR_CASTLE_KINGSIDE}
                    else:
                        return {'valid': False, 'reason': txt.ERROR_CASTLE_QUEENSIDE}
                return {'valid': False, 'reason': txt.ERROR_INVALID_MOVE}

        # Special move handling
        is_castling = piece['type'] == 'king' and abs(to_col - from_col) == 2
        is_en_passant = piece['type'] == 'pawn' and self.en_passant_target == (to_row, to_col)
        is_capture = self.board[to_row][to_col] is not None or is_en_passant

        # Check if capturing a king
        captured_piece = self.board[to_row][to_col]
        is_king_capture = captured_piece and captured_piece['type'] == 'king'

        # Execute the move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

        # Handle castling
        if is_castling:
            if to_col > from_col:  # Kingside
                self.board[to_row][5] = self.board[to_row][7]
                self.board[to_row][7] = None
            else:  # Queenside
                self.board[to_row][3] = self.board[to_row][0]
                self.board[to_row][0] = None
            self.castling_rights[piece['color']]['kingside'] = False
            self.castling_rights[piece['color']]['queenside'] = False

        # Handle en passant
        if is_en_passant:
            # Remove the captured pawn
            capture_row = from_row
            self.board[capture_row][to_col] = None

        # Update castling rights
        if piece['type'] == 'king':
            self.king_positions[piece['color']] = (to_row, to_col)
            self.castling_rights[piece['color']]['kingside'] = False
            self.castling_rights[piece['color']]['queenside'] = False
        elif piece['type'] == 'rook':
            if from_col == 0:
                self.castling_rights[piece['color']]['queenside'] = False
            elif from_col == 7:
                self.castling_rights[piece['color']]['kingside'] = False

        # Update en passant target
        if piece['type'] == 'pawn' and abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, from_col)
        else:
            self.en_passant_target = None

        # Record the move in chess notation
        move_notation = self.get_move_notation(piece, from_row, from_col, to_row, to_col, is_capture, is_castling)
        self.move_history.append(move_notation)

        # Check for pawn promotion
        if piece['type'] == 'pawn':
            promotion_row = 0 if piece['color'] == 'white' else 7
            if to_row == promotion_row:
                return {'valid': True, 'promotion': True, 'position': (to_row, to_col), 'color': piece['color']}

        # Check if a king was captured (before switching player)
        if is_king_capture:
            self.king_captured = True
            self.in_checkmate_capture_mode = False  # Game is over
            self.game_status = 'finished'
            self.game_result = f"{piece['color']}_won"
            if self.win_sound:
                self.win_sound.play()
            # Don't switch player yet, game is over
            return {'valid': True, 'king_captured': True, 'winner': piece['color']}

        # Switch player
        self.current_player = 'black' if self.current_player == 'white' else 'white'

        # Check if opponent is in check
        if self.is_in_check(self.current_player):
            if self.check_sound:
                self.check_sound.play()

            # Check for checkmate
            if self.is_checkmate(self.current_player):
                if self.options.capture_king_on_checkmate:
                    # Option enabled: continue playing, king can be captured
                    self.in_checkmate_capture_mode = True
                    return {'valid': True, 'checkmate': True, 'continue_play': True, 'in_check': self.current_player}
                else:
                    # Default behavior: game ends
                    self.game_status = 'finished'
                    self.game_result = f"{piece['color']}_won"
                    if self.win_sound:
                        self.win_sound.play()
                    return {'valid': True, 'checkmate': True, 'winner': piece['color']}
        else:
            # Check for stalemate only in normal mode (not in check but no legal moves)
            if not self.options.capture_king_on_checkmate:
                if self.is_stalemate(self.current_player):
                    self.game_status = 'finished'
                    self.game_result = 'draw'
                    return {'valid': True, 'stalemate': True}

        return {'valid': True}

    def promote_pawn(self, row, col, piece_type):
        """Promote a pawn to the specified piece type"""
        piece = self.board[row][col]
        if piece and piece['type'] == 'pawn':
            self.board[row][col] = {'type': piece_type, 'color': piece['color']}

            # Now switch player after promotion
            self.current_player = 'black' if self.current_player == 'white' else 'white'

            # Check if opponent is in check after promotion
            if self.is_in_check(self.current_player):
                if self.check_sound:
                    self.check_sound.play()

                # Check for checkmate
                if self.is_checkmate(self.current_player):
                    if self.options.capture_king_on_checkmate:
                        # Option enabled: continue playing, king can be captured
                        self.in_checkmate_capture_mode = True
                        return {'success': True, 'checkmate': True, 'continue_play': True, 'in_check': self.current_player}
                    else:
                        # Default behavior: game ends
                        self.game_status = 'finished'
                        self.game_result = f"{piece['color']}_won"
                        if self.win_sound:
                            self.win_sound.play()
                        return {'checkmate': True, 'winner': piece['color']}
            else:
                # Check for stalemate only in normal mode (not in check but no legal moves)
                if not self.options.capture_king_on_checkmate:
                    if self.is_stalemate(self.current_player):
                        self.game_status = 'finished'
                        self.game_result = 'draw'
                        return {'success': True, 'stalemate': True}

            return {'success': True}
        return {'success': False}

    def is_checkmate(self, color):
        """Check if the given color is in checkmate"""
        if not self.is_in_check(color):
            return False

        # Check if any piece has a valid move
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece['color'] == color:
                    if len(self.get_valid_moves(row, col)) > 0:
                        return False

        return True

    def is_stalemate(self, color):
        """Check if the given color is in stalemate (draw)"""
        # Stalemate occurs when the player is NOT in check but has no legal moves
        if self.is_in_check(color):
            return False

        # Check if any piece has a valid move
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece['color'] == color:
                    if len(self.get_valid_moves(row, col)) > 0:
                        return False

        return True

    def has_any_valid_moves(self, color):
        """Check if the given color has any valid moves"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece['color'] == color:
                    if len(self.get_valid_moves(row, col)) > 0:
                        return True
        return False

    def check_game_status(self):
        """Check and update the current game status and result"""
        # If game is already finished, don't change status
        if self.game_status == 'finished':
            return

        # Check if a king was captured (special mode)
        if self.king_captured:
            self.game_status = 'finished'
            # Determine winner (the player who captured the king)
            opponent = 'black' if self.current_player == 'white' else 'white'
            self.game_result = f'{opponent}_won'
            return

        # In normal mode, check for checkmate or stalemate
        if not self.options.capture_king_on_checkmate:
            # Check if current player is in checkmate
            if self.is_checkmate(self.current_player):
                self.game_status = 'finished'
                opponent = 'black' if self.current_player == 'white' else 'white'
                self.game_result = f'{opponent}_won'
                return

            # Check if current player is in stalemate
            if self.is_stalemate(self.current_player):
                self.game_status = 'finished'
                self.game_result = 'draw'
                return

        # In special mode (capture king), game continues even after checkmate
        # Game only ends when king is captured (checked above)

        # Game is still ongoing
        self.game_status = 'ongoing'
        self.game_result = None

    def pass_turn(self):
        """Pass the turn to the other player (only allowed in special mode when in checkmate)"""
        # Only allow passing in special mode and when in checkmate capture mode
        if not self.options.capture_king_on_checkmate or not self.in_checkmate_capture_mode:
            return {'valid': False, 'reason': txt.ERROR_PASS_ONLY_SPECIAL}

        # Only allow passing when player has no valid moves
        if self.has_any_valid_moves(self.current_player):
            return {'valid': False, 'reason': txt.ERROR_PASS_ONLY_NO_MOVES}

        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.move_history.append("Pass")
        return {'valid': True, 'passed': True}

    def get_move_notation(self, piece, from_row, from_col, to_row, to_col, is_capture, is_castling):
        """Convert a move to chess notation (e.g., pE5, QxB7)"""
        if is_castling:
            return "O-O" if to_col > from_col else "O-O-O"

        # Get piece letter (K=King, Q=Queen, R=Rook, B=Bishop, N=Knight, p=Pawn)
        piece_letters = {
            'king': 'K',
            'queen': 'Q',
            'rook': 'R',
            'bishop': 'B',
            'knight': 'N',
            'pawn': 'p'
        }
        piece_letter = piece_letters.get(piece['type'], '')

        # Convert to chess coordinates (e.g., e4)
        col_letter = chr(ord('a') + to_col)
        row_number = str(8 - to_row)
        destination = f"{col_letter.upper()}{row_number}"

        # Add capture notation
        capture_symbol = 'x' if is_capture else ''

        return f"{piece_letter}{capture_symbol}{destination}"

    def save_game(self, name="game"):
        """Save the current game state to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.json"
        filepath = os.path.join("games", filename)

        game_state = {
            'board': self.board,
            'current_player': self.current_player,
            'move_history': self.move_history,
            'en_passant_target': self.en_passant_target,
            'castling_rights': self.castling_rights,
            'king_positions': self.king_positions,
            'in_checkmate_capture_mode': self.in_checkmate_capture_mode,
            'game_status': self.game_status,
            'game_result': self.game_result,
            'king_captured': self.king_captured
        }

        with open(filepath, 'w') as f:
            json.dump(game_state, f, indent=2)

        return filepath

    def load_game(self, filepath):
        """Load a game state from a file"""
        with open(filepath, 'r') as f:
            game_state = json.load(f)

        self.board = game_state['board']
        self.current_player = game_state['current_player']
        self.move_history = game_state['move_history']
        self.en_passant_target = game_state['en_passant_target']
        if game_state['en_passant_target']:
            self.en_passant_target = tuple(game_state['en_passant_target'])
        self.castling_rights = game_state['castling_rights']
        self.king_positions = {k: tuple(v) for k, v in game_state['king_positions'].items()}
        self.in_checkmate_capture_mode = game_state.get('in_checkmate_capture_mode', False)
        self.game_status = game_state.get('game_status', 'ongoing')
        self.game_result = game_state.get('game_result', None)
        self.king_captured = game_state.get('king_captured', False)

        # For old saved games that don't have game_status, check it now
        if 'game_status' not in game_state:
            self.check_game_status()

    @staticmethod
    def get_saved_games():
        """Get list of all saved games"""
        games_dir = "games"
        if not os.path.exists(games_dir):
            return []

        saved_games = []
        for filename in os.listdir(games_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(games_dir, filename)
                # Get file modification time
                mtime = os.path.getmtime(filepath)
                saved_games.append({
                    'filename': filename,
                    'filepath': filepath,
                    'modified': datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                })

        # Sort by modification time (newest first)
        saved_games.sort(key=lambda x: x['modified'], reverse=True)
        return saved_games
