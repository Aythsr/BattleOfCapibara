import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src import game

if __name__ == "__main__":
    game.run()
