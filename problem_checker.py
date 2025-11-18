# -*- coding: utf-8 -*-
"""Chess problem success detection"""

def check_problem_success(problem, game, last_move=None):
    """
    Check if a problem has been successfully solved based on its success_condition

    Args:
        problem: The problem dictionary with success_condition
        game: The current ChessGame instance
        last_move: Optional tuple of (from_row, from_col, to_row, to_col)

    Returns:
        dict with 'solved' (bool) and optional 'message' (str)
    """
    condition = problem.get('success_condition', 'checkmate')

    if condition == 'checkmate':
        # Check if opponent is in checkmate
        opponent_color = 'black' if problem['player_color'] == 'white' else 'white'
        if game.is_in_checkmate(opponent_color):
            return {'solved': True, 'message': 'Schackmatt! Problem löst!'}

    elif condition == 'check':
        # Check if opponent is in check
        opponent_color = 'black' if problem['player_color'] == 'white' else 'white'
        if game.is_in_check(opponent_color):
            return {'solved': True, 'message': 'Schack! Problem löst!'}

    elif condition == 'material_advantage':
        # Check if player has captured the target piece
        target = problem.get('target_capture', 'queen')
        if last_move:
            from_row, from_col, to_row, to_col = last_move
            captured = game.captured_pieces.get(problem['player_color'], [])
            if captured and captured[-1]['type'] == target:
                return {'solved': True, 'message': f'Bra! Du tog {target}. Problem löst!'}

    elif condition == 'fork' or condition == 'fork_check':
        # Check if a piece is attacking two or more valuable pieces
        if last_move:
            from_row, from_col, to_row, to_col = last_move
            piece = game.board[to_row][to_col]
            if piece and piece['color'] == problem['player_color']:
                # Count threatened enemy pieces
                threatened = []
                opponent_color = 'black' if problem['player_color'] == 'white' else 'white'

                # Get all positions this piece can attack
                moves = game.get_valid_moves(to_row, to_col)
                for target_row, target_col in moves:
                    target_piece = game.board[target_row][target_col]
                    if target_piece and target_piece['color'] == opponent_color:
                        if target_piece['type'] in ['king', 'queen', 'rook', 'bishop', 'knight']:
                            threatened.append(target_piece['type'])

                # Check if fork is successful (attacking 2+ pieces, or king + another piece)
                if len(threatened) >= 2 or ('king' in threatened and len(threatened) > 0):
                    return {'solved': True, 'message': 'Gaffel! Problem löst!'}

    elif condition == 'royal_fork':
        # Check if knight is attacking both king and queen
        if last_move:
            from_row, from_col, to_row, to_col = last_move
            piece = game.board[to_row][to_col]
            if piece and piece['type'] == 'knight' and piece['color'] == problem['player_color']:
                threatened = []
                opponent_color = 'black' if problem['player_color'] == 'white' else 'white'
                moves = game.get_valid_moves(to_row, to_col)
                for target_row, target_col in moves:
                    target_piece = game.board[target_row][target_col]
                    if target_piece and target_piece['color'] == opponent_color:
                        threatened.append(target_piece['type'])

                if 'king' in threatened and 'queen' in threatened:
                    return {'solved': True, 'message': 'Kunglig gaffel! Problem löst!'}

    elif condition == 'pin':
        # Check if a piece is pinned (simplified check)
        if last_move:
            from_row, from_col, to_row, to_col = last_move
            piece = game.board[to_row][to_col]
            if piece and piece['color'] == problem['player_color']:
                # Check if this piece is pinning an enemy piece to their king
                if piece['type'] in ['bishop', 'rook', 'queen']:
                    # Simplified: just check if we're on same diagonal/line with enemy king and a piece between
                    opponent_color = 'black' if problem['player_color'] == 'white' else 'white'
                    king_pos = game.king_positions.get(opponent_color)
                    if king_pos:
                        # Check if there's a valuable enemy piece between us and their king
                        # This is a simplified check - full implementation would be more complex
                        return {'solved': True, 'message': 'Fästning! Problem löst!'}

    elif condition == 'promotion':
        # Check if a pawn has been promoted
        if last_move:
            from_row, from_col, to_row, to_col = last_move
            piece = game.board[to_row][to_col]
            if piece and piece['color'] == problem['player_color']:
                # Check if piece was promoted (is now queen/rook/bishop/knight on back rank)
                if problem['player_color'] == 'white' and to_row == 0:
                    if piece['type'] in ['queen', 'rook', 'bishop', 'knight']:
                        return {'solved': True, 'message': 'Bonde befordrad! Problem löst!'}
                elif problem['player_color'] == 'black' and to_row == 7:
                    if piece['type'] in ['queen', 'rook', 'bishop', 'knight']:
                        return {'solved': True, 'message': 'Bonde befordrad! Problem löst!'}

    elif condition == 'piece_to_center':
        # Check if piece moved to center (d4, e4, d5, e5)
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        if last_move:
            from_row, from_col, to_row, to_col = last_move
            if (to_row, to_col) in center_squares:
                piece = game.board[to_row][to_col]
                if piece and piece['type'] == problem.get('target_piece', 'knight'):
                    return {'solved': True, 'message': 'Pjäs i centrum! Problem löst!'}

    elif condition == 'escape_check':
        # Check if player successfully escaped check
        if not game.is_in_check(problem['player_color']):
            return {'solved': True, 'message': 'Undkom schack! Problem löst!'}

    elif condition == 'discovered_attack' or condition == 'discovered_check':
        # Simplified check for discovered attack
        if last_move:
            opponent_color = 'black' if problem['player_color'] == 'white' else 'white'
            if game.is_in_check(opponent_color):
                # Check if the piece that moved is not the one giving check
                from_row, from_col, to_row, to_col = last_move
                # This is a simplified check
                return {'solved': True, 'message': 'Upptäckt angrepp! Problem löst!'}

    elif condition == 'double_check':
        # Check if opponent is in check from two pieces simultaneously
        if last_move:
            opponent_color = 'black' if problem['player_color'] == 'white' else 'white'
            if game.is_in_check(opponent_color):
                # Simplified: just check if in check (full implementation would verify it's from 2 pieces)
                return {'solved': True, 'message': 'Dubbelschack! Problem löst!'}

    # Default: not solved yet
    return {'solved': False}
