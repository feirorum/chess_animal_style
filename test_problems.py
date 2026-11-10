# -*- coding: utf-8 -*-
"""Verify every chess problem with the game's own engine and problem checker.

For each problem:
  - both kings are on the board and the side not to move is not in check
  - the goal is one the checker supports
  - the stored solution move reaches the goal within the allowed number of
    moves against EVERY opponent reply (for 'win_material' the gain must also
    survive the opponent's next reply)

Run: python test_problems.py [problem numbers...]
"""
import os
import re
import sys
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402

pygame.init()

from chess_problems import CHESS_PROBLEMS  # noqa: E402
from problem_checker import (SUPPORTED_GOALS, check_problem_success, clone_game,  # noqa: E402
                             legal_moves, material_balance, play_move, setup_problem_game)

SAN_PIECES = {'K': 'king', 'Q': 'queen', 'R': 'rook', 'B': 'bishop', 'N': 'knight'}
PROMO = {'Q': 'queen', 'R': 'rook', 'B': 'bishop', 'N': 'knight'}
SAN_RE = re.compile(r'^([KQRBN])?([a-h])?([1-8])?x?([a-h][1-8])(?:=([QRBN]))?[+#]?$')


def square(name):
    return 8 - int(name[1]), ord(name[0]) - ord('a')


def parse_san(game, san):
    """Find the legal move matching a SAN string. Returns (move, promotion piece)."""
    m = SAN_RE.match(san)
    if not m:
        raise ValueError(f"Cannot parse SAN {san!r}")
    piece, from_file, from_rank, dest, promo = m.groups()
    kind = SAN_PIECES.get(piece, 'pawn')
    to = square(dest)
    matches = []
    for move in legal_moves(game, game.current_player):
        fr, fc, tr, tc = move
        if (tr, tc) != to or game.board[fr][fc]['type'] != kind:
            continue
        if from_file and fc != ord(from_file) - ord('a'):
            continue
        if from_rank and fr != 8 - int(from_rank):
            continue
        matches.append(move)
    if len(matches) != 1:
        raise ValueError(f"SAN {san!r} matches {len(matches)} moves")
    return matches[0], PROMO.get(promo, 'queen')


def solved(problem, game, move):
    return check_problem_success(problem, game, move)['solved']


def robust(problem, game):
    """For win_material: the gain must survive every opponent reply."""
    if problem['success_condition'] != 'win_material' or game.is_checkmate(game.current_player):
        return True
    me = problem['player_color']
    base = material_balance(problem['board'], me)
    for reply in legal_moves(game, game.current_player):
        g = clone_game(game)
        play_move(g, reply)
        if material_balance(g.board, me) - base < problem['min_gain']:
            return False
    return True


def can_force(problem, game, n):
    """Player to move: can the goal be forced within n moves?"""
    for move in legal_moves(game, game.current_player):
        if forces_with(problem, game, move, n):
            return True
    return False


def forces_with(problem, game, move, n, promote_to='queen'):
    g = clone_game(game)
    play_move(g, move, promote_to)
    if solved(problem, g, move):
        return robust(problem, g)
    if n <= 1 or g.game_status != 'ongoing':
        return False
    replies = legal_moves(g, g.current_player)
    for reply in replies:
        g2 = clone_game(g)
        play_move(g2, reply)
        if g2.game_status != 'ongoing' or not can_force(problem, g2, n - 1):
            return False
    return bool(replies)


def check(index, problem):
    game = setup_problem_game(problem)
    me = problem['player_color']
    opp = 'black' if me == 'white' else 'white'
    kings = {c: sum(1 for row in game.board for p in row if p and p['type'] == 'king' and p['color'] == c)
             for c in ('white', 'black')}
    if kings != {'white': 1, 'black': 1}:
        return f"kings on board: {kings}"
    if game.is_in_check(opp):
        return "the opponent is already in check"
    if problem['success_condition'] not in SUPPORTED_GOALS:
        return f"unsupported goal {problem['success_condition']!r}"
    if not legal_moves(game, me):
        return "player has no legal moves"
    move, promo = parse_san(game, problem['solution'])
    if not forces_with(problem, game, move, problem['moves'], promo):
        return f"solution {problem['solution']} does not force the goal in {problem['moves']} move(s)"
    return None


def main():
    only = {int(a) for a in sys.argv[1:]}
    failures = 0
    t0 = time.time()
    for i, problem in enumerate(CHESS_PROBLEMS, 1):
        if only and i not in only:
            continue
        error = check(i, problem)
        status = "OK  " if error is None else "FAIL"
        print(f"{status} {i:2}. [{problem['difficulty']:<6}] {problem['title']}" + (f": {error}" if error else ""),
              flush=True)
        failures += error is not None
    print(f"\n{failures} failure(s), {time.time() - t0:.0f}s")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
