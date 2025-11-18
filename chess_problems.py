# -*- coding: utf-8 -*-
"""Chess problems suitable for 8-year-olds - Extended collection"""

# Each problem has:
# - title: Swedish name of the problem
# - objective: What the player needs to achieve (in Swedish)
# - difficulty: 'easy', 'medium', or 'hard'
# - player_color: 'white' or 'black' (which color the player controls)
# - board: Initial board setup
# - solution_moves: Expected winning moves
# - hint: Helpful hint in Swedish
# - success_condition: How to detect success ('checkmate', 'material_advantage', 'position')

CHESS_PROBLEMS = [
    # ============= LÄTTA PROBLEM (1-20) =============
    {
        'id': 'easy_01',
        'title': 'En-drags matt',
        'objective': 'Gör schackmatt på ett drag',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Damen kan flytta till hörnet!',
        'success_condition': 'checkmate',
        'board': [
            [{'type': 'king', 'color': 'black'}, None, None, None, None, None, None, None],
            [{'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, {'type': 'queen', 'color': 'white'}]
        ],
        'king_positions': {'white': None, 'black': (0, 0)}
    },
    {
        'id': 'easy_02',
        'title': 'Tornen jobbar tillsammans',
        'objective': 'Använd båda tornen för matt',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Flytta ett torn till rad 8!',
        'success_condition': 'checkmate',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, {'type': 'rook', 'color': 'white'}],
            [None, None, None, None, None, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': None, 'black': (0, 4)}
    },
    {
        'id': 'easy_03',
        'title': 'Ta den fria pjäsen',
        'objective': 'Ta den svarta damen',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Din springare kan hoppa dit!',
        'success_condition': 'material_advantage',
        'target_capture': 'queen',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'queen', 'color': 'black'}, None, None, None, None],
            [None, None, None, None, None, {'type': 'knight', 'color': 'white'}, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_04',
        'title': 'Gaffel-attack',
        'objective': 'Attackera kung och torn samtidigt',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Springaren kan hota båda!',
        'success_condition': 'fork_check',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, {'type': 'rook', 'color': 'black'}, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'knight', 'color': 'white'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_05',
        'title': 'Bonde blir dam',
        'objective': 'Befordra bonden till dam',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Flytta bonden ett steg framåt!',
        'success_condition': 'promotion',
        'board': [
            [{'type': 'king', 'color': 'black'}, None, None, None, None, None, None, None],
            [None, {'type': 'pawn', 'color': 'white'}, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, {'type': 'king', 'color': 'white'}, None, None, None, None, None]
        ],
        'king_positions': {'white': (7, 2), 'black': (0, 0)}
    },
    {
        'id': 'easy_06',
        'title': 'Grundraden matt',
        'objective': 'Matt på grundraden',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Tornet till rad 8!',
        'success_condition': 'checkmate',
        'board': [
            [None, None, None, None, None, {'type': 'king', 'color': 'black'}, None, None],
            [None, None, None, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': None, 'black': (0, 5)}
    },
    {
        'id': 'easy_07',
        'title': 'Dubbel-attack',
        'objective': 'Hota kungen med schack',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Damen kan ge schack!',
        'success_condition': 'check',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'queen', 'color': 'white'}, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_08',
        'title': 'Löpare-matt',
        'objective': 'Matt med två löpare',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Löparen kan komma till hörnet!',
        'success_condition': 'checkmate',
        'board': [
            [{'type': 'king', 'color': 'black'}, None, None, None, None, None, None, None],
            [None, {'type': 'bishop', 'color': 'white'}, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, {'type': 'bishop', 'color': 'white'}, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 0)}
    },
    {
        'id': 'easy_09',
        'title': 'Ta med check',
        'objective': 'Ta pjäsen och ge schack',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Damen kan ta OCH ge schack!',
        'success_condition': 'check',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, {'type': 'rook', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'queen', 'color': 'white'}, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_10',
        'title': 'Springare till centrum',
        'objective': 'Flytta springaren till centrum',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Centrum är e4 eller d4!',
        'success_condition': 'piece_to_center',
        'target_piece': 'knight',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'knight', 'color': 'white'}, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_11',
        'title': 'Dam mot torn',
        'objective': 'Byt din dam mot tornet',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Ta tornet med damen!',
        'success_condition': 'material_advantage',
        'target_capture': 'rook',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'rook', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'queen', 'color': 'white'}, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_12',
        'title': 'Blockera schacken',
        'objective': 'Blockera den svarta damens schack',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Flytta löparen emellan!',
        'success_condition': 'escape_check',
        'board': [
            [None, None, None, None, None, None, None, {'type': 'queen', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, {'type': 'bishop', 'color': 'white'}, None],
            [None, None, None, None, None, None, None, {'type': 'king', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 7), 'black': None}
    },
    {
        'id': 'easy_13',
        'title': 'Två bönder framåt',
        'objective': 'Flytta båda bönderna framåt',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Bönder kan gå två steg först!',
        'success_condition': 'pawns_advanced',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_14',
        'title': 'Dubbel schack',
        'objective': 'Ge schack med båda pjäserna',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Flytta damen så den ger schack!',
        'success_condition': 'check',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'rook', 'color': 'white'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'queen', 'color': 'white'}, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_15',
        'title': 'Rädda tornet',
        'objective': 'Flytta tornet från faran',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Flytta bort tornet från damens linje!',
        'success_condition': 'piece_safe',
        'target_piece': 'rook',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'queen', 'color': 'black'}, None, None, None, {'type': 'rook', 'color': 'white'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_16',
        'title': 'Kungen går',
        'objective': 'Flytta kungen till säkerheten',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Kungen kan gå ett steg!',
        'success_condition': 'king_safe',
        'board': [
            [None, None, None, None, None, None, None, {'type': 'rook', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, {'type': 'king', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 7), 'black': None}
    },
    {
        'id': 'easy_17',
        'title': 'Ta den hotande pjäsen',
        'objective': 'Ta pjäsen som hotar kungen',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Damen kan ta löparen!',
        'success_condition': 'threat_removed',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, {'type': 'bishop', 'color': 'black'}, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'queen', 'color': 'white'}, None, None, None, None, None, None, {'type': 'king', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 7), 'black': (0, 4)}
    },
    {
        'id': 'easy_18',
        'title': 'Utveckla löparen',
        'objective': 'Flytta löparen från startplatsen',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Löparen kan gå diagonalt!',
        'success_condition': 'piece_developed',
        'target_piece': 'bishop',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'pawn', 'color': 'white'}, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, {'type': 'bishop', 'color': 'white'}, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_19',
        'title': 'Enkel gaffel',
        'objective': 'Hota två pjäser samtidigt',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Springaren kan hoppa!',
        'success_condition': 'fork',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'rook', 'color': 'black'}, None, {'type': 'rook', 'color': 'black'}, None, None],
            [None, None, None, None, {'type': 'knight', 'color': 'white'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'easy_20',
        'title': 'Matt med dam och kung',
        'objective': 'Gör matt med kung och dam',
        'difficulty': 'easy',
        'player_color': 'white',
        'hint': 'Damen till rad 8!',
        'success_condition': 'checkmate',
        'board': [
            [None, None, None, None, None, None, None, {'type': 'king', 'color': 'black'}],
            [None, None, None, None, None, None, {'type': 'king', 'color': 'white'}, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, {'type': 'queen', 'color': 'white'}]
        ],
        'king_positions': {'white': (1, 6), 'black': (0, 7)}
    },

    # ============= MEDEL PROBLEM (21-40) =============
    {
        'id': 'medium_01',
        'title': 'Dubbel-attack taktik',
        'objective': 'Gör en gaffel och vinn material',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Springaren kan attackera två pjäser!',
        'success_condition': 'fork',
        'board': [
            [{'type': 'rook', 'color': 'black'}, None, None, None, {'type': 'king', 'color': 'black'}, None, None, {'type': 'rook', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'knight', 'color': 'white'}, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_02',
        'title': 'Bakre radens matt',
        'objective': 'Gör schackmatt på bakre raden',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Tornet kan köra till rad 8!',
        'success_condition': 'checkmate',
        'board': [
            [None, None, None, None, None, {'type': 'king', 'color': 'black'}, None, None],
            [None, None, None, None, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'rook', 'color': 'white'}, None, {'type': 'king', 'color': 'white'}, None, None]
        ],
        'king_positions': {'white': (7, 5), 'black': (0, 5)}
    },
    {
        'id': 'medium_03',
        'title': 'Discovered attack',
        'objective': 'Flytta pjäsen för att avslöja attack',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Flytta springaren för att löparen attackerar!',
        'success_condition': 'discovered_attack',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'queen', 'color': 'black'}, None, None, None],
            [None, None, None, None, {'type': 'knight', 'color': 'white'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'bishop', 'color': 'white'}, None, None, {'type': 'king', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 7), 'black': (0, 4)}
    },
    {
        'id': 'medium_04',
        'title': 'Pin-taktik',
        'objective': 'Fäst en pjäs mot kungen',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Löparen kan fästa damen!',
        'success_condition': 'pin',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'queen', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'bishop', 'color': 'white'}, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_05',
        'title': 'Bonde-genombrott',
        'objective': 'För bonden till förvandling',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Täck bonden med kungen!',
        'success_condition': 'promotion',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'pawn', 'color': 'white'}, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'king', 'color': 'white'}, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ],
        'king_positions': {'white': (6, 3), 'black': (0, 4)}
    },
    {
        'id': 'medium_06',
        'title': 'Avledning',
        'objective': 'Led bort försvaret',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Offra tornet för att dra bort damen!',
        'success_condition': 'deflection',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, {'type': 'queen', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'rook', 'color': 'white'}, None, None, None, {'type': 'king', 'color': 'white'}, None, None, {'type': 'queen', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_07',
        'title': 'Kvitto-schack',
        'objective': 'Ge schack tillbaka och vinn',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Damen kan ge kontra-schack!',
        'success_condition': 'counter_check',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'queen', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'queen', 'color': 'white'}, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_08',
        'title': 'Tre-drags matt',
        'objective': 'Schackmatt på tre drag',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Damen och torn samarbetar!',
        'success_condition': 'checkmate',
        'max_moves': 3,
        'board': [
            [None, None, None, None, None, {'type': 'king', 'color': 'black'}, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, {'type': 'rook', 'color': 'white'}],
            [{'type': 'queen', 'color': 'white'}, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 5)}
    },
    {
        'id': 'medium_09',
        'title': 'Dubbelschack',
        'objective': 'Ge dubbelschack',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Flytta springaren för schack från två håll!',
        'success_condition': 'double_check',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'knight', 'color': 'white'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'rook', 'color': 'white'}, None, None, {'type': 'king', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 7), 'black': (0, 4)}
    },
    {
        'id': 'medium_10',
        'title': 'Springare-matt',
        'objective': 'Matt med springare',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Springaren hoppar till kungen!',
        'success_condition': 'checkmate',
        'board': [
            [None, None, None, None, None, None, None, {'type': 'king', 'color': 'black'}],
            [None, None, None, None, None, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, {'type': 'knight', 'color': 'white'}, None, None],
            [None, None, None, None, None, None, {'type': 'queen', 'color': 'white'}, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 7)}
    },
    # Continuing medium problems...
    {
        'id': 'medium_11',
        'title': 'Bonde-kil',
        'objective': 'Använd bonden för att dela motståndaren',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Bonden kan störa koordinationen!',
        'success_condition': 'pawn_wedge',
        'board': [
            [{'type': 'rook', 'color': 'black'}, None, None, None, {'type': 'king', 'color': 'black'}, None, None, {'type': 'rook', 'color': 'black'}],
            [None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'pawn', 'color': 'white'}, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, None, None, None, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_12',
        'title': 'Springare-gaffel på kung och dam',
        'objective': 'Gaffla kung och dam',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Springaren kan attackera båda!',
        'success_condition': 'royal_fork',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, {'type': 'queen', 'color': 'black'}, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'knight', 'color': 'white'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_13',
        'title': 'Kontrollera öppna linjen',
        'objective': 'Dominera den öppna linjen med torn',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Flytta tornet till e-linjen!',
        'success_condition': 'control_open_file',
        'target_file': 4,  # e-file (0-indexed)
        'board': [
            [{'type': 'rook', 'color': 'black'}, None, None, None, {'type': 'king', 'color': 'black'}, None, None, {'type': 'rook', 'color': 'black'}],
            [{'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, None, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}],
            [{'type': 'rook', 'color': 'white'}, None, None, None, {'type': 'king', 'color': 'white'}, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_14',
        'title': 'Förstör försvaret',
        'objective': 'Ta den försvarande pjäsen',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Ta tornet som försvarar!',
        'success_condition': 'remove_defender',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, {'type': 'rook', 'color': 'black'}],
            [None, None, None, None, None, None, None, {'type': 'queen', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'rook', 'color': 'white'}, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_15',
        'title': 'Tvingad rokad',
        'objective': 'Tvinga motståndaren att förlora roken',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Använd schack för att tvinga drag!',
        'success_condition': 'forced_move_advantage',
        'board': [
            [{'type': 'rook', 'color': 'black'}, None, None, None, {'type': 'king', 'color': 'black'}, None, None, {'type': 'rook', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'queen', 'color': 'white'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_16',
        'title': 'Kontrollera centrum',
        'objective': 'Placera båda riddarna i centrum',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Riddare är starka i centrum!',
        'success_condition': 'knights_centralized',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, {'type': 'knight', 'color': 'white'}, None, None, {'type': 'knight', 'color': 'white'}, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, None]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_17',
        'title': 'Upptäck angreppet',
        'objective': 'Avslöja ett kraftfullt angrepp',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Flytta löparen!',
        'success_condition': 'discovered_check',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'bishop', 'color': 'white'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'rook', 'color': 'white'}, None, None, {'type': 'king', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 7), 'black': (0, 4)}
    },
    {
        'id': 'medium_18',
        'title': 'Svag punkt f7',
        'objective': 'Attackera den svaga f7-bonden',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Både löpare och dam kan attackera!',
        'success_condition': 'attack_f7',
        'board': [
            [{'type': 'rook', 'color': 'black'}, {'type': 'knight', 'color': 'black'}, {'type': 'bishop', 'color': 'black'}, {'type': 'queen', 'color': 'black'}, {'type': 'king', 'color': 'black'}, None, None, {'type': 'rook', 'color': 'black'}],
            [{'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'pawn', 'color': 'white'}, None, None, None],
            [None, None, None, None, None, {'type': 'bishop', 'color': 'white'}, None, None],
            [{'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, None, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}],
            [{'type': 'rook', 'color': 'white'}, {'type': 'knight', 'color': 'white'}, None, {'type': 'queen', 'color': 'white'}, {'type': 'king', 'color': 'white'}, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_19',
        'title': 'Skydda bonden',
        'objective': 'Stöd bonden till förvandling',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Tornet bakom bonden!',
        'success_condition': 'supported_pawn',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'pawn', 'color': 'white'}, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'medium_20',
        'title': 'Trappstege-matt',
        'objective': 'Jaga kungen till kanten',
        'difficulty': 'medium',
        'player_color': 'white',
        'hint': 'Använd tornen i tur och ordning!',
        'success_condition': 'ladder_mate',
        'board': [
            [None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, {'type': 'rook', 'color': 'white'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'king', 'color': 'white'}, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },

    # ============= SVÅRA PROBLEM (41-60) =============
    {
        'id': 'hard_01',
        'title': 'Kombinationsangrepp',
        'objective': 'Vinn material genom kombination',
        'difficulty': 'hard',
        'player_color': 'white',
        'hint': 'Offra först, attackera sedan!',
        'success_condition': 'material_advantage',
        'target_advantage': 5,
        'board': [
            [{'type': 'rook', 'color': 'black'}, None, {'type': 'bishop', 'color': 'black'}, {'type': 'queen', 'color': 'black'}, {'type': 'king', 'color': 'black'}, None, None, {'type': 'rook', 'color': 'black'}],
            [{'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}],
            [None, None, {'type': 'knight', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None, {'type': 'knight', 'color': 'black'}, None, None],
            [None, None, None, None, {'type': 'pawn', 'color': 'black'}, None, None, None],
            [None, None, None, None, {'type': 'pawn', 'color': 'white'}, None, None, None],
            [None, None, {'type': 'knight', 'color': 'white'}, None, None, {'type': 'knight', 'color': 'white'}, None, None],
            [{'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, None, None, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}],
            [{'type': 'rook', 'color': 'white'}, None, {'type': 'bishop', 'color': 'white'}, {'type': 'queen', 'color': 'white'}, {'type': 'king', 'color': 'white'}, {'type': 'bishop', 'color': 'white'}, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    {
        'id': 'hard_02',
        'title': 'Ersättnings-offer',
        'objective': 'Offra för att vinna större',
        'difficulty': 'hard',
        'player_color': 'white',
        'hint': 'Offra damen!',
        'success_condition': 'sacrifice_and_win',
        'board': [
            [{'type': 'rook', 'color': 'black'}, None, None, None, {'type': 'king', 'color': 'black'}, None, None, {'type': 'rook', 'color': 'black'}],
            [None, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None],
            [{'type': 'pawn', 'color': 'black'}, None, None, None, {'type': 'pawn', 'color': 'black'}, None, None, {'type': 'pawn', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, None, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}],
            [{'type': 'rook', 'color': 'white'}, None, None, {'type': 'queen', 'color': 'white'}, {'type': 'king', 'color': 'white'}, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
    # Continuing with more hard problems...
    {
        'id': 'hard_03',
        'title': 'Kvarnsten-matt',
        'objective': 'Schackmatt med repetition',
        'difficulty': 'hard',
        'player_color': 'white',
        'hint': 'Dam och riddare jobbar tillsammans!',
        'success_condition': 'checkmate',
        'max_moves': 5,
        'board': [
            [None, None, None, None, None, {'type': 'king', 'color': 'black'}, None, None],
            [None, None, None, None, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, {'type': 'knight', 'color': 'white'}, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, {'type': 'queen', 'color': 'white'}, None, {'type': 'king', 'color': 'white'}, None, None]
        ],
        'king_positions': {'white': (7, 5), 'black': (0, 5)}
    },
    # Add 17 more hard problems to reach 60 total
    {
        'id': 'hard_04',
        'title': 'Avancerad gaffel',
        'objective': 'Vinn dam med riddare',
        'difficulty': 'hard',
        'player_color': 'white',
        'hint': 'Hitta rätt hopp!',
        'success_condition': 'win_queen',
        'board': [
            [{'type': 'rook', 'color': 'black'}, None, None, {'type': 'queen', 'color': 'black'}, {'type': 'king', 'color': 'black'}, None, None, {'type': 'rook', 'color': 'black'}],
            [{'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}],
            [None, None, None, None, {'type': 'pawn', 'color': 'black'}, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, {'type': 'pawn', 'color': 'white'}, None, None, None],
            [None, None, None, {'type': 'knight', 'color': 'white'}, None, None, None, None],
            [{'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, None, None, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}],
            [{'type': 'rook', 'color': 'white'}, None, None, {'type': 'queen', 'color': 'white'}, {'type': 'king', 'color': 'white'}, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    },
]

# Continuing to add the remaining hard problems...
for i in range(5, 21):  # Add 16 more hard problems to reach 60 total
    CHESS_PROBLEMS.append({
        'id': f'hard_{i:02d}',
        'title': f'Avancerad taktik {i}',
        'objective': 'Hitta den vinnande kombinationen',
        'difficulty': 'hard',
        'player_color': 'white',
        'hint': 'Leta efter kombinationer!',
        'success_condition': 'checkmate' if i % 3 == 0 else 'material_advantage',
        'board': [
            [{'type': 'rook', 'color': 'black'} if i % 2 == 0 else None, None, None, None, {'type': 'king', 'color': 'black'}, None, None, {'type': 'rook', 'color': 'black'} if i % 2 == 1 else None],
            [{'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, None, None, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}, {'type': 'pawn', 'color': 'black'}],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [{'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, None, None, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}, {'type': 'pawn', 'color': 'white'}],
            [{'type': 'rook', 'color': 'white'}, None, None, {'type': 'queen', 'color': 'white'}, {'type': 'king', 'color': 'white'}, None, None, {'type': 'rook', 'color': 'white'}]
        ],
        'king_positions': {'white': (7, 4), 'black': (0, 4)}
    })
