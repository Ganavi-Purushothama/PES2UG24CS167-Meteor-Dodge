# Meteor Dodge Repair Lab

This project is a space survival obstacle-dodging game using **Pygame**. It introduces students to directional velocity vectors, radial collision math, starfield rendering, particle trails, and dynamic difficulty scaling within an object-oriented codebase.
---

## What's Provided

A working Meteor Dodge game with:

- A responsive player starship with engine trail effects and 4-directional movement (`WASD` / Arrow Keys)
- Procedurally generated starfield background
- Irregular polygonal meteors that rotate and tumble downwards at randomized speeds and angles
- Radius-based circular collision detection against the ship
- Dynamic spawn intervals that decrease as survival time increases
- Launch state, survival timer HUD, and a Game Over overlay with restart functionality

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** Press SPACE to launch or restart. Use WASD or Arrow Keys to pilot the ship.
| Key | Action |
|-----|--------|
| W/A/S/D or Arrows | Move ship |
| SPACE | Start / Restart |

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the laser firing / input state bug

Pressing SPACE is designed to launch the game when waiting and fire a defensive projectile during flight. In the current build of game_engine.handle_events(), pygame.K_SPACE only checks if self.game_over: self.reset() else: self.started = True. Once the game is running, pressing SPACE does nothing because there is no condition handling weapon fire or projectile generation while self.started is active. Implement laser projectile firing when SPACE is pressed during active gameplay so players can shoot down incoming meteors

### Task 2: Implement meteor fragments on destruction

When an incoming large meteor is struck and destroyed by a laser, make it split into 2 smaller child meteor fragments traveling outwards at diverging angles instead of vanishing immediately. Small meteors should be completely eliminated when hit.
 
### Task 3: Implement shield power-up orbs

Introduce a collectible shield orb that periodically drifts down across the screen. Touching the orb equips the player ship with an energy shield barrier that absorbs one meteor collision without triggering Game Over.

### Task 4: Implement surviving score multipliers

Survival score currently increments at a flat rate frame-by-frame. Implement an escalating multiplier in game_engine.update() that increases by 1x for every 10 continuous seconds survived without getting hit, resetting back to 1x if a shield is lost.
---

## Expected Behavior

- Pressing SPACE begins flight from the title screen.
- Arrow keys or WASD steer the ship smoothly inside the window dimensions.   
- Meteors continuously spawn from the top and fall at varying trajectories and rotation speeds.
- Colliding with any meteor ends the run and displays the final survival time.
- Pressing SPACE on the Game Over screen resets all objects and timers for a new run.

## Folder Structure

```
meteor-dodge/
├── main.py
├── requirements.txt
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── ship.py
│   └── meteor.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
