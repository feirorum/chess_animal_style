# -*- coding: utf-8 -*-
"""Swedish translations for Animal Chess"""

# Main menu
MENU_TITLE = "Djurschack"
MENU_START_NEW = "Starta nytt spel"
MENU_RESUME = "Fortsätt spel"
MENU_SAVE = "Spara spel"
MENU_LOAD = "Ladda spel"
MENU_HISTORY = "Visa draghistorik"
MENU_OPTIONS = "Inställningar"
MENU_EXIT = "Avsluta"
MENU_PROBLEMS = "Lös schackproblem"

# Game status
STATUS_CURRENT = "Nu spelar"
STATUS_CHECK = "SCHACK!"
STATUS_CHECKMATE = "SCHACKMATT!"
STATUS_GAME_OVER = "SPELET SLUT"
STATUS_DRAW = "Oavgjort!"
STATUS_WINS = "vinner!"
STATUS_PASS_TURN = "Passera tur"

# Colors
COLOR_WHITE = "vit"
COLOR_BLACK = "svart"

# Error messages
ERROR_NOT_YOUR_PIECE = "Det är inte din pjäs!"
ERROR_IN_CHECK = "Du står i schack! Du måste blockera eller flytta kungen."
ERROR_INVALID_MOVE = "Ogiltigt drag för denna pjäs"
ERROR_CASTLE_KINGSIDE = "Kan inte rockera kungssida: fältet är hotat eller vägen blockerad"
ERROR_CASTLE_QUEENSIDE = "Kan inte rockera damssida: fältet är hotat eller vägen blockerad"
ERROR_PASS_ONLY_SPECIAL = "Passera är bara tillåtet i specialläge efter schackmatt"
ERROR_PASS_ONLY_NO_MOVES = "Du kan bara passera när du inte har några giltiga drag"

# Game outcomes
OUTCOME_CHECKMATE_CONTINUE = "Schackmatt! {color} står i schack. Kan flytta en annan pjäs eller passera, sedan kan kungen tas."
OUTCOME_CHECKMATE_WINS = "Schackmatt! {color} vinner!"
OUTCOME_KING_CAPTURED = "Kungen tagen! {color} vinner!"
OUTCOME_STALEMATE = "Patt! Det är oavgjort - ingen vinner eller förlorar!"

# Promotion
PROMOTION_TITLE = "Välj befordringspjäs"

# Save/Load
SAVE_TITLE = "Spara spel"
SAVE_INSTRUCTION = "Ange spelnamn (eller lämna tomt för standard):"
SAVE_BUTTON = "Spara"
CANCEL_BUTTON = "Avbryt"
LOAD_TITLE = "Ladda spel"
NO_SAVED_GAMES = "Inga sparade spel hittades"

# Move history
HISTORY_TITLE = "Draghistorik"
HISTORY_MOVE_NUM = "Nr"
HISTORY_WHITE = "Vit"
HISTORY_BLACK = "Svart"
HISTORY_NO_MOVES = "Inga drag ännu"
HISTORY_BACK = "Tillbaka till menyn"

# Options
OPTIONS_TITLE = "Spelinställningar"
OPTIONS_CAPTURE_KING = "Ta kungen vid schackmatt"
OPTIONS_CAPTURE_KING_DESC1 = "När aktiverad fortsätter spelet efter schackmatt."
OPTIONS_CAPTURE_KING_DESC2 = "Spelaren kan flytta en annan pjäs eller passera."
OPTIONS_ANIMATIONS = "Tagningsanimationer"
OPTIONS_ANIMATIONS_DESC = "Visa glada animationer när pjäser tar andra pjäser."
OPTIONS_DURATION = "Animationslängd"
OPTIONS_DURATION_DESC = "Hur länge animationer varar: {duration:.1f} sekunder"
OPTIONS_ON = "PÅ"
OPTIONS_OFF = "AV"
OPTIONS_BACK = "Tillbaka till menyn"

# Game mode options
OPTIONS_GAME_MODE = "Spelläge"
OPTIONS_PLAYERS = "Antal spelare"
OPTIONS_1_PLAYER = "1 spelare"
OPTIONS_2_PLAYERS = "2 spelare"
OPTIONS_PLAYER_COLOR = "Din färg"
OPTIONS_AI_LEVEL = "Datorns svårighetsgrad"
OPTIONS_AI_LEVEL_DESC = "Nivå {level}: {desc}"
OPTIONS_AI_LEVELS = {
    1: "Mycket lätt (snabbast)",
    2: "Lätt",
    3: "Ganska lätt",
    4: "Enkel",
    5: "Medel",
    6: "Medel+",
    7: "Utmanande",
    8: "Svår",
    9: "Mycket svår",
    10: "Expert (långsammast)"
}

# Chess problems mode
PROBLEMS_TITLE = "Schackproblem"
PROBLEMS_SELECT = "Välj ett problem att lösa:"
PROBLEMS_OBJECTIVE = "Mål"
PROBLEMS_DIFFICULTY = "Svårighet"
PROBLEMS_YOUR_COLOR = "Du spelar"
PROBLEMS_SOLVE = "Lös"
PROBLEMS_BACK = "Tillbaka"
PROBLEMS_SOLVED = "Bra jobbat! Du löste problemet!"
PROBLEMS_FAILED = "Inte riktigt. Försök igen!"
PROBLEMS_HINT = "Tips"
PROBLEMS_EASY = "Lätt"
PROBLEMS_MEDIUM = "Medel"
PROBLEMS_HARD = "Svår"

# Button text
BUTTON_MENU = "Meny"

# Piece names (for descriptions)
PIECE_PAWN = "bonde"
PIECE_KNIGHT = "springare"
PIECE_BISHOP = "löpare"
PIECE_ROOK = "torn"
PIECE_QUEEN = "dam"
PIECE_KING = "kung"

# Animal names (shown in UI as fun alternative)
ANIMAL_PAWN = "ankunge"
ANIMAL_KNIGHT = "häst"
ANIMAL_BISHOP = "klumpfisk"
ANIMAL_ROOK = "bok"
ANIMAL_QUEEN = "katt"
ANIMAL_KING = "hund"
