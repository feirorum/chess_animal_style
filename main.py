import pygame
import sys
from chess_logic import ChessGame, GameOptions
from ui import ChessUI
from chess_ai import ChessAI
from chess_problems import CHESS_PROBLEMS
import swedish_text as txt
import copy

# Initialize Pygame
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    print("Warning: Audio device not available. Running without sound.")
    pass

# Constants
WINDOW_WIDTH = 2000
WINDOW_HEIGHT = 1600
FPS = 60

# Game states
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PROMOTION = "promotion"
STATE_SAVE_INPUT = "save_input"
STATE_LOAD_GAME = "load_game"
STATE_MOVE_HISTORY = "move_history"
STATE_OPTIONS = "options"
STATE_PROBLEMS_MENU = "problems_menu"
STATE_SOLVING_PROBLEM = "solving_problem"

def main():
    # Create window (resizable)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(txt.MENU_TITLE)
    clock = pygame.time.Clock()

    # Calculate initial board size based on window dimensions
    board_size = min(screen.get_width() - 400, screen.get_height() - 100)

    # Create UI instance
    ui = ChessUI(screen, board_size)

    # Game options
    options = GameOptions()

    # AI opponent
    ai = ChessAI(options.ai_skill_level)

    # Game state
    game = None
    current_state = STATE_MENU

    # Chess problems state
    current_problem = None
    problem_game = None

    # Game loop variables
    dragging = False
    selected_piece = None
    drag_pos = None

    # Promotion state
    promotion_position = None
    promotion_color = None

    # Save input state
    save_name_input = ""

    # Main game loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle window resize
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                board_size = min(screen.get_width() - 400, screen.get_height() - 100)
                ui = ChessUI(screen, board_size)

            # Menu state events
            elif current_state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    buttons = ui.draw_menu(has_ongoing_game=(game is not None))
                    for button in buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            label = button['label']

                            if label == txt.MENU_START_NEW:
                                game = ChessGame(options)
                                current_state = STATE_PLAYING
                            elif label == txt.MENU_RESUME:
                                current_state = STATE_PLAYING
                            elif label == txt.MENU_SAVE:
                                save_name_input = ""
                                current_state = STATE_SAVE_INPUT
                            elif label == txt.MENU_LOAD:
                                current_state = STATE_LOAD_GAME
                            elif label == txt.MENU_HISTORY:
                                current_state = STATE_MOVE_HISTORY
                            elif label == txt.MENU_PROBLEMS:
                                current_state = STATE_PROBLEMS_MENU
                            elif label == txt.MENU_OPTIONS:
                                current_state = STATE_OPTIONS
                            elif label == txt.MENU_EXIT:
                                running = False

            # Playing state events
            elif current_state == STATE_PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        # Check menu button
                        menu_button = ui.draw_menu_button()
                        if menu_button.collidepoint(mouse_pos):
                            current_state = STATE_MENU
                            dragging = False
                            selected_piece = None
                            drag_pos = None
                            continue

                        # Check pass button if in checkmate capture mode
                        if game and game.in_checkmate_capture_mode:
                            pass_button = ui.draw_pass_button()
                            if pass_button.collidepoint(mouse_pos):
                                result = game.pass_turn()
                                if not result.get('valid'):
                                    ui.show_violation_popup(result.get('reason', 'Cannot pass turn'))
                                continue

                        # Handle piece selection (only if game is ongoing)
                        if game.game_status == 'ongoing':
                            square = ui.get_square_from_pos(mouse_pos)
                            if square:
                                row, col = square
                                piece = game.board[row][col]

                                # Check if clicked piece belongs to current player
                                if piece and piece['color'] == game.current_player:
                                    dragging = True
                                    selected_piece = (row, col)
                                    drag_pos = mouse_pos

                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        drag_pos = pygame.mouse.get_pos()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and dragging and game.game_status == 'ongoing':
                        target_square = ui.get_square_from_pos(mouse_pos)

                        if target_square and selected_piece:
                            from_row, from_col = selected_piece
                            to_row, to_col = target_square

                            # Check if this is a capture (before making the move)
                            is_capture = game.board[to_row][to_col] is not None
                            # Also check for en passant capture
                            piece = game.board[from_row][from_col]
                            if piece and piece['type'] == 'pawn' and game.en_passant_target == (to_row, to_col):
                                is_capture = True

                            # Attempt to make the move
                            result = game.make_move(from_row, from_col, to_row, to_col)

                            if not result['valid']:
                                # Show popup with violation reason
                                ui.show_violation_popup(result['reason'])
                            elif result.get('promotion'):
                                # If this was a valid capture, trigger celebration
                                if is_capture:
                                    ui.trigger_celebration(to_row, to_col, options)
                                # Handle pawn promotion
                                promotion_position = result['position']
                                promotion_color = result['color']
                                current_state = STATE_PROMOTION
                            elif result.get('checkmate'):
                                # If this was a valid capture, trigger celebration
                                if is_capture:
                                    ui.trigger_celebration(to_row, to_col, options)
                                if result.get('continue_play'):
                                    # Capture king mode: game continues (flag already set in game object)
                                    color = result['in_check']
                                    color_name = txt.COLOR_WHITE if color == 'white' else txt.COLOR_BLACK
                                    ui.show_violation_popup(txt.OUTCOME_CHECKMATE_CONTINUE.format(color=color_name))
                                else:
                                    # Normal mode: game ends
                                    winner = result['winner']
                                    color_name = txt.COLOR_WHITE if winner == 'white' else txt.COLOR_BLACK
                                    ui.show_violation_popup(txt.OUTCOME_CHECKMATE_WINS.format(color=color_name.capitalize()))
                            elif result.get('king_captured'):
                                # King was captured - game over (always a capture, trigger celebration)
                                ui.trigger_celebration(to_row, to_col, options)
                                winner = result['winner']
                                color_name = txt.COLOR_WHITE if winner == 'white' else txt.COLOR_BLACK
                                ui.show_violation_popup(txt.OUTCOME_KING_CAPTURED.format(color=color_name.capitalize()))
                            elif result.get('stalemate'):
                                # If this was a valid capture, trigger celebration
                                if is_capture:
                                    ui.trigger_celebration(to_row, to_col, options)
                                # Show stalemate message
                                ui.show_violation_popup(txt.OUTCOME_STALEMATE)
                            else:
                                # Regular move - if this was a capture, trigger celebration
                                if is_capture:
                                    ui.trigger_celebration(to_row, to_col, options)

                                # In 1-player mode, trigger AI move if it's AI's turn
                                if options.game_mode == '1_player' and game.game_status == 'ongoing':
                                    ai_color = 'black' if options.player_color == 'white' else 'white'
                                    if game.current_player == ai_color:
                                        # AI makes a move (delay based on skill level)
                                        # Level 1-2: 100ms, Level 3-5: 250ms, Level 6-8: 400ms, Level 9-10: 600ms
                                        if options.ai_skill_level <= 2:
                                            delay = 100
                                        elif options.ai_skill_level <= 5:
                                            delay = 250
                                        elif options.ai_skill_level <= 8:
                                            delay = 400
                                        else:
                                            delay = 600
                                        pygame.time.wait(delay)
                                        ai_move = ai.get_best_move(game)
                                        if ai_move:
                                            ai_from_row, ai_from_col, ai_to_row, ai_to_col = ai_move
                                            ai_result = game.make_move(ai_from_row, ai_from_col, ai_to_row, ai_to_col)
                                            if ai_result.get('promotion'):
                                                # AI always promotes to queen
                                                game.promote_pawn(ai_to_row, ai_to_col, 'queen')

                        dragging = False
                        selected_piece = None
                        drag_pos = None

            # Promotion state events
            elif current_state == STATE_PROMOTION:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    piece_buttons = ui.draw_promotion_popup(promotion_color)
                    for button in piece_buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            # Promote pawn
                            row, col = promotion_position
                            result = game.promote_pawn(row, col, button['type'])

                            if result.get('checkmate'):
                                winner = result['winner']
                                ui.show_violation_popup(f"Checkmate! {winner.capitalize()} wins!")
                            elif result.get('stalemate'):
                                ui.show_violation_popup("Stalemate! It's a draw - nobody wins or loses!")
                            # continue_play flag already set in game object

                            current_state = STATE_PLAYING
                            promotion_position = None
                            promotion_color = None
                            break

            # Save input state events
            elif current_state == STATE_SAVE_INPUT:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Save the game
                        name = save_name_input if save_name_input else "game"
                        filepath = game.save_game(name)
                        print(f"Game saved to {filepath}")
                        current_state = STATE_MENU
                    elif event.key == pygame.K_ESCAPE:
                        current_state = STATE_MENU
                    elif event.key == pygame.K_BACKSPACE:
                        save_name_input = save_name_input[:-1]
                    else:
                        # Add character to input (limit to alphanumeric and some special chars)
                        if event.unicode.isalnum() or event.unicode in ['_', '-', ' ']:
                            if len(save_name_input) < 30:
                                save_name_input += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    popup_elements = ui.draw_save_input_popup(save_name_input)
                    if popup_elements['save_button'].collidepoint(mouse_pos):
                        name = save_name_input if save_name_input else "game"
                        filepath = game.save_game(name)
                        print(f"Game saved to {filepath}")
                        current_state = STATE_MENU
                    elif popup_elements['cancel_button'].collidepoint(mouse_pos):
                        current_state = STATE_MENU

            # Load game state events
            elif current_state == STATE_LOAD_GAME:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    saved_games = ChessGame.get_saved_games()
                    popup_elements = ui.draw_load_game_popup(saved_games)

                    # Check if cancel button clicked
                    if popup_elements['cancel_button'].collidepoint(mouse_pos):
                        current_state = STATE_MENU
                    else:
                        # Check if a game was clicked
                        for button in popup_elements['game_buttons']:
                            if button['rect'].collidepoint(mouse_pos):
                                # Load the game
                                game = ChessGame(options)
                                game.load_game(button['game']['filepath'])
                                print(f"Game loaded from {button['game']['filepath']}")
                                current_state = STATE_PLAYING
                                break

            # Move history state events
            elif current_state == STATE_MOVE_HISTORY:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    back_button = ui.draw_move_history(game.move_history if game else [])
                    if back_button and back_button.collidepoint(mouse_pos):
                        current_state = STATE_MENU

            # Options state events
            elif current_state == STATE_OPTIONS:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    option_elements = ui.draw_options(options)
                    if option_elements['back_button'].collidepoint(mouse_pos):
                        current_state = STATE_MENU
                    elif option_elements['toggle_button'].collidepoint(mouse_pos):
                        options.toggle_capture_king()
                    elif option_elements['mode_1p_button'].collidepoint(mouse_pos):
                        options.set_game_mode('1_player')
                    elif option_elements['mode_2p_button'].collidepoint(mouse_pos):
                        options.set_game_mode('2_player')
                    elif option_elements.get('color_white_button') and option_elements['color_white_button'].collidepoint(mouse_pos):
                        options.set_player_color('white')
                    elif option_elements.get('color_black_button') and option_elements['color_black_button'].collidepoint(mouse_pos):
                        options.set_player_color('black')
                    elif option_elements.get('ai_minus_button') and option_elements['ai_minus_button'].collidepoint(mouse_pos):
                        new_level = max(1, options.ai_skill_level - 1)
                        options.set_ai_skill_level(new_level)
                        ai.skill_level = new_level
                    elif option_elements.get('ai_plus_button') and option_elements['ai_plus_button'].collidepoint(mouse_pos):
                        new_level = min(10, options.ai_skill_level + 1)
                        options.set_ai_skill_level(new_level)
                        ai.skill_level = new_level

            # Problems menu state events
            elif current_state == STATE_PROBLEMS_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    menu_elements = ui.draw_problems_menu(CHESS_PROBLEMS)
                    if menu_elements['back_button'].collidepoint(mouse_pos):
                        current_state = STATE_MENU
                    else:
                        for button in menu_elements['problem_buttons']:
                            if button['rect'].collidepoint(mouse_pos):
                                # Start solving this problem
                                current_problem = button['problem']
                                problem_game = ChessGame(options)
                                # Set up the board from the problem
                                problem_game.board = copy.deepcopy(current_problem['board'])
                                problem_game.current_player = current_problem['player_color']
                                if current_problem['king_positions']['white']:
                                    problem_game.king_positions['white'] = current_problem['king_positions']['white']
                                if current_problem['king_positions']['black']:
                                    problem_game.king_positions['black'] = current_problem['king_positions']['black']
                                problem_game.move_history = []
                                current_state = STATE_SOLVING_PROBLEM
                                break

            # Solving problem state events
            elif current_state == STATE_SOLVING_PROBLEM:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        # Check menu button
                        menu_button = ui.draw_menu_button()
                        if menu_button.collidepoint(mouse_pos):
                            current_state = STATE_PROBLEMS_MENU
                            problem_game = None
                            current_problem = None
                            dragging = False
                            selected_piece = None
                            drag_pos = None
                            continue

                        # Handle piece selection (only if game is ongoing)
                        if problem_game.game_status == 'ongoing':
                            square = ui.get_square_from_pos(mouse_pos)
                            if square:
                                row, col = square
                                piece = problem_game.board[row][col]

                                # Check if clicked piece belongs to current player
                                if piece and piece['color'] == problem_game.current_player:
                                    dragging = True
                                    selected_piece = (row, col)
                                    drag_pos = mouse_pos

                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        drag_pos = pygame.mouse.get_pos()

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and dragging and problem_game.game_status == 'ongoing':
                        target_square = ui.get_square_from_pos(mouse_pos)

                        if target_square and selected_piece:
                            from_row, from_col = selected_piece
                            to_row, to_col = target_square

                            # Attempt to make the move
                            result = problem_game.make_move(from_row, from_col, to_row, to_col)

                            if not result['valid']:
                                ui.show_violation_popup(result['reason'])
                            elif result.get('promotion'):
                                promotion_position = result['position']
                                promotion_color = result['color']
                                current_state = STATE_PROMOTION
                            elif result.get('checkmate') or result.get('stalemate'):
                                # Problem solved!
                                ui.show_violation_popup(txt.PROBLEMS_SOLVED)

                            # AI makes opponent move in problem mode
                            if problem_game.game_status == 'ongoing' and problem_game.current_player != current_problem['player_color']:
                                # Use level 5 (medium) for problem solving
                                pygame.time.wait(300)
                                ai_move = ai.get_best_move(problem_game)
                                if ai_move:
                                    ai_from_row, ai_from_col, ai_to_row, ai_to_col = ai_move
                                    problem_game.make_move(ai_from_row, ai_from_col, ai_to_row, ai_to_col)

                        dragging = False
                        selected_piece = None
                        drag_pos = None

        # Draw based on current state
        if current_state == STATE_MENU:
            ui.draw_menu(has_ongoing_game=(game is not None))

        elif current_state == STATE_PLAYING:
            # Get valid moves for selected piece
            valid_moves = []
            if selected_piece:
                row, col = selected_piece
                valid_moves = game.get_valid_moves(row, col)

            # Draw game
            ui.draw(game, selected_piece, drag_pos, valid_moves)

            # Draw pass button if in checkmate capture mode and player has no moves
            if game and game.in_checkmate_capture_mode and not game.has_any_valid_moves(game.current_player):
                ui.draw_pass_button()

        elif current_state == STATE_PROMOTION:
            # Draw game in background
            ui.draw(game, None, None, [])
            # Draw promotion popup on top
            ui.draw_promotion_popup(promotion_color)

        elif current_state == STATE_SAVE_INPUT:
            # Draw game in background
            ui.draw(game, None, None, [])
            # Draw save input popup on top
            ui.draw_save_input_popup(save_name_input)

        elif current_state == STATE_LOAD_GAME:
            # Draw menu in background
            ui.draw_menu(has_ongoing_game=(game is not None))
            # Draw load game popup on top
            saved_games = ChessGame.get_saved_games()
            ui.draw_load_game_popup(saved_games)

        elif current_state == STATE_MOVE_HISTORY:
            # Draw move history screen
            ui.draw_move_history(game.move_history if game else [])

        elif current_state == STATE_OPTIONS:
            # Draw options screen
            ui.draw_options(options)

        elif current_state == STATE_PROBLEMS_MENU:
            # Draw problems menu
            ui.draw_problems_menu(CHESS_PROBLEMS)

        elif current_state == STATE_SOLVING_PROBLEM:
            # Get valid moves for selected piece
            valid_moves = []
            if selected_piece and problem_game:
                row, col = selected_piece
                valid_moves = problem_game.get_valid_moves(row, col)

            # Draw problem game
            if problem_game:
                ui.draw(problem_game, selected_piece, drag_pos, valid_moves)
                # Draw problem objective
                if current_problem:
                    ui.draw_problem_objective(current_problem)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
