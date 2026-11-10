# -*- coding: utf-8 -*-
"""Schackuppgifter för barn som just lärt sig hur pjäserna går (ca 8-10 år).

Upplägget följer hur nybörjarkurser brukar byggas (t.ex. Lichess "Lär dig
schack" och Stegmetoden): ett tema i taget, korta förklaringar och flera
uppgifter per tema, nästan alla på ett drag. Matt på två drag kommer först
i sista kapitlet.

Varje uppgift skrivs som en FEN-sträng och görs om till spelets bräde när
modulen laddas. test_problems.py kontrollerar att varje ställning är laglig
(båda kungarna finns) och att målet går att nå mot alla motdrag.

Fält i varje uppgift:
  title, objective, hint   texter som visas i spelet
  chapter                  index i CHAPTERS
  difficulty               'easy' | 'medium' | 'hard'
  fen                      ställningen; den som ska dra är spelaren
  success_condition        målet, se problem_checker.py
  moves                    hur många drag spelaren får göra
  target                   pjästyper för 'capture' / 'save_piece'
  min_gain                 hur mycket material som ska vinnas ('win_material')
  solution                 ett rätt första drag (SAN), används av testerna
"""

# Kapitel: rubrik och en kort förklaring som visas i listan
CHAPTERS = [
    ('Slå pjäser', 'Ta motståndarens pjäser. Värde: bonde 1, häst 3, löpare 3, torn 5, dam 9.'),
    ('Skydda dina pjäser', 'När en pjäs hotas: flytta den till en säker ruta eller skydda den.'),
    ('Schack', 'Schack betyder att du hotar kungen.'),
    ('Ur schack', 'Tre sätt att klara en schack: flytta kungen, ta pjäsen eller ställ något i vägen.'),
    ('Schackmatt', 'Matt: kungen står i schack och kan inte komma undan. Då är partiet slut!'),
    ('Matt – inte patt!', 'Patt: kungen står inte i schack men kan inte flytta. Då blir det oavgjort.'),
    ('Bonden blir dam', 'En bonde som når sista raden förvandlas till en ny pjäs.'),
    ('Gaffel', 'En gaffel hotar två pjäser på en gång. Motståndaren kan bara rädda en.'),
    ('Bindning och spett', 'Pjäser på samma linje som kungen kan bli fångade.'),
    ('Avtäckt schack', 'Flytta en pjäs ur vägen, så ger pjäsen bakom schack.'),
    ('Försvar', 'Se vad motståndaren hotar innan du drar.'),
    ('Matt på två drag', 'Tänk ett drag längre: vad händer efter motståndarens svar?'),
]

