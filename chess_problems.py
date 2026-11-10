# -*- coding: utf-8 -*-
"""Chess problems for children, ordered from easy to hard.

The 60 problems form a course:
  Easy   1-20  how the pieces move and capture, promotion, check,
               getting out of check, first checkmates, first forks
  Medium 21-40 tactics (fork, pin, skewer, discovered attack, double check),
               classic mate patterns, stopping a mate threat, first mates in two
  Hard   41-60 combinations: sacrifices, deflection, underpromotion, quiet moves

Each problem is written as a FEN string and converted to the game's board
format when this module is imported. Every problem is checked by
test_problems.py: legal position with both kings, and the goal can be forced
within the allowed number of moves whatever the opponent replies.

Problem fields:
  title, objective, hint   Swedish texts shown in the game
  difficulty               'easy' | 'medium' | 'hard'
  fen                      position; side to move is the player
  success_condition        goal, see problem_checker.py
  moves                    how many moves the player gets
  target                   piece types for 'capture' / 'save_piece'
  min_gain                 material the player must win for 'win_material'
  solution                 a correct first move (SAN), used by the tests
"""

_DEFS = [
    # ===================== LÄTT: pjäserna, slå, schack, första matterna =====================
    dict(title='Tornet tar', objective='Ta hästen med tornet',
         hint='Tornet (boken) går rakt: upp, ner och åt sidan. Hästen står på a4.',
         difficulty='easy', success_condition='capture', target=['knight'], moves=1,
         fen='7k/8/8/8/n7/8/8/R3K3 w - - 0 1', solution='Rxa4'),
    dict(title='Löparen tar', objective='Ta tornet med löparen',
         hint='Löparen (klumpfisken) går snett. Följ diagonalen från c1 upp till h6.',
         difficulty='easy', success_condition='capture', target=['rook'], moves=1,
         fen='7k/8/7r/8/8/8/8/2B1K3 w - - 0 1', solution='Bxh6'),
    dict(title='Hästen hoppar', objective='Ta damen med hästen',
         hint='Hästen hoppar som ett L: två steg åt ett håll och ett steg åt sidan.',
         difficulty='easy', success_condition='capture', target=['queen'], moves=1,
         fen='4k3/8/8/3q4/8/2N5/8/4K3 w - - 0 1', solution='Nxd5'),
    dict(title='Damen tar', objective='Ta tornet med damen',
         hint='Damen (katten) går både rakt och snett, hur långt som helst.',
         difficulty='easy', success_condition='capture', target=['rook'], moves=1,
         fen='6k1/3r4/8/8/8/8/8/3Q2K1 w - - 0 1', solution='Qxd7'),
    dict(title='Bonden tar snett', objective='Ta hästen med bonden',
         hint='Bonden (ankungen) går rakt fram, men den tar snett framåt.',
         difficulty='easy', success_condition='capture', target=['knight'], moves=1,
         fen='4k3/8/8/3np3/4P3/8/8/4K3 w - - 0 1', solution='exd5'),
    dict(title='Kungen tar', objective='Ta tornet med kungen',
         hint='Kungen (hunden) går ett steg åt alla håll. Ingen skyddar tornet!',
         difficulty='easy', success_condition='capture', target=['rook'], moves=1,
         fen='4k3/8/8/8/8/8/3r4/4K3 w - - 0 1', solution='Kxd2'),
    dict(title='Bonden blir dam', objective='Gör bonden till en dam',
         hint='När bonden kommer till sista raden får den bli en dam.',
         difficulty='easy', success_condition='promotion', moves=1,
         fen='7k/P7/8/8/8/8/8/4K3 w - - 0 1', solution='a8=Q+'),
    dict(title='Rädda damen', objective='Flytta damen i säkerhet',
         hint='Bonden på e5 hotar damen. Hitta en ruta där ingen kan ta henne.',
         difficulty='easy', success_condition='save_piece', target=['queen'], moves=1,
         fen='6k1/8/8/4p3/3Q4/8/8/6K1 w - - 0 1', solution='Qd3'),
    dict(title='Schack med tornet', objective='Ge schack med tornet',
         hint='Schack betyder att du hotar kungen. Ställ tornet på samma rad eller linje som kungen.',
         difficulty='easy', success_condition='check', moves=1,
         fen='4k3/8/8/8/8/8/8/R5K1 w - - 0 1', solution='Ra8+'),
    dict(title='Schack med hästen', objective='Ge schack med hästen',
         hint='Vilka rutor kan hästen hoppa till? Hitta en som hotar kungen på e8.',
         difficulty='easy', success_condition='check', moves=1,
         fen='4k3/8/8/8/4N3/8/8/4K3 w - - 0 1', solution='Nf6+'),
    dict(title='Kliv undan', objective='Flytta kungen ur schack',
         hint='Tornet hotar hela e-linjen. Kliv åt sidan!',
         difficulty='easy', success_condition='escape_check', moves=1,
         fen='k3r3/8/8/8/8/8/8/4K3 w - - 0 1', solution='Kd2'),
    dict(title='Ta den som ger schack', objective='Ta pjäsen som ger schack',
         hint='Damen står precis bredvid din kung och ingen skyddar henne.',
         difficulty='easy', success_condition='capture', target=['queen'], moves=1,
         fen='k7/8/8/8/8/8/4q3/4K3 w - - 0 1', solution='Kxe2'),
    dict(title='Ställ dig i vägen', objective='Blockera schacken',
         hint='Kungen kan inte fly. Ställ löparen mellan tornet och kungen.',
         difficulty='easy', success_condition='escape_check', moves=1,
         fen='7k/8/8/8/2B5/8/5PPP/r5K1 w - - 0 1', solution='Bf1'),
    dict(title='Matt i hörnet', objective='Gör schackmatt',
         hint='Matt = kungen står i schack och kan inte fly. Din kung vaktar g7 och h7.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='7k/8/6K1/8/8/8/8/1Q6 w - - 0 1', solution='Qb8#'),
    dict(title='Matt vid kanten', objective='Gör schackmatt',
         hint='Din kung stänger in den svarta kungen. Ge schack på åttonde raden.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='4k3/8/4K3/8/8/8/8/7Q w - - 0 1', solution='Qh8#'),
    dict(title='Bakre raden', objective='Gör schackmatt med tornet',
         hint='Den svarta kungen är instängd bakom sina egna bönder.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='6k1/5ppp/8/8/8/8/5PPP/3R2K1 w - - 0 1', solution='Rd8#'),
    dict(title='Tornstegen', objective='Gör schackmatt med två torn',
         hint='Tornet på a7 stänger rad 7. Ge schack på rad 8 med det andra tornet.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='7k/R7/8/8/8/8/8/1R4K1 w - - 0 1', solution='Rb8#'),
    dict(title='Damen får hjälp', objective='Gör schackmatt med damen',
         hint='Löparen på d3 skyddar rutan h7.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='5rk1/5pp1/8/7Q/8/3B4/8/6K1 w - - 0 1', solution='Qh7#'),
    dict(title='Hästgaffel', objective='Vinn tornet med en gaffel',
         hint='En gaffel hotar två pjäser samtidigt. Var kan hästen hota både kungen och tornet?',
         difficulty='easy', success_condition='win_material', min_gain=5, moves=2,
         fen='r3k3/8/8/1N6/8/8/8/4K3 w - - 0 1', solution='Nc7+'),
    dict(title='Bondegaffel', objective='Vinn en pjäs med bonden',
         hint='Flytta en bonde så att den hotar både tornet och hästen.',
         difficulty='easy', success_condition='win_material', min_gain=2, moves=2,
         fen='6k1/8/3r1n2/8/3PP3/2P5/8/6K1 w - - 0 1', solution='e5'),

    # ===================== MEDEL: taktik och mattmönster =====================
    dict(title='Kunglig gaffel', objective='Vinn damen med hästen',
         hint='Ge schack med hästen så att den samtidigt hotar damen.',
         difficulty='medium', success_condition='win_material', min_gain=6, moves=2,
         fen='3q3k/6pp/8/6N1/8/8/8/6K1 w - - 0 1', solution='Nf7+'),
    dict(title='Damgaffel', objective='Vinn tornet med damen',
         hint='Ge schack med damen från mitten av brädet. Då hotar hon också tornet i hörnet.',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='r5k1/8/8/8/8/8/8/3Q2K1 w - - 0 1', solution='Qd5+'),
    dict(title='Gaffel bland bönderna', objective='Vinn damen',
         hint='Hästen kan ge schack från e7. Vad mer hotar den därifrån?',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='2q2rk1/5ppp/8/3N4/8/8/5PPP/3R2K1 w - - 0 1', solution='Ne7+'),
    dict(title='Bindning', objective='Vinn damen med en bindning',
         hint='Ställ löparen på b5. Damen kan inte flytta därifrån, för då står kungen i schack.',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='4k3/3q4/8/8/8/2N5/8/4KB2 w - - 0 1', solution='Bb5'),
    dict(title='Bindning och bonde', objective='Vinn hästen',
         hint='Hästen är bunden till kungen och kan inte flytta. Anfall den med en bonde!',
         difficulty='medium', success_condition='win_material', min_gain=2, moves=2,
         fen='4k3/1p6/2n5/1B6/3P4/8/8/4K3 w - - 0 1', solution='d5'),
    dict(title='Spett med tornet', objective='Vinn damen med ett spett',
         hint='Spett: ge schack så att kungen måste flytta. Då kan du ta pjäsen bakom.',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='3k3q/8/8/8/8/8/8/R5K1 w - - 0 1', solution='Ra8+'),
    dict(title='Spett med löparen', objective='Vinn damen med löparen',
         hint='Ge schack längs diagonalen. Damen står bakom kungen.',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='8/5q2/4k3/8/8/8/8/5BK1 w - - 0 1', solution='Bc4+'),
    dict(title='Avtäckt schack', objective='Vinn damen',
         hint='Flytta hästen så att tornet ger schack, och låt hästen hota damen samtidigt.',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='3qk3/8/8/4N3/8/8/8/4R1K1 w - - 0 1', solution='Nc6+'),
    dict(title='Avtäckt angrepp', objective='Vinn tornet',
         hint='Hästen står i vägen för löparen. Flytta den med schack!',
         difficulty='medium', success_condition='win_material', min_gain=4, moves=2,
         fen='7r/4k3/8/8/3N2P1/8/1B6/6K1 w - - 0 1', solution='Nf5+'),
    dict(title='Dubbelschack', objective='Vinn damen med dubbelschack',
         hint='Vid dubbelschack ger två pjäser schack samtidigt. Då måste kungen flytta.',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='2q1k3/8/8/8/4N3/8/8/4R1K1 w - - 0 1', solution='Nd6+'),
    dict(title='Vilken pjäs är fri?', objective='Ta en pjäs som inte är skyddad',
         hint='Hästen på d7 skyddas av kungen. Löparen på h5 skyddas inte av någon.',
         difficulty='medium', success_condition='win_material', min_gain=3, moves=1,
         fen='4k3/3n4/8/7b/8/8/8/3QK3 w - - 0 1', solution='Qxh5+'),
    dict(title='Kvävningsmatt', objective='Gör schackmatt med hästen',
         hint='Kungen är instängd av sina egna pjäser. Hästen kan hoppa in!',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='6rk/6pp/8/4N3/8/8/8/6K1 w - - 0 1', solution='Nf7#'),
    dict(title='Ta och ge matt', objective='Gör schackmatt',
         hint='Du kan ta tornet på e8, och då är det matt!',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='4r1k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1', solution='Rxe8#'),
    dict(title='Arabisk matt', objective='Gör matt med torn och häst',
         hint='Hästen på f6 skyddar h7 och vaktar g8.',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='7k/R7/5N2/8/8/8/8/6K1 w - - 0 1', solution='Rh7#'),
    dict(title='Kungen mellan tornen', objective='Gör schackmatt med damen',
         hint='Kungens egna torn stänger in den. Ge schack från e6.',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='3rkr2/8/8/8/8/1Q6/8/6K1 w - - 0 1', solution='Qe6#'),
    dict(title='Två löpare', objective='Gör schackmatt med löparen',
         hint='Löparen på d5 vaktar g8. Ge schack längs den långa diagonalen.',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='7k/8/6K1/3B4/8/8/8/2B5 w - - 0 1', solution='Bb2#'),
    dict(title='Förvandla genom att ta', objective='Gör bonden till en dam',
         hint='Rutan b8 är blockerad, men bonden kan ta snett och förvandlas på a8.',
         difficulty='medium', success_condition='promotion', moves=1,
         fen='rn5k/1P6/8/8/8/8/8/6K1 w - - 0 1', solution='bxa8=Q'),
    dict(title='Stoppa matten', objective='Stoppa svarts hot om matt',
         hint='Svart hotar matt med tornet på a1. Skydda första raden eller ge kungen en flyktruta.',
         difficulty='medium', success_condition='stop_mate', moves=1,
         fen='r5k1/5ppp/8/8/3R4/8/5PPP/6K1 w - - 0 1', solution='h3'),
    dict(title='Tornstegen i två drag', objective='Gör matt på två drag',
         hint='Tornen turas om: det ena ger schack, det andra stänger raden.',
         difficulty='medium', success_condition='checkmate', moves=2,
         fen='8/4k3/R7/8/8/8/8/1R4K1 w - - 0 1', solution='Rb7+'),
    dict(title='Dubbla torn', objective='Gör matt på två drag',
         hint='Två torn på samma linje är starka. Börja med att ta på e8.',
         difficulty='medium', success_condition='checkmate', moves=2,
         fen='3rr1k1/5ppp/8/8/8/8/4R3/4R1K1 w - - 0 1', solution='Rxe8+'),

    # ===================== SVÅR: kombinationer =====================
    dict(title='Philidors kvävningsmatt', objective='Gör matt på två drag',
         hint='Offra damen på g8! Bara tornet kan ta henne, och sedan kan hästen hoppa in.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='5r1k/6pp/7N/3Q4/8/8/5PPP/6K1 w - - 0 1', solution='Qg8+'),
    dict(title='Avledning', objective='Gör matt på två drag',
         hint='Svarts dam vaktar e8. Locka bort henne med en schack!',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='3q2k1/5ppp/8/1Q6/8/8/5PPP/4R1K1 w - - 0 1', solution='Re8+'),
    dict(title='Dam och torn', objective='Gör matt på två drag',
         hint='Tornet på a6 stänger rad 6. Ge schack med damen på rad 7.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='8/5k2/R7/8/8/8/8/1Q4K1 w - - 0 1', solution='Qb7+'),
    dict(title='Förvandla till häst', objective='Vinn damen',
         hint='Bonden kan bli en häst i stället för en dam, och då ger den gaffel!',
         difficulty='hard', success_condition='capture', target=['queen'], moves=2,
         fen='8/2k1P1q1/8/8/8/8/7K/8 w - - 0 1', solution='e8=N+'),
    dict(title='Damoffer på h7', objective='Gör matt på två drag',
         hint='Offra damen på h7. Sedan kan tornet ge matt på h-linjen.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='5r1k/6pp/8/5P1Q/2B5/3R4/6PP/6K1 w - - 0 1', solution='Qxh7+'),
    dict(title='Bodens matt', objective='Gör matt på två drag',
         hint='Offra damen på c6! Sedan ger löparna matt i kors.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='2kr4/pp1n4/2n5/8/5B2/5Q2/5PPP/5BK1 w - - 0 1', solution='Qxc6+'),
    dict(title='Torn mot bakre raden', objective='Gör matt på två drag',
         hint='Ta tornet på b8. Ditt andra torn står redo bakom.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='1r5k/6pp/1R1q4/8/8/1R2B3/PP6/1K6 w - - 0 1', solution='Rxb8+'),
    dict(title='Slå på f7', objective='Gör matt på två drag',
         hint='Ta bonden på f7 med tornet. Då kan damen komma in på e8.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='6k1/R4p1p/6p1/8/8/1B6/5PPP/4Q1K1 w - - 0 1', solution='Rxf7'),
    dict(title='Tornoffer på g7', objective='Gör matt på två drag',
         hint='Ta bonden på g7 med tornet. Sedan kan hästen ge matt på f7.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='7k/6p1/n2N3p/5N2/6R1/8/PP6/1K6 w - - 0 1', solution='Rxg7'),
    dict(title='Den bundna bonden', objective='Gör matt på två drag',
         hint='Bonden på g7 är bunden av tornet på d7 och kan inte ta. Låt damen hota g7.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='8/3R2pk/n1Q4p/8/8/8/5PPP/6K1 w - - 0 1', solution='Qf6'),
    dict(title='Tornet lockar', objective='Gör matt på två drag',
         hint='Ställ tornet på c6. Det hotar matt på c8, och tar bonden tornet öppnas vägen till e7.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='4k3/3ppp2/4RB2/8/8/8/PPP1Q3/2K5 w - - 0 1', solution='Rc6'),
    dict(title='Sjunde raden', objective='Gör matt på två drag',
         hint='Ett tyst drag utan schack. Ställ tornet på sjunde raden, då hotar damen två matter.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='6k1/6pp/5p2/8/R7/6Q1/5PPP/6K1 w - - 0 1', solution='Ra7'),
    dict(title='Tornet stänger in', objective='Gör matt på två drag',
         hint='Ställ tornet på f7. Då kan damen ge matt på g7.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='8/6pk/7p/4Q3/8/8/PP6/1K3R2 w - - 0 1', solution='Rf7'),
    dict(title='Damen till h6', objective='Gör matt på två drag',
         hint='Löparen vaktar f8. Ställ damen där hon hotar matt på f8.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='6k1/5p1p/6p1/2B5/8/4Q3/5PPP/6K1 w - - 0 1', solution='Qh6'),
    dict(title='Den långa diagonalen', objective='Gör matt på två drag',
         hint='Löparen på d4 siktar på g7. Ställ damen så att hon också hotar g7.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='7k/6p1/7p/8/3B4/8/1Q4PP/7K w - - 0 1', solution='Qb7'),
    dict(title='Hästen vaktar g8', objective='Gör matt på två drag',
         hint='Flytta hästen så att den skyddar g8. Då kan damen ge matt där.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='7k/6p1/2N4p/8/2Q5/8/5PPP/4N1K1 w - - 0 1', solution='Ne7'),
    dict(title='Damen smyger fram', objective='Gör matt på två drag',
         hint='Löparen siktar på b7. Ställ damen nära kungen utan att ge schack.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='1k6/pp6/8/8/Q3B3/8/5PPP/6K1 w - - 0 1', solution='Qd7'),
    dict(title='Två hästar', objective='Gör matt på två drag',
         hint='Damen stänger åttonde raden. Flytta en häst så att den kan ge matt nästa drag.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='1kN3Q1/ppN5/8/8/8/8/6PP/7K w - - 0 1', solution='Nb5'),
    dict(title='Kungen i mitten', objective='Gör matt på två drag',
         hint='Ställ damen på e4. Därifrån hotar hon både a8 och e7.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='4k3/3pppb1/3B4/8/5Q2/8/6PP/7K w - - 0 1', solution='Qe4'),
    dict(title='Tornlyftet', objective='Gör matt på två drag',
         hint='Lyft tornet till g4. Då hotar både tornet och damen bonden på g7.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='7k/B5pp/2n5/8/R7/8/1Q4PP/7K w - - 0 1', solution='Rg4'),
]

_FEN_PIECES = {'p': 'pawn', 'n': 'knight', 'b': 'bishop', 'r': 'rook', 'q': 'queen', 'k': 'king'}


def fen_to_board(fen):
    """Convert the piece placement and side to move of a FEN string.

    Returns (board, king_positions, player_color). Row 0 is rank 8.
    """
    placement, side = fen.split()[:2]
    board = []
    kings = {'white': None, 'black': None}
    for r, rank in enumerate(placement.split('/')):
        row = []
        for ch in rank:
            if ch.isdigit():
                row.extend([None] * int(ch))
            else:
                color = 'white' if ch.isupper() else 'black'
                kind = _FEN_PIECES[ch.lower()]
                if kind == 'king':
                    kings[color] = (r, len(row))
                row.append({'type': kind, 'color': color})
        if len(row) != 8:
            raise ValueError(f"Bad FEN rank {rank!r} in {fen!r}")
        board.append(row)
    if len(board) != 8 or None in kings.values():
        raise ValueError(f"FEN needs 8 ranks and both kings: {fen!r}")
    return board, kings, 'white' if side == 'w' else 'black'


def _build(index, d):
    board, kings, color = fen_to_board(d['fen'])
    p = dict(d)
    p['id'] = f"{d['difficulty']}_{index:02d}"
    p['board'] = board
    p['king_positions'] = kings
    p['player_color'] = color
    return p


CHESS_PROBLEMS = [_build(i, d) for i, d in enumerate(_DEFS, 1)]
