# Botomy Python Bot

This repository is a carefully curated museum of ambition, overthinking, and the gradual realization that the first solution was _technically correct_ but **structurally cursed**.

What began as a simple attempt to build a Botomy bot in Python has now entered its second phase:  
a slow, deliberate transition away from a _tick-by-tick, reactionary “bothavior” model_ and toward a **state-driven bot architecture**.

This is not a glow-up.  
This is a controlled demolition followed by rebuilding with slightly better blueprints and marginally less hubris.

---

## About the Game
If you’d like to witness the digital arena where this bot repeatedly questions its life choices, the game lives here:
> [Botomy](https://botomy.com/)

---

## Project Purpose

This is still not a polished showcase.  
It is now also not pretending to be one.

This repository exists so I can:
- Learn how to structure non-trivial behavior without duct tape and vibes
- Explore state-driven AI patterns in a real, hostile environment
- Understand _why_ my previous approach felt increasingly brittle
- Make mistakes in public and document them so future-me can sigh knowingly

The original bot made decisions every tick, reacted to everything immediately, and slowly evolved into a tangled mass of conditionals, edge cases, and regret. It _worked_, but only in the way a shopping cart with one bad wheel technically moves forward.

Rather than endlessly refactoring that model, I’ve chosen to **retire it with honors** and start fresh.

---

## Architectural Shift: From Behavior to State

The old bot logic has been archived.

It was:
- reactive
- stateless
- increasingly difficult to reason about
- very good at oscillating between two bad decisions

The new bot will be:
- **state-driven**
- explicit about intent
- aware of transitions (tracking → attacking → fleeing, etc.)
- slower to write, but easier to reason about
    

This is my first serious attempt at building a state machine ever, not only for gameplay AI.  
If this feels like I’ve discovered fire and immediately decided to invent metallurgy, that’s probably an accurate observation.

This may be Dunning–Kruger in action.  
Or it may be me finally noticing the slope.

Time will tell.

---

## Repository Structure (Evolving)

- `archive/`  
    Contains the retired behavior-driven bot. It remains preserved as a reference, warning, and historical artifact.
- `bot/`  
    The new state-driven bot implementation. This is where all new development happens.
- `bot/data/`  
    Bot-specific personality, flavor text, and transitional behavior data.  
    This is intentionally isolated from game logic and may be abused for humor.    
- `main.py`  
    The boring, responsible adult. Wires the bot to the API and stays out of the way.

The structure is expected to change as understanding improves and assumptions collapse.

---

## Current Status

At present, the bot:
- Exists in two forms: archived and structural skeleton
- Has a functioning legacy implementation
- Has a new skeleton waiting for states to inhabit it    
- Is undergoing a philosophical crisis about identity and intent

No promises are made about stability, performance, or wisdom.

---

## Roadmap

### Short-Term
- Define a minimal, sane state interface
- Implement basic states (idle, seek, engage, flee)
- Make transitions explicit instead of accidental
- Avoid reinventing a worse behavior tree

### Long-Term
- Improve threat assessment and pathing
- Introduce item usage and conditional behaviors
- Expand state transitions without creating spaghetti    
- Graduate from “confused intern” to “junior developer with opinions”
    

---

## Licensing and Attribution
The old archived bot was based on the **Botomy Python Starter** project with duct tape and hope holding my functions together:

> [Botomy Python Starter](https://github.com/botomy/botomy-python-starter)

It remains under the MIT License, because freedom is important — especially the freedom for others to learn from or fix my mistakes.

---

If you’re reading this version of the repository, please assume that any architectural decisions are **tentative**, any bugs are **intentional learning opportunities**, and any misspellings are the result of prolonged exposure to Python and existential doubt.

Thank you for your patience.