_DEFS = [
    # ===================== 1. Slå pjäser =====================
    dict(chapter=0, title='Tornet tar', objective='Ta hästen med tornet',
         hint='Tornet (boken) går rakt: upp, ner och åt sidan. Hästen står på a4.',
         difficulty='easy', success_condition='capture', target=['knight'], moves=1,
         fen='7k/8/8/8/n7/8/8/R3K3 w - - 0 1', solution='Rxa4'),
    dict(chapter=0, title='Löparen tar', objective='Ta tornet med löparen',
         hint='Löparen (klumpfisken) går snett. Följ diagonalen från c1 upp till h6.',
         difficulty='easy', success_condition='capture', target=['rook'], moves=1,
         fen='7k/8/7r/8/8/8/8/2B1K3 w - - 0 1', solution='Bxh6'),
    dict(chapter=0, title='Hästen hoppar', objective='Ta damen med hästen',
         hint='Hästen hoppar som ett L: två steg åt ett håll och ett steg åt sidan.',
         difficulty='easy', success_condition='capture', target=['queen'], moves=1,
         fen='4k3/8/8/3q4/8/2N5/8/4K3 w - - 0 1', solution='Nxd5'),
    dict(chapter=0, title='Bonden tar snett', objective='Ta hästen med bonden',
         hint='Bonden (ankungen) går rakt fram, men den tar snett framåt.',
         difficulty='easy', success_condition='capture', target=['knight'], moves=1,
         fen='4k3/8/8/3np3/4P3/8/8/4K3 w - - 0 1', solution='exd5'),
    dict(chapter=0, title='Kungen tar', objective='Ta tornet med kungen',
         hint='Kungen (hunden) går ett steg åt alla håll. Ingen skyddar tornet!',
         difficulty='easy', success_condition='capture', target=['rook'], moves=1,
         fen='4k3/8/8/8/8/8/3r4/4K3 w - - 0 1', solution='Kxd2'),
    dict(chapter=0, title='Ta det bästa', objective='Ta den pjäs som är mest värd',
         hint='Hästen kan ta tre pjäser. Tornet är värt 5, löparen 3 och bonden 1.',
         difficulty='easy', success_condition='win_material', min_gain=5, moves=1,
         fen='7k/8/2p1r3/8/3N4/5b2/8/6K1 w - - 0 1', solution='Nxe6'),
    dict(chapter=0, title='Vilken pjäs är fri?', objective='Ta en pjäs som inte är skyddad',
         hint='Hästen på d7 skyddas av kungen. Löparen på h5 skyddas inte av någon.',
         difficulty='easy', success_condition='win_material', min_gain=3, moves=1,
         fen='4k3/3n4/8/7b/8/8/8/3QK3 w - - 0 1', solution='Qxh5+'),

    # ===================== 2. Skydda dina pjäser =====================
    dict(chapter=1, title='Rädda damen', objective='Flytta damen i säkerhet',
         hint='Bonden på e5 hotar damen. Hitta en ruta där ingen kan ta henne.',
         difficulty='easy', success_condition='save_piece', target=['queen'], moves=1,
         fen='6k1/8/8/4p3/3Q4/8/8/6K1 w - - 0 1', solution='Qd3'),
    dict(chapter=1, title='Rädda tornet', objective='Flytta tornet i säkerhet',
         hint='Löparen går snett. Se upp för rutorna på hans diagonaler!',
         difficulty='easy', success_condition='save_piece', target=['rook'], moves=1,
         fen='7k/8/5b2/8/3R4/8/8/6K1 w - - 0 1', solution='Rb4'),
    dict(chapter=1, title='Skydda bonden', objective='Skydda bonden på e4',
         hint='Hästen hotar bonden. Ställ en pjäs så att den skyddar e4, eller flytta bonden.',
         difficulty='easy', success_condition='save_piece', target=['pawn'], moves=1,
         fen='6k1/5ppp/5n2/8/4P3/8/3P1PPP/1N4K1 w - - 0 1', solution='d3'),

    # ===================== 3. Schack =====================
    dict(chapter=2, title='Schack med tornet', objective='Ge schack med tornet',
         hint='Ställ tornet på samma rad eller linje som kungen.',
         difficulty='easy', success_condition='check', moves=1,
         fen='4k3/8/8/8/8/8/8/R5K1 w - - 0 1', solution='Ra8+'),
    dict(chapter=2, title='Schack med hästen', objective='Ge schack med hästen',
         hint='Vilka rutor kan hästen hoppa till? Hitta en som hotar kungen på e8.',
         difficulty='easy', success_condition='check', moves=1,
         fen='4k3/8/8/8/4N3/8/8/4K3 w - - 0 1', solution='Nf6+'),
    dict(chapter=2, title='Schack med löparen', objective='Ge schack med löparen',
         hint='Följ diagonalerna från kungen på e8. Var kan löparen ställa sig?',
         difficulty='easy', success_condition='check', moves=1,
         fen='4k3/8/8/8/8/8/8/4KB2 w - - 0 1', solution='Bb5+'),
    dict(chapter=2, title='Schack med bonden', objective='Ge schack med bonden',
         hint='Bonden hotar rutorna snett framför sig.',
         difficulty='easy', success_condition='check', moves=1,
         fen='4k3/8/3P4/8/8/8/8/4K3 w - - 0 1', solution='d7+'),

    # ===================== 4. Ur schack =====================
    dict(chapter=3, title='Kliv undan', objective='Flytta kungen ur schack',
         hint='Tornet hotar hela e-linjen. Kliv åt sidan!',
         difficulty='easy', success_condition='escape_check', moves=1,
         fen='k3r3/8/8/8/8/8/8/4K3 w - - 0 1', solution='Kd2'),
    dict(chapter=3, title='Ta den som ger schack', objective='Ta pjäsen som ger schack',
         hint='Damen står precis bredvid din kung och ingen skyddar henne.',
         difficulty='easy', success_condition='capture', target=['queen'], moves=1,
         fen='k7/8/8/8/8/8/4q3/4K3 w - - 0 1', solution='Kxe2'),
    dict(chapter=3, title='Ställ dig i vägen', objective='Blockera schacken',
         hint='Kungen kan inte fly. Ställ löparen mellan tornet och kungen.',
         difficulty='easy', success_condition='escape_check', moves=1,
         fen='7k/8/8/8/2B5/8/5PPP/r5K1 w - - 0 1', solution='Bf1'),
    dict(chapter=3, title='Hästen ger schack', objective='Ta hästen som ger schack',
         hint='En häst kan man inte blockera, den hoppar. Men en bonde kan ta den!',
         difficulty='easy', success_condition='capture', target=['knight'], moves=1,
         fen='7k/8/8/8/8/5n2/5PPP/6K1 w - - 0 1', solution='gxf3'),

    # ===================== 5. Schackmatt =====================
    dict(chapter=4, title='Matt i hörnet', objective='Gör schackmatt',
         hint='Din kung vaktar g7 och h7. Ge schack så att kungen inte kan fly.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='7k/8/6K1/8/8/8/8/1Q6 w - - 0 1', solution='Qb8#'),
    dict(chapter=4, title='Matt vid kanten', objective='Gör schackmatt',
         hint='Din kung stänger in den svarta kungen. Ge schack på åttonde raden.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='4k3/8/4K3/8/8/8/8/7Q w - - 0 1', solution='Qh8#'),
    dict(chapter=4, title='Bakre raden', objective='Gör schackmatt med tornet',
         hint='Den svarta kungen är instängd bakom sina egna bönder.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='6k1/5ppp/8/8/8/8/5PPP/3R2K1 w - - 0 1', solution='Rd8#'),
    dict(chapter=4, title='Tornstegen', objective='Gör schackmatt med två torn',
         hint='Tornet på a7 stänger rad 7. Ge schack på rad 8 med det andra tornet.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='7k/R7/8/8/8/8/8/1R4K1 w - - 0 1', solution='Rb8#'),
    dict(chapter=4, title='Dam och torn', objective='Gör schackmatt',
         hint='Tornet på g1 stänger g-linjen. Ge schack med damen på h-linjen.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='7k/8/8/8/8/8/3Q4/6RK w - - 0 1', solution='Qh2#'),
    dict(chapter=4, title='Damen får hjälp', objective='Gör schackmatt med damen',
         hint='Löparen på d3 skyddar rutan h7.',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='5rk1/5pp1/8/7Q/8/3B4/8/6K1 w - - 0 1', solution='Qh7#'),
    dict(chapter=4, title='Ta och ge matt', objective='Gör schackmatt',
         hint='Du kan ta tornet på e8, och då är det matt!',
         difficulty='easy', success_condition='checkmate', moves=1,
         fen='4r1k1/5ppp/8/8/8/8/5PPP/4R1K1 w - - 0 1', solution='Rxe8#'),
    dict(chapter=4, title='Kvävningsmatt', objective='Gör schackmatt med hästen',
         hint='Kungen är instängd av sina egna pjäser. Hästen kan hoppa in!',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='6rk/6pp/8/4N3/8/8/8/6K1 w - - 0 1', solution='Nf7#'),
    dict(chapter=4, title='Torn och häst', objective='Gör matt med torn och häst',
         hint='Hästen på f6 skyddar h7 och vaktar g8.',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='7k/R7/5N2/8/8/8/8/6K1 w - - 0 1', solution='Rh7#'),
    dict(chapter=4, title='Kungen mellan tornen', objective='Gör schackmatt med damen',
         hint='Kungens egna torn stänger in den. Ge schack från e6.',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='3rkr2/8/8/8/8/1Q6/8/6K1 w - - 0 1', solution='Qe6#'),
    dict(chapter=4, title='Två löpare', objective='Gör schackmatt med löparen',
         hint='Löparen på d5 vaktar g8. Ge schack längs den långa diagonalen.',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='7k/8/6K1/3B4/8/8/8/2B5 w - - 0 1', solution='Bb2#'),

    # ===================== 6. Matt – inte patt! =====================
    dict(chapter=5, title='Akta dig för patt', objective='Gör matt – inte patt!',
         hint='Om damen bara stänger in kungen utan schack blir det patt. Ge schack!',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='k7/2K5/8/8/8/8/8/1Q6 w - - 0 1', solution='Qb7#'),
    dict(chapter=5, title='Tornet och patt', objective='Gör matt – inte patt!',
         hint='Ställer du tornet på g-linjen kan kungen inte röra sig, men det är inte schack. Ge schack!',
         difficulty='medium', success_condition='checkmate', moves=1,
         fen='7k/8/6K1/8/8/8/8/R7 w - - 0 1', solution='Ra8#'),

    # ===================== 7. Bonden blir dam =====================
    dict(chapter=6, title='Bonden blir dam', objective='Gör bonden till en dam',
         hint='Flytta bonden till sista raden och välj en dam.',
         difficulty='easy', success_condition='promotion', moves=1,
         fen='7k/P7/8/8/8/8/8/4K3 w - - 0 1', solution='a8=Q+'),
    dict(chapter=6, title='Förvandla genom att ta', objective='Gör bonden till en dam',
         hint='Rutan b8 är blockerad, men bonden kan ta snett och förvandlas på a8.',
         difficulty='easy', success_condition='promotion', moves=1,
         fen='rn5k/1P6/8/8/8/8/8/6K1 w - - 0 1', solution='bxa8=Q'),
    dict(chapter=6, title='Spring, bonden!', objective='Förvandla bonden på tre drag',
         hint='Den svarta kungen hinner inte ikapp. Gå rakt fram varje drag!',
         difficulty='medium', success_condition='promotion', moves=3,
         fen='8/8/8/2P5/7k/8/8/6K1 w - - 0 1', solution='c6'),

    # ===================== 8. Gaffel =====================
    dict(chapter=7, title='Hästgaffel', objective='Vinn tornet med en gaffel',
         hint='Var kan hästen hota både kungen och tornet samtidigt?',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='r3k3/8/8/1N6/8/8/8/4K3 w - - 0 1', solution='Nc7+'),
    dict(chapter=7, title='Kunglig gaffel', objective='Vinn damen med hästen',
         hint='Ge schack med hästen så att den samtidigt hotar damen.',
         difficulty='medium', success_condition='win_material', min_gain=6, moves=2,
         fen='3q3k/6pp/8/6N1/8/8/8/6K1 w - - 0 1', solution='Nf7+'),
    dict(chapter=7, title='Bondegaffel', objective='Vinn en pjäs med bonden',
         hint='Flytta en bonde så att den hotar både tornet och hästen.',
         difficulty='medium', success_condition='win_material', min_gain=2, moves=2,
         fen='6k1/8/3r1n2/8/3PP3/2P5/8/6K1 w - - 0 1', solution='e5'),
    dict(chapter=7, title='Damgaffel', objective='Vinn tornet med damen',
         hint='Ge schack med damen från mitten av brädet. Då hotar hon också tornet i hörnet.',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='r5k1/8/8/8/8/8/8/3Q2K1 w - - 0 1', solution='Qd5+'),
    dict(chapter=7, title='Gaffel bland bönderna', objective='Vinn damen',
         hint='Hästen kan ge schack från e7. Vad mer hotar den därifrån?',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='2q2rk1/5ppp/8/3N4/8/8/5PPP/3R2K1 w - - 0 1', solution='Ne7+'),

    # ===================== 9. Bindning och spett =====================
    dict(chapter=8, title='Bindning', objective='Vinn damen med en bindning',
         hint='Ställ löparen på b5. Damen kan inte flytta därifrån, för då står kungen i schack.',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='4k3/3q4/8/8/8/2N5/8/4KB2 w - - 0 1', solution='Bb5'),
    dict(chapter=8, title='Bindning och bonde', objective='Vinn hästen',
         hint='Hästen är bunden till kungen och kan inte flytta. Anfall den med en bonde!',
         difficulty='medium', success_condition='win_material', min_gain=2, moves=2,
         fen='4k3/1p6/2n5/1B6/3P4/8/8/4K3 w - - 0 1', solution='d5'),
    dict(chapter=8, title='Spett med tornet', objective='Vinn damen med ett spett',
         hint='Spett: ge schack så att kungen måste flytta. Då kan du ta pjäsen bakom.',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='3k3q/8/8/8/8/8/8/R5K1 w - - 0 1', solution='Ra8+'),
    dict(chapter=8, title='Spett med löparen', objective='Vinn damen med löparen',
         hint='Ge schack längs diagonalen. Damen står bakom kungen.',
         difficulty='medium', success_condition='win_material', min_gain=5, moves=2,
         fen='8/5q2/4k3/8/8/8/8/5BK1 w - - 0 1', solution='Bc4+'),

    # ===================== 10. Avtäckt schack =====================
    dict(chapter=9, title='Avtäckt schack', objective='Vinn damen',
         hint='Flytta hästen så att tornet ger schack, och låt hästen hota damen samtidigt.',
         difficulty='hard', success_condition='win_material', min_gain=5, moves=2,
         fen='3qk3/8/8/4N3/8/8/8/4R1K1 w - - 0 1', solution='Nc6+'),
    dict(chapter=9, title='Dubbelschack', objective='Vinn damen med dubbelschack',
         hint='Vid dubbelschack ger två pjäser schack samtidigt. Då måste kungen flytta.',
         difficulty='hard', success_condition='win_material', min_gain=5, moves=2,
         fen='2q1k3/8/8/8/4N3/8/8/4R1K1 w - - 0 1', solution='Nd6+'),

    # ===================== 11. Försvar =====================
    dict(chapter=10, title='Stoppa matten', objective='Stoppa svarts hot om matt',
         hint='Svart hotar matt med tornet på a1. Skydda första raden eller ge kungen en flyktruta.',
         difficulty='medium', success_condition='stop_mate', moves=1,
         fen='r5k1/5ppp/8/8/3R4/8/5PPP/6K1 w - - 0 1', solution='h3'),

    # ===================== 12. Matt på två drag =====================
    dict(chapter=11, title='Tornstegen i två drag', objective='Gör matt på två drag',
         hint='Tornen turas om: det ena ger schack, det andra stänger raden.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='8/4k3/R7/8/8/8/8/1R4K1 w - - 0 1', solution='Rb7+'),
    dict(chapter=11, title='Dam och torn i två drag', objective='Gör matt på två drag',
         hint='Tornet på a6 stänger rad 6. Ge schack med damen på rad 7.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='8/5k2/R7/8/8/8/8/1Q4K1 w - - 0 1', solution='Qb7+'),
    dict(chapter=11, title='Dubbla torn', objective='Gör matt på två drag',
         hint='Två torn på samma linje är starka. Börja med att ta på e8.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='3rr1k1/5ppp/8/8/8/8/4R3/4R1K1 w - - 0 1', solution='Rxe8+'),
    dict(chapter=11, title='Torn mot bakre raden', objective='Gör matt på två drag',
         hint='Ta tornet på b8. Ditt andra torn står redo bakom.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='1r5k/6pp/1R1q4/8/8/1R2B3/PP6/1K6 w - - 0 1', solution='Rxb8+'),
    dict(chapter=11, title='Superproblemet', objective='Gör matt på två drag',
         hint='Offra damen på g8! Bara tornet kan ta henne, och sedan kan hästen hoppa in.',
         difficulty='hard', success_condition='checkmate', moves=2,
         fen='5r1k/6pp/7N/3Q4/8/8/5PPP/6K1 w - - 0 1', solution='Qg8+'),
]

_FEN_PIECES = {'p': 'pawn', 'n': 'knight', 'b': 'bishop', 'r': 'rook', 'q': 'queen', 'k': 'king'}


def fen_to_board(fen):
    """Gör om pjäsplaceringen och vem som drar i en FEN-sträng.

    Returnerar (board, king_positions, player_color). Rad 0 är rad 8 på brädet.
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
            raise ValueError(f"Fel i FEN-raden {rank!r} i {fen!r}")
        board.append(row)
    if len(board) != 8 or None in kings.values():
        raise ValueError(f"FEN måste ha 8 rader och båda kungarna: {fen!r}")
    return board, kings, 'white' if side == 'w' else 'black'


def _build(index, d):
    board, kings, color = fen_to_board(d['fen'])
    p = dict(d)
    p['id'] = f"k{d['chapter'] + 1:02d}_{index:02d}"
    p['board'] = board
    p['king_positions'] = kings
    p['player_color'] = color
    return p


CHESS_PROBLEMS = [_build(i, d) for i, d in enumerate(_DEFS, 1)]
