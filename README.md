# Crepe Pygame Project

This project is a simple game created with Pygame where you control a pan to flip a crepe. The game includes standard movement features and a "super move" feature activated by a special key. 

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Python 3.6 or later
- Pygame

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/crepe-pygame-project.git
   ```

2. Navigate to the project directory:
   ```bash
   cd crepe-pygame-project
   ```

3. Install the required dependencies:
   ```bash
   pip install pygame
   ```

## Usage

To start the game, run the main script:
```bash
python main.py
```

## Project Structure

```
crepe-pygame-project/
├── main.py               # Main game script
├── pan.py                # Pan class to control the pan
├── crepe.py              # Crepe class to handle the crepe
├── score.py              # Score class to display the score
├── pan_skin.png          # Image of the pan
├── background.jpg        # Background image
└── README.md             # This file
```

## Features

### Pan Control

- **Standard Movement**: Use the arrow keys to move the pan.
- **Super Move**: Hold the `C` key to activate the super move for 3 seconds.
- **Flip the Crepe**: Press the spacebar to tilt the pan and launch the crepe.

### Pan Rotation

The pan can be tilted to launch the crepe by pressing the spacebar. The crepe is launched when the pan's angle is released.

### Crepe Update

The crepe is updated based on the position and angle of the pan. If the crepe falls off the screen, the game ends.

### Score

The score is updated and displayed based on the player's actions.




Enjoy playing our crepe game!

## Authors

Valentin Auffray - Grégoire Badiche - Jude Guehl - Samy Gharnaout - Oscar Masdupuy

