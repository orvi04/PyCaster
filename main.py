from Map import Map
from RayCaster import RayCaster
from Renderer import Renderer
from Player import Player
from InputHandler import InputHandler
import math
import time

def create_map():
    map = Map(10, 10)
    map.set_map([
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,0,1,1,0,1],
        [1,0,1,0,0,0,0,1,0,1],
        [1,0,0,0,1,1,0,0,0,1],
        [1,0,0,0,1,1,0,0,0,1],
        [1,0,1,0,0,0,0,1,0,1],
        [1,0,1,1,0,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]
    ])
    return map

def main():
    SCREEN_WIDTH = 150
    SCREEN_HEIGHT = 50
    FOV = math.pi / 2
    MOVE_SPEED = 0.05
    ROTATION_SPEED = 0.05
    TARGET_FPS = 30
    FRAME_TIME = 1.0 / TARGET_FPS
    
    game_map = create_map()
    player = Player(2.0, 2.0, 0.0, FOV, MOVE_SPEED)
    input_handler = InputHandler(player)
    raycaster = RayCaster(game_map, player)
    renderer = Renderer(player, SCREEN_WIDTH, SCREEN_HEIGHT, 'alt')
    
    print("Ray Casting Game Started!")
    print("Controls: W/S - Move, A/D - Strafe, Q/E or Arrow Keys - Rotate, ESC - Quit")
    print("Press any key to start...")
    time.sleep(1)
    
    running = True
    
    try:
        while running:
            frame_start = time.time()
            
            input_state = input_handler.get_input()
            if input_state['esc']:
                running = False
                break
            
            input_handler.handle_movement(player, game_map)
            input_handler.handle_rotation(player, ROTATION_SPEED)
            
            ray_distances = raycaster.cast_fan(SCREEN_WIDTH)
            
            renderer.render_frame(ray_distances)
            
            frame_end = time.time()
            frame_duration = frame_end - frame_start
            sleep_time = FRAME_TIME - frame_duration
            if sleep_time > 0:
                time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    finally:
        input_handler.stop()
        print("\nGame ended. Thanks for playing!")

if __name__ == "__main__":
    main()

