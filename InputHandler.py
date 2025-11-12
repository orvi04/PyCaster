from pynput import keyboard
import math

class InputHandler:
    def __init__(self, player):
        self.player = player
        self.pressed_keys = set()
        self.listener = None
        self._start_listener()
    
    def _on_press(self, key):
        """Called when a key is pressed"""
        try:
            if key == keyboard.Key.left:
                self.pressed_keys.add('left')
            elif key == keyboard.Key.right:
                self.pressed_keys.add('right')
            elif key == keyboard.Key.up:
                self.pressed_keys.add('up')
            elif key == keyboard.Key.down:
                self.pressed_keys.add('down')
            elif key == keyboard.Key.esc:
                self.pressed_keys.add('esc')
            else:
                if hasattr(key, 'char') and key.char:
                    self.pressed_keys.add(key.char.lower())
        except AttributeError:
            pass
    
    def _on_release(self, key):
        """Called when a key is released"""
        try:
            if key == keyboard.Key.left:
                self.pressed_keys.discard('left')
            elif key == keyboard.Key.right:
                self.pressed_keys.discard('right')
            elif key == keyboard.Key.up:
                self.pressed_keys.discard('up')
            elif key == keyboard.Key.down:
                self.pressed_keys.discard('down')
            elif key == keyboard.Key.esc:
                self.pressed_keys.discard('esc')
            else:
                if hasattr(key, 'char') and key.char:
                    self.pressed_keys.discard(key.char.lower())
        except AttributeError:
            pass
    
    def _start_listener(self):
        """Start the keyboard listener in a separate thread"""
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.daemon = True
        self.listener.start()
    
    def get_input(self):
        """Get current input state"""
        return {
            'forward': 'w' in self.pressed_keys or 'up' in self.pressed_keys,
            'backward': 's' in self.pressed_keys or 'down' in self.pressed_keys,
            'strafe_left': 'a' in self.pressed_keys,
            'strafe_right': 'd' in self.pressed_keys,
            'rotate_left': 'q' in self.pressed_keys or 'left' in self.pressed_keys,
            'rotate_right': 'e' in self.pressed_keys or 'right' in self.pressed_keys,
            'esc': 'esc' in self.pressed_keys
        }
    
    def stop(self):
        """Stop the keyboard listener"""
        if self.listener:
            self.listener.stop()

    def handle_movement(self, player, map):
        move_speed = player.move_speed
        input_state = self.get_input()
        new_x = player.x
        new_y = player.y
        
        dx = 0
        dy = 0
        
        if input_state['forward']:
            dx += math.cos(player.angle) * move_speed
            dy += math.sin(player.angle) * move_speed
        
        if input_state['backward']:
            dx -= math.cos(player.angle) * move_speed
            dy -= math.sin(player.angle) * move_speed
        
        if input_state['strafe_right']:
            dx += math.cos(player.angle + math.pi/2) * move_speed
            dy += math.sin(player.angle + math.pi/2) * move_speed
        
        if input_state['strafe_left']:
            dx += math.cos(player.angle - math.pi/2) * move_speed
            dy += math.sin(player.angle - math.pi/2) * move_speed
        
        new_x = player.x + dx
        new_y = player.y + dy
        
        if map.get_cell(new_x, new_y) != 1:
            player.x = new_x
            player.y = new_y

    def handle_rotation(self, player, rotation_speed):
        input_state = self.get_input()
        
        if input_state['rotate_left']:
            player.angle -= rotation_speed
        
        if input_state['rotate_right']:
            player.angle += rotation_speed
        
        player.angle = player.angle % (2 * math.pi)
    