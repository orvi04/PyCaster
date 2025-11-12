from RayCaster import RayCaster
import os
import sys
import math

class Renderer:
    def __init__(self, player, screen_width, screen_height, gradient):
        self.player = player
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gradient = gradient

    def clear_screen(self):
        os.system('cls')

    ascii_gradient = "@%#*+=-:. "
    ascii_gradient_alt = "█▓▒░ "
    
    def distance_to_shading(self, distance, max_distance):
        if distance > max_distance:
            distance = max_distance
        else:
            if distance < 0:
                distance = 0
        grad_to_use = self.ascii_gradient if self.gradient == 'default' else self.ascii_gradient_alt
        return grad_to_use[int((distance / max_distance) * (len(grad_to_use) - 1))]

    def render_frame(self, ray_distances):
        frame = [[' '] * self.screen_width for _ in range(self.screen_height)]
        proj_plane_dist = 0.5 * self.screen_height

        max_distance = max(ray_distances)

        for col in range(self.screen_width):
            ray_index = int(col * len(ray_distances) / self.screen_width)
            ray_distance = ray_distances[ray_index]

            angle_step = self.player.fov / len(ray_distances)
            ray_angle = self.player.angle - self.player.fov / 2 + ray_index * angle_step
            angle_diff = ray_angle - self.player.angle
            
            corrected_distance = max(0.0001, ray_distance * math.cos(angle_diff))
            wall_height = min(self.screen_height, int(proj_plane_dist / corrected_distance))
            wall_top = (self.screen_height - wall_height) // 2
            wall_bottom = wall_top + wall_height
            
            shade_char = self.distance_to_shading(corrected_distance, max_distance)

            for row in range(self.screen_height):
                if row < wall_top:
                    frame[row][col] = ' '
                elif row < wall_bottom:
                    frame[row][col] = shade_char
                else:
                    frame[row][col] = '.'

        frame_string = '\n'.join(''.join(row) for row in frame)
        
        # Clear screen once
        self.clear_screen()
        
        sys.stdout.write(frame_string)
        sys.stdout.flush()