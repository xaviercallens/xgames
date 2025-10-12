"""
Input handling utilities for game development.
Provides consistent input management across different game engines.
"""

import pygame
from typing import Dict, Set, Callable, Any


class InputManager:
    """Manages keyboard and mouse input with customizable key bindings."""
    
    def __init__(self):
        self.key_bindings: Dict[int, str] = {}
        self.pressed_keys: Set[int] = set()
        self.just_pressed: Set[int] = set()
        self.just_released: Set[int] = set()
        self.actions: Dict[str, Callable] = {}
        
        # Mouse state
        self.mouse_pos = (0, 0)
        self.mouse_buttons = {1: False, 2: False, 3: False}  # Left, Middle, Right
        
    def bind_key(self, key: int, action: str):
        """Bind a key to an action name."""
        self.key_bindings[key] = action
        
    def bind_action(self, action: str, callback: Callable):
        """Bind an action to a callback function."""
        self.actions[action] = callback
        
    def update(self, events):
        """Update input state based on pygame events."""
        self.just_pressed.clear()
        self.just_released.clear()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.pressed_keys.add(event.key)
                self.just_pressed.add(event.key)
                
                # Execute bound action
                if event.key in self.key_bindings:
                    action = self.key_bindings[event.key]
                    if action in self.actions:
                        self.actions[action]()
                        
            elif event.type == pygame.KEYUP:
                self.pressed_keys.discard(event.key)
                self.just_released.add(event.key)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_buttons[event.button] = True
                
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_buttons[event.button] = False
                
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                
    def is_key_pressed(self, key: int) -> bool:
        """Check if a key is currently pressed."""
        return key in self.pressed_keys
        
    def is_key_just_pressed(self, key: int) -> bool:
        """Check if a key was just pressed this frame."""
        return key in self.just_pressed
        
    def is_key_just_released(self, key: int) -> bool:
        """Check if a key was just released this frame."""
        return key in self.just_released
        
    def is_action_pressed(self, action: str) -> bool:
        """Check if an action is currently active."""
        for key, bound_action in self.key_bindings.items():
            if bound_action == action and self.is_key_pressed(key):
                return True
        return False
        
    def get_mouse_pos(self) -> tuple:
        """Get current mouse position."""
        return self.mouse_pos
        
    def is_mouse_button_pressed(self, button: int) -> bool:
        """Check if a mouse button is pressed (1=left, 2=middle, 3=right)."""
        return self.mouse_buttons.get(button, False)


# Common key constants for easy reference
class Keys:
    """Common key constants for easier key binding."""
    
    # Movement keys
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    
    W = pygame.K_w
    A = pygame.K_a
    S = pygame.K_s
    D = pygame.K_d
    
    # Action keys
    SPACE = pygame.K_SPACE
    ENTER = pygame.K_RETURN
    ESCAPE = pygame.K_ESCAPE
    
    # Number keys
    NUM_1 = pygame.K_1
    NUM_2 = pygame.K_2
    NUM_3 = pygame.K_3
    NUM_4 = pygame.K_4
    NUM_5 = pygame.K_5
