import math

class RayCaster:
    def __init__(self, map, player):
        self.map = map
        self.player = player

    def cast_ray(self, rayAngle):
        ray_direction = (math.cos(rayAngle), math.sin(rayAngle))
        ray_position = (self.player.x, self.player.y)
        ray_length = 0
        step_size = 0.1  # Smaller steps for more accuracy
        while ray_length < 100:
            ray_position = (ray_position[0] + ray_direction[0] * step_size, 
                          ray_position[1] + ray_direction[1] * step_size)
            ray_length += step_size
            if self.map.get_cell(ray_position[0], ray_position[1]) == 1:
                return ray_length
        return 100

    def cast_fan(self, num_rays):
        rays = []
        for i in range(num_rays):
            ray_angle = self.player.angle - self.player.fov / 2 + i * self.player.fov / num_rays
            rays.append(self.cast_ray(ray_angle))
        return rays

    