# -*- coding: utf-8 -*-
"""Chess problem setup and success detection.

A problem's goal ('success_condition') is evaluated after each of the
player's moves. Supported goals:

  checkmate     the opponent is checkmated
  check         the opponent is in check
  capture       an opponent piece of a type in problem['target'] was captured
  promotion     a pawn has been promoted
  escape_check  the player is no longer in check
  save_piece    the player's piece of type target[0] is still there and not attacked
  stop_mate     the opponent has no move that checkmates the player
  win_material  the player has won at least problem['min_gain'] points of material
"""
import copy

from chess_logic import ChessGame, GameOptions

PIECE_VALUES = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 0}
PIECE_NAMES = {'pawn': 'bonden', 'knight': 'hästen', 'bishop': 'löparen',
               'rook': 'tornet', 'queen': 'damen', 'king': 'kungen'}

MESSAGES = {
    'checkmate': 'Schackmatt! Problemet är löst!',
    'check': 'Schack! Problemet är löst!',
    'capture': 'Bra! Du tog {target}. Problemet är löst!',
    'promotion': 'Bonden förvandlades! Problemet är löst!',
    'escape_check': 'Kungen är säker! Problemet är löst!',
    'save_piece': 'Bra! {target} är räddad. Problemet är löst!',
    'stop_mate': 'Bra försvar! Nu kan svart inte göra matt.',
    'win_material': 'Bra! Du vann material. Problemet är löst!',
}

SUPPORTED_GOALS = set(MESSAGES)


def _opponent(color):
    return 'black' if color == 'white' else 'white'


def setup_problem_game(problem, options=None):
    """Create a ChessGame set up with the problem's position."""
    opts = copy.copy(options) if options else GameOptions()
    # Problems always end at checkmate, regardless of the "capture the king" option
    opts.capture_king_on_checkmate = False
    game = ChessGame(opts)
    game.board = copy.deepcopy(problem['board'])
    game.current_player = problem['player_color']
    game.king_positions = dict(problem['king_positions'])
    game.castling_rights = {c: {'kingside': False, 'queenside': False} for c in ('white', 'black')}
    game.en_passant_target = None
    game.move_history = []
    return game


def clone_game(game):
    """Cheap copy of a game for looking ahead (no sounds)."""
    g = ChessGame.__new__(ChessGame)
    g.__dict__.update(game.__dict__)
    g.board = [row[:] for row in game.board]
    g.king_positions = dict(game.king_positions)
    g.castling_rights = copy.deepcopy(game.castling_rights)
    g.captured_pieces = {c: list(v) for c, v in game.captured_pieces.items()}
    g.move_history = list(game.move_history)
    g.check_sound = None
    g.win_sound = None
    return g


def legal_moves(game, color):
    """All legal moves (from_row, from_col, to_row, to_col) for color, which must be to move."""
    moves = []
    for r in range(8):
        for c in range(8):
            piece = game.board[r][c]
            if piece and piece['color'] == color:
                for tr, tc in game.get_valid_moves(r, c):
                    moves.append((r, c, tr, tc))
    return moves


def play_move(game, move, promote_to='queen'):
    """Make a move on game, completing a promotion. Returns make_move's result."""
    result = game.make_move(*move)
    if result.get('valid') and result.get('promotion'):
        row, col = result['position']
        game.promote_pawn(row, col, promote_to)
    return result


def _count(board, color, types):
    return sum(1 for row in board for p in row
               if p and p['color'] == color and p['type'] in types)


def material_balance(board, color):
    """Material of color minus material of the opponent."""
    total = 0
    for row in board:
        for p in row:
            if p:
                v = PIECE_VALUES[p['type']]
                total += v if p['color'] == color else -v
    return total


def attackers_of(game, row, col, color):
    """Types of color's pieces that attack the square (row, col)."""
    # Put a stand-in enemy piece on the square so that pawn captures count
    original = game.board[row][col]
    game.board[row][col] = {'type': 'pawn', 'color': _opponent(color)}
    try:
        return [p['type'] for r, line in enumerate(game.board) for c, p in enumerate(line)
                if p and p['color'] == color and (r, c) != (row, col)
                and (row, col) in game.get_pseudo_legal_moves_no_castling(r, c)]
    finally:
        game.board[row][col] = original


def piece_is_safe(game, row, col):
    """A piece is safe if nobody attacks it, or if it is defended and every
    attacker is worth at least as much (taking it would lose material)."""
    piece = game.board[row][col]
    enemies = attackers_of(game, row, col, _opponent(piece['color']))
    if not enemies:
        return True
    if not attackers_of(game, row, col, piece['color']):
        return False
    value = PIECE_VALUES[piece['type']]
    return min(100 if t == 'king' else PIECE_VALUES[t] for t in enemies) >= value


def opponent_can_mate(game, player):
    """True if the side to move (the player's opponent) has a mating move."""
    opp = _opponent(player)
    if game.current_player != opp:
        return False
    for move in legal_moves(game, opp):
        g = clone_game(game)
        play_move(g, move)
        if g.is_checkmate(player):
            return True
    return False


def goal_reached(problem, game):
    """Evaluate the problem's goal on the position after a player move."""
    goal = problem.get('success_condition', 'checkmate')
    me = problem['player_color']
    opp = _opponent(me)
    start = problem['board']
    targets = problem.get('target', [])

    if goal == 'checkmate':
        return game.is_checkmate(opp)
    if goal == 'check':
        return game.is_in_check(opp)
    if goal == 'capture':
        return _count(game.board, opp, targets) < _count(start, opp, targets)
    if goal == 'promotion':
        officers = ['knight', 'bishop', 'rook', 'queen']
        return _count(game.board, me, officers) > _count(start, me, officers)
    if goal == 'escape_check':
        return not game.is_in_check(me)
    if goal == 'save_piece':
        kind = targets[0]
        if _count(game.board, me, [kind]) < _count(start, me, [kind]):
            return False
        return all(piece_is_safe(game, r, c)
                   for r, row in enumerate(game.board) for c, p in enumerate(row)
                   if p and p['color'] == me and p['type'] == kind)
    if goal == 'stop_mate':
        return not opponent_can_mate(game, me)
    if goal == 'win_material':
        gain = material_balance(game.board, me) - material_balance(start, me)
        return gain >= problem.get('min_gain', 3)
    raise ValueError(f"Unknown success_condition {goal!r}")


def check_problem_success(problem, game, last_move=None):
    """Check if the problem is solved after the player's move.

    Returns dict with 'solved' (bool) and, when solved, 'message' (str).
    """
    goal = problem.get('success_condition', 'checkmate')
    me = problem['player_color']
    # A checkmate always solves the problem; a stalemate never does
    if goal != 'stop_mate' and game.is_checkmate(_opponent(me)):
        return {'solved': True, 'message': MESSAGES['checkmate']}
    if game.is_stalemate(_opponent(me)):
        return {'solved': False}
    if goal_reached(problem, game):
        target = PIECE_NAMES.get((problem.get('target') or ['queen'])[0], 'pjäsen')
        message = MESSAGES[goal].format(target=target)
        return {'solved': True, 'message': message[0].upper() + message[1:]}
    return {'solved': False}
