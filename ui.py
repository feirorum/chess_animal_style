import pygame
import os
import swedish_text as txt

class ChessUI:
    def __init__(self, screen, board_size):
        self.screen = screen
        self.board_size = board_size
        self.square_size = board_size // 8

        # Calculate responsive offsets based on window size
        self.board_offset_x = max(50, (screen.get_width() - board_size - 300) // 2)
        self.board_offset_y = max(50, (screen.get_height() - board_size) // 2)

        # Colors
        self.light_square = (240, 217, 181)
        self.dark_square = (181, 136, 99)
        self.highlight_color = (255, 255, 0, 100)
        self.valid_move_color = (0, 255, 0, 150)
        self.bg_color = (200, 230, 255)  # Light blue background

        # Responsive font sizes based on board size
        base_scale = board_size / 700
        self.font_large = pygame.font.Font(None, int(48 * base_scale))
        self.font_medium = pygame.font.Font(None, int(36 * base_scale))
        self.font_small = pygame.font.Font(None, int(24 * base_scale))

        # Load piece images
        self.piece_images = self.load_piece_images()

        # Popup state
        self.popup_message = None
        self.popup_timer = 0

        # Celebration tracking for pieces that just captured
        # Key: (row, col), Value: frames remaining (4-5 seconds at 60 FPS = 240-300 frames)
        self.celebrating_pieces = {}

        # Load background
        self.background = self.create_background()

    def create_background(self):
        """Create a fun animal-themed background"""
        width = self.screen.get_width()
        height = self.screen.get_height()
        bg = pygame.Surface((width, height))
        bg.fill(self.bg_color)

        # Draw some fun elements (simple version - can be enhanced with images)
        # Draw clouds (responsive to window width)
        num_clouds = max(5, width // 300)
        for i in range(num_clouds):
            x = (width // (num_clouds + 1)) * (i + 1) - 40
            y = 50 + (i % 2) * 30
            cloud_scale = min(1.0, width / 1000)
            pygame.draw.ellipse(bg, (255, 255, 255), (x, y, int(80 * cloud_scale), int(40 * cloud_scale)))
            pygame.draw.ellipse(bg, (255, 255, 255), (x + int(20 * cloud_scale), y - int(10 * cloud_scale), int(60 * cloud_scale), int(40 * cloud_scale)))
            pygame.draw.ellipse(bg, (255, 255, 255), (x + int(40 * cloud_scale), y, int(70 * cloud_scale), int(40 * cloud_scale)))

        # Draw grass at bottom (responsive height)
        grass_height = max(100, int(height * 0.1))
        pygame.draw.rect(bg, (150, 220, 150), (0, height - grass_height, width, grass_height))

        # Draw some simple flowers (responsive to window width)
        num_flowers = max(10, width // 150)
        for i in range(num_flowers):
            x = (width // (num_flowers + 1)) * (i + 1)
            y = height - int(grass_height * 0.8) + (i % 3) * 10
            flower_scale = min(1.0, width / 1000)
            # Stem
            pygame.draw.line(bg, (100, 180, 100), (x, y + int(20 * flower_scale)), (x, y + int(50 * flower_scale)), max(2, int(3 * flower_scale)))
            # Flower
            for angle in range(0, 360, 60):
                offset_x = int(8 * flower_scale) * pygame.math.Vector2(1, 0).rotate(angle).x
                offset_y = int(8 * flower_scale) * pygame.math.Vector2(1, 0).rotate(angle).y
                pygame.draw.circle(bg, (255, 200, 220), (int(x + offset_x), int(y + offset_y)), max(4, int(6 * flower_scale)))
            # Center
            pygame.draw.circle(bg, (255, 255, 100), (x, y), max(4, int(6 * flower_scale)))

        return bg

    def trigger_celebration(self, row, col, options=None):
        """Start a celebration animation for a piece at the given position"""
        # Check if animations are enabled
        if options and not options.animations_enabled:
            return

        # Use duration from options if available
        duration_seconds = options.animation_duration if options else 4.5
        frames = int(duration_seconds * 60)  # Convert seconds to frames at 60 FPS
        self.celebrating_pieces[(row, col)] = frames

    def update_celebrations(self):
        """Update celebration timers and remove expired ones"""
        expired = []
        for pos, frames in self.celebrating_pieces.items():
            self.celebrating_pieces[pos] = frames - 1
            if self.celebrating_pieces[pos] <= 0:
                expired.append(pos)

        for pos in expired:
            del self.celebrating_pieces[pos]

    def load_piece_images(self):
        """Load or create piece images (animal representations)"""
        images = {}
        colors = ['white', 'black']
        pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']

        for color in colors:
            for piece in pieces:
                images[f"{color}_{piece}"] = self.create_piece_image(piece, color)

        return images

    def create_piece_image(self, piece_type, color):
        """Create a simple representation of animal pieces"""
        surface = pygame.Surface((self.square_size - 10, self.square_size - 10), pygame.SRCALPHA)
        piece_color = (255, 255, 255) if color == 'white' else (50, 50, 50)
        accent_color = (220, 220, 220) if color == 'white' else (80, 80, 80)
        outline_color = (0, 0, 0)

        center_x = (self.square_size - 10) // 2
        center_y = (self.square_size - 10) // 2

        # Calculate scale factor based on square size (base size is ~70 pixels)
        scale = self.square_size / 70.0

        def s(value):
            """Scale a coordinate value"""
            return int(value * scale)

        size = min(self.square_size - 20, 60)

        if piece_type == 'pawn':  # Duckling
            # Rounder, cuter body
            pygame.draw.ellipse(surface, piece_color, (center_x - s(12), center_y, s(24), s(28)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(12), center_y, s(24), s(28)), max(1, s(2)))
            # Bigger, rounder head (more proportionate to baby duck)
            pygame.draw.circle(surface, piece_color, (center_x, center_y - s(8)), s(14))
            pygame.draw.circle(surface, outline_color, (center_x, center_y - s(8)), s(14), max(1, s(2)))
            # Bigger, rounder beak (more like duckling)
            beak_color = (255, 180, 0)
            pygame.draw.ellipse(surface, beak_color, (center_x + s(8), center_y - s(12), s(10), s(8)))
            pygame.draw.ellipse(surface, outline_color, (center_x + s(8), center_y - s(12), s(10), s(8)), max(1, s(1)))
            # Bigger, cuter eyes
            pygame.draw.circle(surface, (255, 255, 255), (center_x - s(4), center_y - s(11)), s(4))
            pygame.draw.circle(surface, (255, 255, 255), (center_x + s(4), center_y - s(11)), s(4))
            pygame.draw.circle(surface, outline_color, (center_x - s(4), center_y - s(11)), max(1, s(2)))
            pygame.draw.circle(surface, outline_color, (center_x + s(4), center_y - s(11)), max(1, s(2)))
            # Tiny wing fluff
            pygame.draw.ellipse(surface, accent_color, (center_x - s(14), center_y + s(8), s(8), s(12)))
            pygame.draw.ellipse(surface, accent_color, (center_x + s(6), center_y + s(8), s(8), s(12)))
            # Little webbed feet
            foot_color = (255, 180, 0)
            # Left foot
            pygame.draw.ellipse(surface, foot_color, (center_x - s(10), center_y + s(24), s(8), s(4)))
            # Right foot
            pygame.draw.ellipse(surface, foot_color, (center_x + s(2), center_y + s(24), s(8), s(4)))

        elif piece_type == 'knight':  # Horse
            # Head
            pygame.draw.ellipse(surface, piece_color, (center_x - s(15), center_y - s(20), s(30), s(40)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(15), center_y - s(20), s(30), s(40)), max(1, s(2)))
            # Snout
            pygame.draw.ellipse(surface, accent_color, (center_x - s(10), center_y + s(5), s(20), s(15)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(10), center_y + s(5), s(20), s(15)), max(1, s(2)))
            # Ears
            pygame.draw.polygon(surface, piece_color, [(center_x - s(10), center_y - s(20)), (center_x - s(15), center_y - s(30)), (center_x - s(5), center_y - s(22))])
            pygame.draw.polygon(surface, piece_color, [(center_x + s(10), center_y - s(20)), (center_x + s(15), center_y - s(30)), (center_x + s(5), center_y - s(22))])
            # Eyes
            pygame.draw.circle(surface, outline_color, (center_x - s(6), center_y - s(10)), max(1, s(3)))
            pygame.draw.circle(surface, outline_color, (center_x + s(6), center_y - s(10)), max(1, s(3)))
            # Mane
            for i in range(3):
                pygame.draw.line(surface, accent_color, (center_x - s(5) + i * s(5), center_y - s(25)), (center_x - s(5) + i * s(5), center_y - s(18)), max(1, s(2)))

        elif piece_type == 'bishop':  # Blobfish
            # Blob body
            pygame.draw.ellipse(surface, piece_color, (center_x - s(20), center_y - s(15), s(40), s(35)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(20), center_y - s(15), s(40), s(35)), max(1, s(2)))
            # Droopy face
            pygame.draw.ellipse(surface, accent_color, (center_x - s(15), center_y - s(10), s(30), s(25)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(15), center_y - s(10), s(30), s(25)), max(1, s(2)))
            # Sad eyes
            pygame.draw.circle(surface, outline_color, (center_x - s(8), center_y - s(5)), max(1, s(4)))
            pygame.draw.circle(surface, outline_color, (center_x + s(8), center_y - s(5)), max(1, s(4)))
            # Droopy mouth
            pygame.draw.arc(surface, outline_color, (center_x - s(8), center_y, s(16), s(10)), 0, 3.14, max(1, s(2)))
            # Fins
            pygame.draw.polygon(surface, piece_color, [(center_x - s(20), center_y), (center_x - s(30), center_y - s(5)), (center_x - s(25), center_y + s(5))])
            pygame.draw.polygon(surface, piece_color, [(center_x + s(20), center_y), (center_x + s(30), center_y - s(5)), (center_x + s(25), center_y + s(5))])

        elif piece_type == 'rook':  # Book
            # Book cover
            pygame.draw.rect(surface, piece_color, (center_x - s(18), center_y - s(22), s(36), s(44)))
            pygame.draw.rect(surface, outline_color, (center_x - s(18), center_y - s(22), s(36), s(44)), max(1, s(2)))
            # Book spine
            pygame.draw.rect(surface, accent_color, (center_x - s(18), center_y - s(22), s(6), s(44)))
            pygame.draw.rect(surface, outline_color, (center_x - s(18), center_y - s(22), s(6), s(44)), max(1, s(2)))
            # Pages
            for i in range(4):
                y_offset = center_y - s(18) + i * s(10)
                pygame.draw.line(surface, accent_color, (center_x - s(10), y_offset), (center_x + s(15), y_offset), max(1, s(1)))
            # Bookmark
            pygame.draw.rect(surface, (255, 200, 200), (center_x + s(5), center_y - s(22), s(4), s(15)))

        elif piece_type == 'queen':  # Cat
            # Body
            pygame.draw.ellipse(surface, piece_color, (center_x - s(15), center_y - s(5), s(30), s(30)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(15), center_y - s(5), s(30), s(30)), max(1, s(2)))
            # Head
            pygame.draw.circle(surface, piece_color, (center_x, center_y - s(15)), s(14))
            pygame.draw.circle(surface, outline_color, (center_x, center_y - s(15)), s(14), max(1, s(2)))
            # Ears
            pygame.draw.polygon(surface, piece_color, [(center_x - s(12), center_y - s(20)), (center_x - s(18), center_y - s(30)), (center_x - s(8), center_y - s(24))])
            pygame.draw.polygon(surface, outline_color, [(center_x - s(12), center_y - s(20)), (center_x - s(18), center_y - s(30)), (center_x - s(8), center_y - s(24))], max(1, s(2)))
            pygame.draw.polygon(surface, piece_color, [(center_x + s(12), center_y - s(20)), (center_x + s(18), center_y - s(30)), (center_x + s(8), center_y - s(24))])
            pygame.draw.polygon(surface, outline_color, [(center_x + s(12), center_y - s(20)), (center_x + s(18), center_y - s(30)), (center_x + s(8), center_y - s(24))], max(1, s(2)))
            # Eyes
            pygame.draw.ellipse(surface, (100, 200, 100), (center_x - s(8), center_y - s(18), s(6), s(8)))
            pygame.draw.ellipse(surface, (100, 200, 100), (center_x + s(2), center_y - s(18), s(6), s(8)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(5), center_y - s(17), max(1, s(2)), s(4)))
            pygame.draw.ellipse(surface, outline_color, (center_x + s(5), center_y - s(17), max(1, s(2)), s(4)))
            # Nose
            pygame.draw.polygon(surface, (255, 150, 150), [(center_x, center_y - s(12)), (center_x - s(2), center_y - s(14)), (center_x + s(2), center_y - s(14))])
            # Whiskers
            pygame.draw.line(surface, outline_color, (center_x - s(14), center_y - s(12)), (center_x - s(22), center_y - s(13)), max(1, s(1)))
            pygame.draw.line(surface, outline_color, (center_x - s(14), center_y - s(10)), (center_x - s(22), center_y - s(10)), max(1, s(1)))
            pygame.draw.line(surface, outline_color, (center_x + s(14), center_y - s(12)), (center_x + s(22), center_y - s(13)), max(1, s(1)))
            pygame.draw.line(surface, outline_color, (center_x + s(14), center_y - s(10)), (center_x + s(22), center_y - s(10)), max(1, s(1)))
            # Tail
            pygame.draw.arc(surface, outline_color, (center_x + s(10), center_y, s(20), s(25)), -1.57, 1.57, max(1, s(2)))
            # Crown
            crown_color = (255, 215, 0)
            pygame.draw.polygon(surface, crown_color, [(center_x - s(10), center_y - s(28)), (center_x, center_y - s(35)), (center_x + s(10), center_y - s(28)), (center_x + s(8), center_y - s(25)), (center_x, center_y - s(30)), (center_x - s(8), center_y - s(25))])

        elif piece_type == 'king':  # Dog
            # Body
            pygame.draw.ellipse(surface, piece_color, (center_x - s(15), center_y - s(5), s(30), s(30)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(15), center_y - s(5), s(30), s(30)), max(1, s(2)))
            # Head
            pygame.draw.ellipse(surface, piece_color, (center_x - s(12), center_y - s(20), s(24), s(20)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(12), center_y - s(20), s(24), s(20)), max(1, s(2)))
            # Snout
            pygame.draw.ellipse(surface, accent_color, (center_x - s(8), center_y - s(8), s(16), s(12)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(8), center_y - s(8), s(16), s(12)), max(1, s(2)))
            # Floppy ears
            pygame.draw.ellipse(surface, piece_color, (center_x - s(20), center_y - s(15), s(10), s(15)))
            pygame.draw.ellipse(surface, outline_color, (center_x - s(20), center_y - s(15), s(10), s(15)), max(1, s(2)))
            pygame.draw.ellipse(surface, piece_color, (center_x + s(10), center_y - s(15), s(10), s(15)))
            pygame.draw.ellipse(surface, outline_color, (center_x + s(10), center_y - s(15), s(10), s(15)), max(1, s(2)))
            # Eyes
            pygame.draw.circle(surface, outline_color, (center_x - s(5), center_y - s(15)), max(1, s(3)))
            pygame.draw.circle(surface, outline_color, (center_x + s(5), center_y - s(15)), max(1, s(3)))
            # Nose
            pygame.draw.circle(surface, outline_color, (center_x, center_y - s(5)), max(1, s(3)))
            # Tongue
            pygame.draw.ellipse(surface, (255, 150, 150), (center_x + s(4), center_y - s(2), s(6), s(8)))
            # Tail
            pygame.draw.arc(surface, outline_color, (center_x + s(12), center_y + s(5), s(15), s(15)), -1.57, 1.57, max(1, s(3)))
            # Crown
            crown_color = (255, 215, 0)
            pygame.draw.polygon(surface, crown_color, [(center_x - s(10), center_y - s(25)), (center_x - s(8), center_y - s(32)), (center_x - s(3), center_y - s(26)), (center_x, center_y - s(33)), (center_x + s(3), center_y - s(26)), (center_x + s(8), center_y - s(32)), (center_x + s(10), center_y - s(25)), (center_x + s(8), center_y - s(23)), (center_x, center_y - s(23)), (center_x - s(8), center_y - s(23))])
            pygame.draw.polygon(surface, outline_color, [(center_x - s(10), center_y - s(25)), (center_x - s(8), center_y - s(32)), (center_x - s(3), center_y - s(26)), (center_x, center_y - s(33)), (center_x + s(3), center_y - s(26)), (center_x + s(8), center_y - s(32)), (center_x + s(10), center_y - s(25)), (center_x + s(8), center_y - s(23)), (center_x, center_y - s(23)), (center_x - s(8), center_y - s(23))], max(1, s(2)))

        return surface

    def draw(self, game, selected_piece, drag_pos, valid_moves):
        """Draw the entire game state"""
        # Update celebration timers
        self.update_celebrations()

        # Draw background
        self.screen.blit(self.background, (0, 0))

        # Draw board
        self.draw_board()

        # Draw valid move indicators
        if valid_moves:
            self.draw_valid_moves(valid_moves)

        # Draw pieces
        self.draw_pieces(game.board, selected_piece, drag_pos)

        # Draw game status (handles all cases: ongoing, finished, draw, winner)
        self.draw_game_status(game)

        # Draw menu button
        menu_button = self.draw_menu_button()

        # Draw popup if active
        if self.popup_message and self.popup_timer > 0:
            self.draw_popup()
            self.popup_timer -= 1

        return menu_button

    def draw_menu_button(self):
        """Draw menu button on game screen (responsive sizing)"""
        button_width = min(120, int(self.board_size * 0.17))
        button_height = max(30, int(self.board_size * 0.057))
        button_x = self.board_offset_x + self.board_size + int(self.board_size * 0.043)
        button_y = self.board_offset_y + int(self.board_size * 0.357)
        menu_button = pygame.Rect(button_x, button_y, button_width, button_height)

        pygame.draw.rect(self.screen, (150, 150, 200), menu_button, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), menu_button, 2, border_radius=5)

        text = self.font_small.render(txt.BUTTON_MENU, True, (0, 0, 0))
        text_x = button_x + (button_width - text.get_width()) // 2
        text_y = button_y + (button_height - text.get_height()) // 2
        self.screen.blit(text, (text_x, text_y))

        return menu_button

    def draw_board(self):
        """Draw the chess board"""
        for row in range(8):
            for col in range(8):
                color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                x = self.board_offset_x + col * self.square_size
                y = self.board_offset_y + row * self.square_size
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))

        # Draw board border
        pygame.draw.rect(self.screen, (100, 70, 50), (self.board_offset_x - 3, self.board_offset_y - 3, self.board_size + 6, self.board_size + 6), 6)

        # Draw coordinates
        for i in range(8):
            # Letters (a-h)
            letter = chr(ord('a') + i)
            text = self.font_small.render(letter, True, (0, 0, 0))
            x = self.board_offset_x + i * self.square_size + self.square_size // 2 - text.get_width() // 2
            y = self.board_offset_y + self.board_size + 10
            self.screen.blit(text, (x, y))

            # Numbers (1-8)
            number = str(8 - i)
            text = self.font_small.render(number, True, (0, 0, 0))
            x = self.board_offset_x - 30
            y = self.board_offset_y + i * self.square_size + self.square_size // 2 - text.get_height() // 2
            self.screen.blit(text, (x, y))

    def draw_celebration_effects(self, x, y, frames_remaining, total_frames):
        """Draw celebration effects around a piece (hearts, bouncing, sparkles)"""
        import math

        # Calculate animation progress (0.0 to 1.0)
        progress = frames_remaining / total_frames

        # Bouncing effect - piece bounces higher at the start
        bounce_height = int(math.sin(frames_remaining * 0.15) * 8 * progress)

        # Draw hearts around the piece
        heart_color = (255, 100, 150)
        heart_positions = [
            (-15, -20), (15, -20),  # Top hearts
            (-20, 0), (20, 0),      # Side hearts
        ]

        for i, (dx, dy) in enumerate(heart_positions):
            # Hearts fade in and out
            if progress > 0.1:  # Only show hearts after initial bounce
                heart_x = x + self.square_size // 2 + dx
                heart_y = y + self.square_size // 2 + dy + bounce_height
                # Floating effect
                float_offset = int(math.sin(frames_remaining * 0.1 + i) * 5)
                heart_y += float_offset

                # Draw simple heart shape
                heart_size = 6
                pygame.draw.circle(self.screen, heart_color, (heart_x - heart_size//2, heart_y), heart_size//2)
                pygame.draw.circle(self.screen, heart_color, (heart_x + heart_size//2, heart_y), heart_size//2)
                pygame.draw.polygon(self.screen, heart_color, [
                    (heart_x - heart_size, heart_y),
                    (heart_x, heart_y + heart_size),
                    (heart_x + heart_size, heart_y)
                ])

        # Draw sparkles
        sparkle_color = (255, 255, 100)
        for i in range(6):
            angle = (frames_remaining * 0.05 + i * 60) % 360
            distance = 25 + math.sin(frames_remaining * 0.1) * 5
            sparkle_x = x + self.square_size // 2 + int(math.cos(math.radians(angle)) * distance)
            sparkle_y = y + self.square_size // 2 + int(math.sin(math.radians(angle)) * distance) + bounce_height

            # Draw star sparkle
            star_size = 3
            pygame.draw.circle(self.screen, sparkle_color, (sparkle_x, sparkle_y), star_size)
            pygame.draw.line(self.screen, sparkle_color, (sparkle_x - star_size - 2, sparkle_y), (sparkle_x + star_size + 2, sparkle_y), 1)
            pygame.draw.line(self.screen, sparkle_color, (sparkle_x, sparkle_y - star_size - 2), (sparkle_x, sparkle_y + star_size + 2), 1)

        return bounce_height

    def draw_pieces(self, board, selected_piece, drag_pos):
        """Draw all pieces on the board"""
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    # Skip the piece being dragged
                    if selected_piece and selected_piece == (row, col):
                        continue

                    piece_key = f"{piece['color']}_{piece['type']}"
                    piece_img = self.piece_images.get(piece_key)

                    if piece_img:
                        x = self.board_offset_x + col * self.square_size + 5
                        y = self.board_offset_y + row * self.square_size + 5

                        # Check if this piece is celebrating
                        bounce_height = 0
                        if (row, col) in self.celebrating_pieces:
                            frames_remaining = self.celebrating_pieces[(row, col)]
                            total_frames = int(4.5 * 60)  # Match duration_seconds default
                            bounce_height = self.draw_celebration_effects(x, y, frames_remaining, total_frames)

                        # Draw piece with bounce offset
                        self.screen.blit(piece_img, (x, y - bounce_height))

        # Draw dragged piece
        if selected_piece and drag_pos:
            row, col = selected_piece
            piece = board[row][col]
            if piece:
                piece_key = f"{piece['color']}_{piece['type']}"
                piece_img = self.piece_images.get(piece_key)

                if piece_img:
                    x = drag_pos[0] - self.square_size // 2
                    y = drag_pos[1] - self.square_size // 2
                    self.screen.blit(piece_img, (x, y))

    def draw_valid_moves(self, valid_moves):
        """Draw indicators for valid moves"""
        for row, col in valid_moves:
            x = self.board_offset_x + col * self.square_size
            y = self.board_offset_y + row * self.square_size

            # Create semi-transparent surface
            s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            s.fill(self.valid_move_color)
            self.screen.blit(s, (x, y))

            # Draw a circle in the center
            center_x = x + self.square_size // 2
            center_y = y + self.square_size // 2
            pygame.draw.circle(self.screen, (0, 200, 0), (center_x, center_y), 10)

    def draw_player_indicator(self, current_player):
        """Draw indicator for current player"""
        color_name = txt.COLOR_WHITE if current_player == 'white' else txt.COLOR_BLACK
        text = f"{txt.STATUS_CURRENT}: {color_name}"
        rendered = self.font_medium.render(text, True, (0, 0, 0))
        x = self.board_offset_x + self.board_size + 30
        y = self.board_offset_y + 50
        self.screen.blit(rendered, (x, y))

    def draw_game_status(self, game):
        """Draw game status indicator based on game state"""
        x = self.board_offset_x + self.board_size + 30
        y = self.board_offset_y + 50

        if game.game_status == 'finished':
            # Game is finished - show result
            if game.game_result == 'draw':
                # Draw
                status_text = txt.STATUS_GAME_OVER
                status_rendered = self.font_large.render(status_text, True, (255, 140, 0))
                self.screen.blit(status_rendered, (x, y))

                result_text = txt.STATUS_DRAW
                result_rendered = self.font_medium.render(result_text, True, (100, 100, 100))
                self.screen.blit(result_rendered, (x, y + 70))
            elif game.game_result in ['white_won', 'black_won']:
                # Someone won
                winner = game.game_result.split('_')[0]
                color_name = txt.COLOR_WHITE if winner == 'white' else txt.COLOR_BLACK
                status_text = txt.STATUS_GAME_OVER
                status_rendered = self.font_large.render(status_text, True, (255, 0, 0))
                self.screen.blit(status_rendered, (x, y))

                winner_text = f"{color_name.capitalize()} {txt.STATUS_WINS}"
                winner_rendered = self.font_medium.render(winner_text, True, (0, 128, 0))
                self.screen.blit(winner_rendered, (x, y + 70))
        else:
            # Game is ongoing
            self.draw_player_indicator(game.current_player)
            # Draw check indicator if in check
            if game.is_in_check(game.current_player):
                self.draw_check_indicator()

    def draw_check_indicator(self):
        """Draw indicator when in check"""
        text = txt.STATUS_CHECK
        rendered = self.font_large.render(text, True, (255, 0, 0))
        x = self.board_offset_x + self.board_size + 30
        y = self.board_offset_y + 150
        self.screen.blit(rendered, (x, y))

    def draw_checkmate_indicator(self, winner):
        """Draw checkmate indicator with winner"""
        # Draw "CHECKMATE" text
        checkmate_text = txt.STATUS_CHECKMATE
        checkmate_rendered = self.font_large.render(checkmate_text, True, (255, 0, 0))
        x = self.board_offset_x + self.board_size + 30
        y = self.board_offset_y + 50
        self.screen.blit(checkmate_rendered, (x, y))

        # Draw winner text
        color_name = txt.COLOR_WHITE if winner == 'white' else txt.COLOR_BLACK
        winner_text = f"{color_name.capitalize()} {txt.STATUS_WINS}"
        winner_rendered = self.font_medium.render(winner_text, True, (0, 128, 0))
        y = self.board_offset_y + 120
        self.screen.blit(winner_rendered, (x, y))

    def draw_popup(self):
        """Draw popup message"""
        # Semi-transparent background
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.screen.blit(s, (0, 0))

        # Popup box (responsive to window size)
        box_width = min(500, int(self.screen.get_width() * 0.4))
        box_height = min(200, int(self.screen.get_height() * 0.2))
        box_x = (self.screen.get_width() - box_width) // 2
        box_y = (self.screen.get_height() - box_height) // 2

        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 3, border_radius=10)

        # Message text
        text = self.font_medium.render(self.popup_message, True, (255, 0, 0))
        text_x = box_x + (box_width - text.get_width()) // 2
        text_y = box_y + (box_height - text.get_height()) // 2
        self.screen.blit(text, (text_x, text_y))

    def show_violation_popup(self, message):
        """Show a popup with violation reason"""
        self.popup_message = message
        self.popup_timer = 120  # Show for 2 seconds at 60 FPS

    def get_square_from_pos(self, pos):
        """Convert screen position to board square"""
        x, y = pos
        col = (x - self.board_offset_x) // self.square_size
        row = (y - self.board_offset_y) // self.square_size

        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)
        return None

    def draw_menu(self, has_ongoing_game=False):
        """Draw the main menu screen"""
        self.screen.blit(self.background, (0, 0))

        # Title (responsive positioning)
        title = self.font_large.render(txt.MENU_TITLE, True, (0, 0, 0))
        title_x = (self.screen.get_width() - title.get_width()) // 2
        title_y = int(self.screen.get_height() * 0.125)
        self.screen.blit(title, (title_x, title_y))

        # Create button list (responsive sizing and positioning)
        buttons = []
        button_y_start = int(self.screen.get_height() * 0.3)
        button_spacing = max(60, int(self.screen.get_height() * 0.08))
        button_width = min(350, int(self.screen.get_width() * 0.35))
        button_height = max(50, int(self.screen.get_height() * 0.06))
        button_x = (self.screen.get_width() - button_width) // 2

        # Button labels (in Swedish)
        labels = [txt.MENU_START_NEW]
        if has_ongoing_game:
            labels.insert(0, txt.MENU_RESUME)
            labels.append(txt.MENU_SAVE)
            labels.append(txt.MENU_HISTORY)
        labels.append(txt.MENU_PROBLEMS)  # Add problems mode
        labels.append(txt.MENU_LOAD)
        labels.append(txt.MENU_OPTIONS)
        labels.append(txt.MENU_EXIT)

        # Draw buttons
        for i, label in enumerate(labels):
            y = button_y_start + i * button_spacing
            button_rect = pygame.Rect(button_x, y, button_width, button_height)
            buttons.append({'label': label, 'rect': button_rect})

            # Draw button
            pygame.draw.rect(self.screen, (100, 200, 100), button_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 3, border_radius=10)

            # Draw text
            text = self.font_medium.render(label, True, (0, 0, 0))
            text_x = button_x + (button_width - text.get_width()) // 2
            text_y = y + (button_height - text.get_height()) // 2
            self.screen.blit(text, (text_x, text_y))

        return buttons

    def draw_promotion_popup(self, color):
        """Draw pawn promotion piece selection popup"""
        # Semi-transparent background
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.screen.blit(s, (0, 0))

        # Popup box (responsive to window size)
        box_width = min(600, int(self.screen.get_width() * 0.5))
        box_height = min(300, int(self.screen.get_height() * 0.3))
        box_x = (self.screen.get_width() - box_width) // 2
        box_y = (self.screen.get_height() - box_height) // 2

        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 3, border_radius=10)

        # Title
        title = self.font_medium.render(txt.PROMOTION_TITLE, True, (0, 0, 0))
        title_x = box_x + (box_width - title.get_width()) // 2
        self.screen.blit(title, (title_x, box_y + int(box_height * 0.1)))

        # Draw piece options (responsive sizing)
        pieces = ['queen', 'rook', 'bishop', 'knight']
        piece_buttons = []
        piece_size = min(100, int(box_width * 0.15))
        spacing = max(20, int(box_width * 0.03))
        total_width = len(pieces) * piece_size + (len(pieces) - 1) * spacing
        start_x = box_x + (box_width - total_width) // 2
        start_y = box_y + int(box_height * 0.35)

        for i, piece_type in enumerate(pieces):
            x = start_x + i * (piece_size + spacing)
            y = start_y
            rect = pygame.Rect(x, y, piece_size, piece_size)
            piece_buttons.append({'type': piece_type, 'rect': rect})

            # Draw button
            pygame.draw.rect(self.screen, (200, 200, 200), rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 3, border_radius=10)

            # Draw piece image (scaled responsive to piece_size)
            piece_key = f"{color}_{piece_type}"
            piece_img = self.piece_images.get(piece_key)
            if piece_img:
                img_size = int(piece_size * 0.8)
                scaled_img = pygame.transform.scale(piece_img, (img_size, img_size))
                img_x = x + (piece_size - img_size) // 2
                img_y = y + (piece_size - img_size) // 2
                self.screen.blit(scaled_img, (img_x, img_y))

        return piece_buttons

    def draw_save_input_popup(self, current_text=""):
        """Draw save game name input popup"""
        # Semi-transparent background
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.screen.blit(s, (0, 0))

        # Popup box (responsive to window size)
        box_width = min(500, int(self.screen.get_width() * 0.4))
        box_height = min(250, int(self.screen.get_height() * 0.25))
        box_x = (self.screen.get_width() - box_width) // 2
        box_y = (self.screen.get_height() - box_height) // 2

        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 3, border_radius=10)

        # Title
        title = self.font_medium.render(txt.SAVE_TITLE, True, (0, 0, 0))
        title_x = box_x + (box_width - title.get_width()) // 2
        self.screen.blit(title, (title_x, box_y + 30))

        # Instruction
        instruction = self.font_small.render(txt.SAVE_INSTRUCTION, True, (0, 0, 0))
        instruction_x = box_x + (box_width - instruction.get_width()) // 2
        self.screen.blit(instruction, (instruction_x, box_y + 80))

        # Input box (responsive sizing)
        input_box_width = int(box_width * 0.8)
        input_box_height = max(30, int(box_height * 0.16))
        input_box_x = box_x + (box_width - input_box_width) // 2
        input_box_y = box_y + int(box_height * 0.48)
        input_rect = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)

        pygame.draw.rect(self.screen, (240, 240, 240), input_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), input_rect, 2)

        # Draw text
        text_surface = self.font_small.render(current_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (input_box_x + 5, input_box_y + (input_box_height - text_surface.get_height()) // 2))

        # Buttons (responsive sizing)
        button_width = int(box_width * 0.3)
        button_height = max(30, int(box_height * 0.16))
        save_button = pygame.Rect(box_x + int(box_width * 0.1), box_y + int(box_height * 0.76), button_width, button_height)
        cancel_button = pygame.Rect(box_x + int(box_width * 0.6), box_y + int(box_height * 0.76), button_width, button_height)

        # Draw save button
        pygame.draw.rect(self.screen, (100, 200, 100), save_button, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), save_button, 2, border_radius=5)
        save_text = self.font_small.render(txt.SAVE_BUTTON, True, (0, 0, 0))
        self.screen.blit(save_text, (save_button.centerx - save_text.get_width() // 2, save_button.centery - save_text.get_height() // 2))

        # Draw cancel button
        pygame.draw.rect(self.screen, (200, 100, 100), cancel_button, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), cancel_button, 2, border_radius=5)
        cancel_text = self.font_small.render(txt.CANCEL_BUTTON, True, (0, 0, 0))
        self.screen.blit(cancel_text, (cancel_button.centerx - cancel_text.get_width() // 2, cancel_button.centery - cancel_text.get_height() // 2))

        return {'input_rect': input_rect, 'save_button': save_button, 'cancel_button': cancel_button}

    def draw_load_game_popup(self, saved_games):
        """Draw load game selection popup"""
        # Semi-transparent background
        s = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.screen.blit(s, (0, 0))

        # Popup box (responsive to window size)
        box_width = min(600, int(self.screen.get_width() * 0.5))
        box_height = min(500, int(self.screen.get_height() * 0.5))
        box_x = (self.screen.get_width() - box_width) // 2
        box_y = (self.screen.get_height() - box_height) // 2

        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 3, border_radius=10)

        # Title
        title = self.font_medium.render(txt.LOAD_TITLE, True, (0, 0, 0))
        title_x = box_x + (box_width - title.get_width()) // 2
        self.screen.blit(title, (title_x, box_y + 30))

        # Game list (responsive sizing)
        game_buttons = []
        list_start_y = box_y + int(box_height * 0.16)
        item_height = max(40, int(box_height * 0.1))
        item_spacing = max(8, int(box_height * 0.02))

        if not saved_games:
            no_games_text = self.font_small.render(txt.NO_SAVED_GAMES, True, (100, 100, 100))
            text_x = box_x + (box_width - no_games_text.get_width()) // 2
            self.screen.blit(no_games_text, (text_x, list_start_y + int(box_height * 0.1)))
        else:
            for i, game in enumerate(saved_games[:6]):  # Show max 6 games
                y = list_start_y + i * (item_height + item_spacing)
                item_rect = pygame.Rect(box_x + int(box_width * 0.033), y, int(box_width * 0.933), item_height)
                game_buttons.append({'game': game, 'rect': item_rect})

                # Draw item background
                pygame.draw.rect(self.screen, (220, 220, 220), item_rect, border_radius=5)
                pygame.draw.rect(self.screen, (0, 0, 0), item_rect, 2, border_radius=5)

                # Draw filename
                filename_text = self.font_small.render(game['filename'], True, (0, 0, 0))
                self.screen.blit(filename_text, (box_x + 30, y + 8))

                # Draw modified time
                time_text = self.font_small.render(game['modified'], True, (100, 100, 100))
                self.screen.blit(time_text, (box_x + 30, y + 28))

        # Cancel button (responsive sizing)
        cancel_button_width = int(box_width * 0.25)
        cancel_button_height = max(30, int(box_height * 0.08))
        cancel_button = pygame.Rect(box_x + (box_width - cancel_button_width) // 2, box_y + box_height - int(box_height * 0.12) - cancel_button_height, cancel_button_width, cancel_button_height)
        pygame.draw.rect(self.screen, (200, 100, 100), cancel_button, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), cancel_button, 2, border_radius=5)
        cancel_text = self.font_small.render(txt.CANCEL_BUTTON, True, (0, 0, 0))
        self.screen.blit(cancel_text, (cancel_button.centerx - cancel_text.get_width() // 2, cancel_button.centery - cancel_text.get_height() // 2))

        return {'game_buttons': game_buttons, 'cancel_button': cancel_button}

    def draw_move_history(self, move_history):
        """Draw the move history in a table with white on left, black on right"""
        self.screen.blit(self.background, (0, 0))

        # Title
        title = self.font_large.render(txt.HISTORY_TITLE, True, (0, 0, 0))
        title_x = (self.screen.get_width() - title.get_width()) // 2
        title_y = int(self.screen.get_height() * 0.08)
        self.screen.blit(title, (title_x, title_y))

        # Calculate table dimensions
        table_width = min(800, int(self.screen.get_width() * 0.6))
        table_height = min(900, int(self.screen.get_height() * 0.7))
        table_x = (self.screen.get_width() - table_width) // 2
        table_y = int(self.screen.get_height() * 0.18)

        # Draw table background
        pygame.draw.rect(self.screen, (255, 255, 255), (table_x, table_y, table_width, table_height), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (table_x, table_y, table_width, table_height), 3, border_radius=10)

        # Draw header
        header_height = max(40, int(table_height * 0.05))
        pygame.draw.rect(self.screen, (200, 200, 200), (table_x, table_y, table_width, header_height), border_radius=10)
        pygame.draw.line(self.screen, (0, 0, 0), (table_x, table_y + header_height), (table_x + table_width, table_y + header_height), 2)

        # Header text
        col_width = table_width // 3
        move_num_text = self.font_medium.render(txt.HISTORY_MOVE_NUM, True, (0, 0, 0))
        white_text = self.font_medium.render(txt.HISTORY_WHITE, True, (0, 0, 0))
        black_text = self.font_medium.render(txt.HISTORY_BLACK, True, (0, 0, 0))

        self.screen.blit(move_num_text, (table_x + col_width // 2 - move_num_text.get_width() // 2, table_y + (header_height - move_num_text.get_height()) // 2))
        self.screen.blit(white_text, (table_x + col_width + col_width // 2 - white_text.get_width() // 2, table_y + (header_height - white_text.get_height()) // 2))
        self.screen.blit(black_text, (table_x + 2 * col_width + col_width // 2 - black_text.get_width() // 2, table_y + (header_height - black_text.get_height()) // 2))

        # Draw moves
        if not move_history:
            no_moves_text = self.font_small.render(txt.HISTORY_NO_MOVES, True, (100, 100, 100))
            text_x = table_x + (table_width - no_moves_text.get_width()) // 2
            text_y = table_y + header_height + int(table_height * 0.1)
            self.screen.blit(no_moves_text, (text_x, text_y))
        else:
            row_height = max(30, int(table_height * 0.04))
            start_y = table_y + header_height + 10
            max_visible_rows = (table_height - header_height - 20) // row_height

            # Organize moves into pairs (white, black)
            move_pairs = []
            for i in range(0, len(move_history), 2):
                white_move = move_history[i]
                black_move = move_history[i + 1] if i + 1 < len(move_history) else ""
                move_pairs.append((white_move, black_move))

            # Draw move pairs
            for i, (white_move, black_move) in enumerate(move_pairs):
                if i >= max_visible_rows:
                    break

                y = start_y + i * row_height
                move_num = str(i + 1)

                # Alternating row colors
                if i % 2 == 0:
                    row_rect = pygame.Rect(table_x + 2, y - 5, table_width - 4, row_height)
                    pygame.draw.rect(self.screen, (245, 245, 245), row_rect)

                # Move number
                num_text = self.font_small.render(move_num, True, (0, 0, 0))
                self.screen.blit(num_text, (table_x + col_width // 2 - num_text.get_width() // 2, y))

                # White's move
                white_text = self.font_small.render(white_move, True, (0, 0, 0))
                self.screen.blit(white_text, (table_x + col_width + col_width // 2 - white_text.get_width() // 2, y))

                # Black's move
                if black_move:
                    black_text = self.font_small.render(black_move, True, (0, 0, 0))
                    self.screen.blit(black_text, (table_x + 2 * col_width + col_width // 2 - black_text.get_width() // 2, y))

        # Back button
        button_width = min(250, int(self.screen.get_width() * 0.18))
        button_height = max(40, int(self.screen.get_height() * 0.05))
        back_button = pygame.Rect((self.screen.get_width() - button_width) // 2, table_y + table_height + 20, button_width, button_height)
        pygame.draw.rect(self.screen, (100, 200, 100), back_button, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), back_button, 3, border_radius=10)

        back_text = self.font_medium.render(txt.HISTORY_BACK, True, (0, 0, 0))
        self.screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2, back_button.centery - back_text.get_height() // 2))

        return back_button

    def draw_options(self, options):
        """Draw the options screen"""
        self.screen.blit(self.background, (0, 0))

        # Title
        title = self.font_large.render(txt.OPTIONS_TITLE, True, (0, 0, 0))
        title_x = (self.screen.get_width() - title.get_width()) // 2
        title_y = int(self.screen.get_height() * 0.1)
        self.screen.blit(title, (title_x, title_y))

        # Options box
        box_width = min(700, int(self.screen.get_width() * 0.6))
        box_height = min(600, int(self.screen.get_height() * 0.65))
        box_x = (self.screen.get_width() - box_width) // 2
        box_y = int(self.screen.get_height() * 0.2)

        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 3, border_radius=10)

        # Option 1: Capture King on Checkmate
        option_y = box_y + 30
        option_spacing = 120

        # Option toggle button
        toggle_size = 50
        toggle_x = box_x + box_width - 100
        toggle_y = option_y - 10
        toggle_rect = pygame.Rect(toggle_x, toggle_y, toggle_size, 30)

        # Draw toggle
        if options.capture_king_on_checkmate:
            pygame.draw.rect(self.screen, (100, 200, 100), toggle_rect, border_radius=15)
            toggle_text = self.font_small.render("ON", True, (0, 0, 0))
        else:
            pygame.draw.rect(self.screen, (200, 100, 100), toggle_rect, border_radius=15)
            toggle_text = self.font_small.render("OFF", True, (0, 0, 0))

        pygame.draw.rect(self.screen, (0, 0, 0), toggle_rect, 3, border_radius=15)
        self.screen.blit(toggle_text, (toggle_rect.centerx - toggle_text.get_width() // 2, toggle_rect.centery - toggle_text.get_height() // 2))

        # Option label (in Swedish)
        label = self.font_medium.render(txt.OPTIONS_CAPTURE_KING, True, (0, 0, 0))
        self.screen.blit(label, (box_x + 30, option_y))

        # Option description (in Swedish)
        desc_y = option_y + 35
        desc_lines = [txt.OPTIONS_CAPTURE_KING_DESC1, txt.OPTIONS_CAPTURE_KING_DESC2]
        for i, line in enumerate(desc_lines):
            desc_text = self.font_small.render(line, True, (80, 80, 80))
            self.screen.blit(desc_text, (box_x + 30, desc_y + i * 22))

        # Option 2: Game Mode (1/2 players)
        option_y += option_spacing
        label = self.font_medium.render(txt.OPTIONS_PLAYERS, True, (0, 0, 0))
        self.screen.blit(label, (box_x + 30, option_y))

        # Game mode buttons
        button_y = option_y + 35
        mode_1p_button = pygame.Rect(box_x + 30, button_y, 80, 30)
        mode_2p_button = pygame.Rect(box_x + 120, button_y, 80, 30)

        # 1 player button
        color_1p = (100, 200, 100) if options.game_mode == '1_player' else (200, 200, 200)
        pygame.draw.rect(self.screen, color_1p, mode_1p_button, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), mode_1p_button, 2, border_radius=5)
        text_1p = self.font_small.render(txt.OPTIONS_1_PLAYER, True, (0, 0, 0))
        self.screen.blit(text_1p, (mode_1p_button.centerx - text_1p.get_width() // 2, mode_1p_button.centery - text_1p.get_height() // 2))

        # 2 players button
        color_2p = (100, 200, 100) if options.game_mode == '2_player' else (200, 200, 200)
        pygame.draw.rect(self.screen, color_2p, mode_2p_button, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), mode_2p_button, 2, border_radius=5)
        text_2p = self.font_small.render(txt.OPTIONS_2_PLAYERS, True, (0, 0, 0))
        self.screen.blit(text_2p, (mode_2p_button.centerx - text_2p.get_width() // 2, mode_2p_button.centery - text_2p.get_height() // 2))

        # Option 3: Player Color (only for 1 player mode)
        option_y += option_spacing
        if options.game_mode == '1_player':
            label = self.font_medium.render(txt.OPTIONS_PLAYER_COLOR, True, (0, 0, 0))
            self.screen.blit(label, (box_x + 30, option_y))

            button_y = option_y + 35
            color_white_button = pygame.Rect(box_x + 30, button_y, 80, 30)
            color_black_button = pygame.Rect(box_x + 120, button_y, 80, 30)

            # White button
            color_w = (100, 200, 100) if options.player_color == 'white' else (200, 200, 200)
            pygame.draw.rect(self.screen, color_w, color_white_button, border_radius=5)
            pygame.draw.rect(self.screen, (0, 0, 0), color_white_button, 2, border_radius=5)
            text_w = self.font_small.render(txt.COLOR_WHITE.capitalize(), True, (0, 0, 0))
            self.screen.blit(text_w, (color_white_button.centerx - text_w.get_width() // 2, color_white_button.centery - text_w.get_height() // 2))

            # Black button
            color_b = (100, 200, 100) if options.player_color == 'black' else (200, 200, 200)
            pygame.draw.rect(self.screen, color_b, color_black_button, border_radius=5)
            pygame.draw.rect(self.screen, (0, 0, 0), color_black_button, 2, border_radius=5)
            text_b = self.font_small.render(txt.COLOR_BLACK.capitalize(), True, (0, 0, 0))
            self.screen.blit(text_b, (color_black_button.centerx - text_b.get_width() // 2, color_black_button.centery - text_b.get_height() // 2))

            # AI Skill Level
            option_y += option_spacing
            label = self.font_medium.render(txt.OPTIONS_AI_LEVEL, True, (0, 0, 0))
            self.screen.blit(label, (box_x + 30, option_y))

            button_y = option_y + 35
            ai_easy_button = pygame.Rect(box_x + 30, button_y, 80, 30)
            ai_med_button = pygame.Rect(box_x + 120, button_y, 80, 30)
            ai_hard_button = pygame.Rect(box_x + 210, button_y, 80, 30)

            # Easy button
            color_easy = (100, 200, 100) if options.ai_skill_level == 'easy' else (200, 200, 200)
            pygame.draw.rect(self.screen, color_easy, ai_easy_button, border_radius=5)
            pygame.draw.rect(self.screen, (0, 0, 0), ai_easy_button, 2, border_radius=5)
            text_easy = self.font_small.render(txt.OPTIONS_AI_EASY, True, (0, 0, 0))
            self.screen.blit(text_easy, (ai_easy_button.centerx - text_easy.get_width() // 2, ai_easy_button.centery - text_easy.get_height() // 2))

            # Medium button
            color_med = (100, 200, 100) if options.ai_skill_level == 'medium' else (200, 200, 200)
            pygame.draw.rect(self.screen, color_med, ai_med_button, border_radius=5)
            pygame.draw.rect(self.screen, (0, 0, 0), ai_med_button, 2, border_radius=5)
            text_med = self.font_small.render(txt.OPTIONS_AI_MEDIUM, True, (0, 0, 0))
            self.screen.blit(text_med, (ai_med_button.centerx - text_med.get_width() // 2, ai_med_button.centery - text_med.get_height() // 2))

            # Hard button
            color_hard = (100, 200, 100) if options.ai_skill_level == 'hard' else (200, 200, 200)
            pygame.draw.rect(self.screen, color_hard, ai_hard_button, border_radius=5)
            pygame.draw.rect(self.screen, (0, 0, 0), ai_hard_button, 2, border_radius=5)
            text_hard = self.font_small.render(txt.OPTIONS_AI_HARD, True, (0, 0, 0))
            self.screen.blit(text_hard, (ai_hard_button.centerx - text_hard.get_width() // 2, ai_hard_button.centery - text_hard.get_height() // 2))
        else:
            color_white_button = color_black_button = None
            ai_easy_button = ai_med_button = ai_hard_button = None

        # Back button
        button_width = min(250, int(self.screen.get_width() * 0.18))
        button_height = max(40, int(self.screen.get_height() * 0.05))
        back_button = pygame.Rect((self.screen.get_width() - button_width) // 2, box_y + box_height + 20, button_width, button_height)
        pygame.draw.rect(self.screen, (100, 200, 100), back_button, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), back_button, 3, border_radius=10)

        back_text = self.font_medium.render(txt.OPTIONS_BACK, True, (0, 0, 0))
        self.screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2, back_button.centery - back_text.get_height() // 2))

        return {
            'back_button': back_button,
            'toggle_button': toggle_rect,
            'mode_1p_button': mode_1p_button,
            'mode_2p_button': mode_2p_button,
            'color_white_button': color_white_button,
            'color_black_button': color_black_button,
            'ai_easy_button': ai_easy_button,
            'ai_med_button': ai_med_button,
            'ai_hard_button': ai_hard_button
        }

    def draw_pass_button(self):
        """Draw a pass button when player is in checkmate with capture king option enabled"""
        button_width = min(150, int(self.screen.get_width() * 0.12))
        button_height = max(40, int(self.screen.get_height() * 0.04))
        button_x = self.board_offset_x + self.board_size + 50
        button_y = self.board_offset_y + self.board_size - 100

        pass_button = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, (200, 150, 100), pass_button, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), pass_button, 3, border_radius=10)

        pass_text = self.font_medium.render(txt.STATUS_PASS_TURN, True, (0, 0, 0))
        self.screen.blit(pass_text, (pass_button.centerx - pass_text.get_width() // 2, pass_button.centery - pass_text.get_height() // 2))

        return pass_button

    def draw_problems_menu(self, problems):
        """Draw the chess problems selection menu"""
        from chess_problems import CHESS_PROBLEMS

        self.screen.blit(self.background, (0, 0))

        # Title
        title = self.font_large.render(txt.PROBLEMS_TITLE, True, (0, 0, 0))
        title_x = (self.screen.get_width() - title.get_width()) // 2
        title_y = int(self.screen.get_height() * 0.08)
        self.screen.blit(title, (title_x, title_y))

        # Subtitle
        subtitle = self.font_medium.render(txt.PROBLEMS_SELECT, True, (0, 0, 0))
        subtitle_x = (self.screen.get_width() - subtitle.get_width()) // 2
        self.screen.blit(subtitle, (subtitle_x, title_y + 60))

        # Problem buttons
        button_y_start = int(self.screen.get_height() * 0.25)
        button_spacing = max(80, int(self.screen.get_height() * 0.1))
        button_width = min(600, int(self.screen.get_width() * 0.6))
        button_height = max(70, int(self.screen.get_height() * 0.08))
        button_x = (self.screen.get_width() - button_width) // 2

        problem_buttons = []
        for i, problem in enumerate(CHESS_PROBLEMS[:5]):  # Show first 5 problems
            y = button_y_start + i * button_spacing
            button_rect = pygame.Rect(button_x, y, button_width, button_height)
            problem_buttons.append({'problem': problem, 'rect': button_rect})

            # Draw button
            pygame.draw.rect(self.screen, (150, 180, 220), button_rect, border_radius=10)
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 3, border_radius=10)

            # Draw problem title
            title_text = self.font_medium.render(problem['title'], True, (0, 0, 0))
            self.screen.blit(title_text, (button_x + 15, y + 10))

            # Draw objective and difficulty
            obj_text = self.font_small.render(f"{txt.PROBLEMS_OBJECTIVE}: {problem['objective']}", True, (50, 50, 50))
            self.screen.blit(obj_text, (button_x + 15, y + 40))

            diff_text = problem['difficulty']
            diff_label = {'easy': txt.PROBLEMS_EASY, 'medium': txt.PROBLEMS_MEDIUM, 'hard': txt.PROBLEMS_HARD}[diff_text]
            diff_rendered = self.font_small.render(f"{txt.PROBLEMS_DIFFICULTY}: {diff_label}", True, (100, 50, 150))
            self.screen.blit(diff_rendered, (button_x + button_width - 150, y + 10))

        # Back button
        button_width_back = min(250, int(self.screen.get_width() * 0.18))
        button_height_back = max(50, int(self.screen.get_height() * 0.06))
        back_button = pygame.Rect((self.screen.get_width() - button_width_back) // 2,
                                   button_y_start + 5 * button_spacing + 20,
                                   button_width_back, button_height_back)
        pygame.draw.rect(self.screen, (200, 100, 100), back_button, border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), back_button, 3, border_radius=10)

        back_text = self.font_medium.render(txt.PROBLEMS_BACK, True, (0, 0, 0))
        self.screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2,
                                     back_button.centery - back_text.get_height() // 2))

        return {'problem_buttons': problem_buttons, 'back_button': back_button}

    def draw_problem_objective(self, problem):
        """Draw the current problem's objective on the side"""
        x = self.board_offset_x + self.board_size + 30
        y = self.board_offset_y + 200

        # Objective box
        box_width = 250
        box_height = 150
        pygame.draw.rect(self.screen, (255, 255, 220), (x, y, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, box_width, box_height), 2, border_radius=10)

        # Title
        title = self.font_medium.render(txt.PROBLEMS_OBJECTIVE, True, (0, 0, 0))
        self.screen.blit(title, (x + 10, y + 10))

        # Objective text (wrap if needed)
        obj_lines = self.wrap_text(problem['objective'], box_width - 20, self.font_small)
        for i, line in enumerate(obj_lines):
            text = self.font_small.render(line, True, (50, 50, 50))
            self.screen.blit(text, (x + 10, y + 45 + i * 25))

        # Hint if available
        if 'hint' in problem:
            hint_label = self.font_small.render(f"{txt.PROBLEMS_HINT}:", True, (100, 100, 100))
            self.screen.blit(hint_label, (x + 10, y + 100))
            hint_lines = self.wrap_text(problem['hint'], box_width - 20, self.font_small)
            for i, line in enumerate(hint_lines):
                text = self.font_small.render(line, True, (120, 120, 120))
                self.screen.blit(text, (x + 10, y + 120 + i * 20))

    def wrap_text(self, text, max_width, font):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines
