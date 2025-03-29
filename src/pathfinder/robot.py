import numpy as np
from pathfinder.example import move, turn, close, connect

class Robot:
    def __init__(self, coords):
        self.angle: np.ndarray = np.array([1, 0])
        self.coords: np.ndarray = np.array(coords)

    def move_by_path(self, vectors):
        for vec in vectors:
            current_angle = np.cross(self.angle, vec) / (np.linalg.norm(vec))
            self.angle = vec / np.linalg.norm(vec)
            print(round(np.linalg.norm(vec)))

            if round(current_angle, 1) == 0:
                move(round(np.linalg.norm(vec)))
            elif round(current_angle, 1) < 0:
                turn('left')
                move(round(np.linalg.norm(vec)))
            elif round(current_angle, 1) > 0:
                turn('right')
                move(round(np.linalg.norm(vec)))
        
