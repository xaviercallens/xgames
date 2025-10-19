"""
Multiplayer menu system for player and AI configuration.
Allows selecting number of human/AI players and AI modes.
"""

import pygame
from . import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GREEN, RED, BLUE, YELLOW, BROWN


class MultiplayerMenu:
    """Menu for configuring multiplayer games."""
    
    def __init__(self, screen):
        """Initialize multiplayer menu."""
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Game mode selection
        self.game_modes = [
            {'name': '1v1 (Human vs AI)', 'humans': 1, 'ais': 1},
            {'name': '2 Players (Local)', 'humans': 2, 'ais': 0},
            {'name': '3 Players (Local)', 'humans': 3, 'ais': 0},
            {'name': '4 Players (Local)', 'humans': 4, 'ais': 0},
            {'name': '2 Human + 1 AI', 'humans': 2, 'ais': 1},
            {'name': '2 Human + 2 AI', 'humans': 2, 'ais': 2},
            {'name': '3 Human + 1 AI', 'humans': 3, 'ais': 1},
        ]
        
        self.selected_mode = 0
        self.pulse_timer = 0
        self.pulse_speed = 2.0
    
    def show_game_mode_selection(self):
        """
        Show game mode selection menu.
        
        Returns:
            Selected game mode dict or None
        """
        clock = pygame.time.Clock()
        
        while True:
            dt = clock.tick(60) / 1000.0
            self.pulse_timer += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_mode = (self.selected_mode - 1) % len(self.game_modes)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_mode = (self.selected_mode + 1) % len(self.game_modes)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return self.game_modes[self.selected_mode]
                    elif event.key == pygame.K_ESCAPE:
                        return None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i, rect in enumerate(self.mode_rects):
                        if rect.collidepoint(mouse_pos):
                            self.selected_mode = i
                            return self.game_modes[i]
            
            self._draw_game_mode_selection()
            pygame.display.flip()
    
    def show_player_configuration(self, game_mode):
        """
        Show player configuration menu.
        
        Args:
            game_mode: Selected game mode
            
        Returns:
            List of player configurations
        """
        total_players = game_mode['humans'] + game_mode['ais']
        players_config = []
        
        # Initialize player configs
        for i in range(total_players):
            if i < game_mode['humans']:
                players_config.append({
                    'id': i + 1,
                    'type': 'human',
                    'name': f'Player {i + 1}',
                    'ai_mode': None,
                    'color': self._get_player_color(i)
                })
            else:
                players_config.append({
                    'id': i + 1,
                    'type': 'ai',
                    'name': f'AI {i - game_mode["humans"] + 1}',
                    'ai_mode': 'intermediate_heuristic',
                    'color': self._get_player_color(i)
                })
        
        # If only AI players, return default config
        if game_mode['humans'] == 0:
            return players_config
        
        # Show configuration for each player
        current_player = 0
        while current_player < total_players:
            if players_config[current_player]['type'] == 'human':
                result = self.show_player_name_input(current_player, players_config)
                if result is None:
                    return None
                players_config[current_player]['name'] = result
            else:
                result = self.show_ai_mode_selection(current_player, players_config)
                if result is None:
                    return None
                players_config[current_player]['ai_mode'] = result
            
            current_player += 1
        
        return players_config
    
    def show_player_name_input(self, player_id, players_config):
        """
        Show player name input dialog.
        
        Args:
            player_id: Player ID (0-based)
            players_config: Current player configuration
            
        Returns:
            Player name or None
        """
        clock = pygame.time.Clock()
        player_name = players_config[player_id]['name']
        cursor_visible = True
        cursor_timer = 0
        
        while True:
            dt = clock.tick(60) / 1000.0
            cursor_timer += dt
            if cursor_timer > 0.5:
                cursor_visible = not cursor_visible
                cursor_timer = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return player_name if player_name else f'Player {player_id + 1}'
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    elif event.unicode.isprintable() and len(player_name) < 20:
                        player_name += event.unicode
            
            self._draw_player_name_input(player_id, player_name, cursor_visible)
            pygame.display.flip()
    
    def show_ai_mode_selection(self, player_id, players_config):
        """
        Show AI mode selection menu.
        
        Args:
            player_id: Player ID (0-based)
            players_config: Current player configuration
            
        Returns:
            Selected AI mode or None
        """
        ai_modes = [
            {'name': 'Beginner Bot', 'type': 'simple', 'win_rate': 10.0},
            {'name': 'Intermediate Bot', 'type': 'heuristic', 'win_rate': 35.0},
            {'name': 'Advanced Bot (Smart)', 'type': 'advanced_heuristic', 'win_rate': 60.0},
        ]
        
        selected_ai = 0
        clock = pygame.time.Clock()
        
        while True:
            dt = clock.tick(60) / 1000.0
            self.pulse_timer += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        selected_ai = (selected_ai - 1) % len(ai_modes)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        selected_ai = (selected_ai + 1) % len(ai_modes)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return ai_modes[selected_ai]['type']
                    elif event.key == pygame.K_ESCAPE:
                        return None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i, rect in enumerate(self.ai_mode_rects):
                        if rect.collidepoint(mouse_pos):
                            return ai_modes[i]['type']
            
            self._draw_ai_mode_selection(player_id, ai_modes, selected_ai)
            pygame.display.flip()
    
    def show_summary(self, players_config):
        """
        Show game configuration summary.
        
        Args:
            players_config: Player configuration list
            
        Returns:
            True to start game, False to go back
        """
        clock = pygame.time.Clock()
        selected = 0  # 0 = Start, 1 = Back
        
        while True:
            dt = clock.tick(60) / 1000.0
            self.pulse_timer += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        selected = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        selected = 1
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return selected == 0
                    elif event.key == pygame.K_ESCAPE:
                        return False
            
            self._draw_summary(players_config, selected)
            pygame.display.flip()
    
    # Private drawing methods
    
    def _draw_game_mode_selection(self):
        """Draw game mode selection screen."""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("🎮 Select Game Mode", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_small.render("Choose how many players", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 140))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Draw modes
        self.mode_rects = []
        start_y = 200
        mode_height = 70
        mode_spacing = 10
        mode_width = 600
        
        for i, mode in enumerate(self.game_modes):
            y = start_y + i * (mode_height + mode_spacing)
            x = (SCREEN_WIDTH - mode_width) // 2
            
            rect = pygame.Rect(x, y, mode_width, mode_height)
            self.mode_rects.append(rect)
            
            # Determine colors
            if i == self.selected_mode:
                bg_color = (60, 60, 100)
                border_color = GREEN
                border_width = 4
                
                # Pulse effect
                pulse = abs(pygame.math.Vector2(0, 1).rotate(
                    self.pulse_timer * 360 * self.pulse_speed).y)
                glow = int(20 + 20 * pulse)
                bg_color = tuple(min(255, c + glow) for c in bg_color)
            else:
                bg_color = (40, 40, 60)
                border_color = (100, 100, 150)
                border_width = 2
            
            # Draw box
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
            pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=10)
            
            # Draw text
            text = self.font_small.render(mode['name'], True, WHITE)
            text_rect = text.get_rect(left=rect.left + 20, centery=rect.centery)
            self.screen.blit(text, text_rect)
            
            # Draw player count
            count_text = self.font_tiny.render(
                f"👤 {mode['humans']} | 🤖 {mode['ais']}", True, (200, 200, 200)
            )
            count_rect = count_text.get_rect(right=rect.right - 20, centery=rect.centery)
            self.screen.blit(count_text, count_rect)
        
        # Instructions
        instructions = [
            "↑↓ or W/S to select",
            "ENTER or SPACE to confirm",
            "ESC to go back"
        ]
        
        y = SCREEN_HEIGHT - 100
        for instruction in instructions:
            text = self.font_tiny.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 25
    
    def _draw_player_name_input(self, player_id, player_name, cursor_visible):
        """Draw player name input screen."""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("👤 Player Name", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Player info
        player_num = self.font_medium.render(f"Player {player_id + 1}", True, WHITE)
        player_num_rect = player_num.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(player_num, player_num_rect)
        
        # Input box
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, 350, 400, 60)
        pygame.draw.rect(self.screen, (60, 60, 100), input_box, border_radius=10)
        pygame.draw.rect(self.screen, GREEN, input_box, 3, border_radius=10)
        
        # Input text
        text = self.font_medium.render(player_name, True, WHITE)
        text_rect = text.get_rect(center=input_box.center)
        self.screen.blit(text, text_rect)
        
        # Cursor
        if cursor_visible:
            cursor_x = text_rect.right + 5
            pygame.draw.line(self.screen, GREEN, (cursor_x, input_box.top + 10),
                           (cursor_x, input_box.bottom - 10), 2)
        
        # Instructions
        hint = self.font_small.render("Type name and press ENTER", True, WHITE)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 450))
        self.screen.blit(hint, hint_rect)
    
    def _draw_ai_mode_selection(self, player_id, ai_modes, selected_ai):
        """Draw AI mode selection screen."""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("🤖 Select AI Mode", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # AI player info
        ai_num = self.font_medium.render(f"AI Player {player_id}", True, WHITE)
        ai_num_rect = ai_num.get_rect(center=(SCREEN_WIDTH // 2, 140))
        self.screen.blit(ai_num, ai_num_rect)
        
        # Draw AI modes
        self.ai_mode_rects = []
        start_y = 200
        mode_height = 80
        mode_spacing = 15
        mode_width = 600
        
        for i, mode in enumerate(ai_modes):
            y = start_y + i * (mode_height + mode_spacing)
            x = (SCREEN_WIDTH - mode_width) // 2
            
            rect = pygame.Rect(x, y, mode_width, mode_height)
            self.ai_mode_rects.append(rect)
            
            # Determine colors
            if i == selected_ai:
                bg_color = (60, 60, 100)
                border_color = GREEN
                border_width = 4
                
                # Pulse effect
                pulse = abs(pygame.math.Vector2(0, 1).rotate(
                    self.pulse_timer * 360 * self.pulse_speed).y)
                glow = int(20 + 20 * pulse)
                bg_color = tuple(min(255, c + glow) for c in bg_color)
            else:
                bg_color = (40, 40, 60)
                border_color = (100, 100, 150)
                border_width = 2
            
            # Draw box
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
            pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=10)
            
            # Draw name
            name_text = self.font_small.render(mode['name'], True, WHITE)
            name_rect = name_text.get_rect(left=rect.left + 20, top=rect.top + 10)
            self.screen.blit(name_text, name_rect)
            
            # Draw win rate
            wr_text = self.font_tiny.render(
                f"Expected Win Rate: {mode['win_rate']:.0f}%", True, (200, 200, 200)
            )
            wr_rect = wr_text.get_rect(left=rect.left + 20, bottom=rect.bottom - 10)
            self.screen.blit(wr_text, wr_rect)
        
        # Instructions
        instructions = [
            "↑↓ or W/S to select",
            "ENTER or SPACE to confirm",
            "ESC to go back"
        ]
        
        y = SCREEN_HEIGHT - 100
        for instruction in instructions:
            text = self.font_tiny.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 25
    
    def _draw_summary(self, players_config, selected):
        """Draw game configuration summary."""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("🎮 Game Configuration", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Player list
        y = 180
        for i, player in enumerate(players_config):
            # Player info
            if player['type'] == 'human':
                player_text = f"👤 {player['name']} (Human)"
                color = (100, 255, 100)
            else:
                player_text = f"🤖 {player['name']} ({player['ai_mode']})"
                color = (255, 100, 100)
            
            text = self.font_small.render(player_text, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 50
        
        # Buttons
        button_y = SCREEN_HEIGHT - 150
        
        # Start button
        start_color = GREEN if selected == 0 else WHITE
        start_text = self.font_medium.render("START GAME", True, start_color)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2 - 150, button_y))
        self.screen.blit(start_text, start_rect)
        
        if selected == 0:
            pygame.draw.rect(self.screen, GREEN, start_rect.inflate(20, 20), 2, border_radius=5)
        
        # Back button
        back_color = GREEN if selected == 1 else WHITE
        back_text = self.font_medium.render("GO BACK", True, back_color)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2 + 150, button_y))
        self.screen.blit(back_text, back_rect)
        
        if selected == 1:
            pygame.draw.rect(self.screen, GREEN, back_rect.inflate(20, 20), 2, border_radius=5)
        
        # Instructions
        hint = self.font_tiny.render("↑↓ or W/S to select, ENTER to confirm", True, WHITE)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)
    
    def _get_player_color(self, player_id):
        """Get color for player ID."""
        colors = [GREEN, RED, BLUE, YELLOW]
        return colors[player_id % len(colors)]
