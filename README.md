# Pacman Multi-Agent Search

This repository contains my implementation of the **Artificial Intelligence (AI) course project** at the National and Kapodistrian University of Athens (NKUA), based on the UC Berkeley **Pacman AI Projects**.  
The project focuses on **multi-agent search algorithms** and decision-making for the Pacman game, where Pacman competes against adversarial ghosts.

---

## 📌 Project Overview

The goal of this project was to implement and compare several **adversarial search algorithms** for Pacman, in order to enable optimal decision-making under uncertainty and competition.

The following agents and evaluation functions were implemented:

1. **ReflexAgent**  
   - Chooses actions greedily based on an evaluation function.  
   - Considers distance to food and immediate ghost danger.  

2. **MinimaxAgent**  
   - Implements the **Minimax algorithm**.  
   - Pacman acts as the maximizing player, while ghosts act as minimizing players.  
   - Explores the game tree up to a given depth and returns the optimal action.  

3. **AlphaBetaAgent**  
   - Minimax with **alpha–beta pruning** for efficiency.  
   - Prunes branches of the game tree that cannot affect the final decision.  

4. **ExpectimaxAgent**  
   - Models ghosts as **stochastic agents** (choosing moves uniformly at random).  
   - Pacman maximizes expected utility rather than worst-case utility.  

5. **BetterEvaluationFunction**  
   - An improved heuristic evaluation that balances:  
     - Distance to the nearest food.  
     - Distance to ghosts (taking into account **scared timers**).  
     - Score adjustments for chasing scared ghosts and avoiding threats.  

---

## ⚙️ Features
- Implementation of **adversarial search**: Minimax, Alpha-Beta, Expectimax.  
- Reflex-based and heuristic-driven decision-making.  
- Evaluation functions that combine proximity to food and ghosts.  
- Support for stochastic opponent modeling.  
- Fully compatible with the UC Berkeley **autograder** and test suite.  

---

## ▶️ Run Instructions

Clone the Berkeley AI Project framework and replace `multiAgents.py` with this implementation.

Run Pacman with different agents:

```bash
# Reflex agent
python pacman.py -p ReflexAgent -l testClassic

# Minimax agent (depth 2)
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=2

# Alpha-beta agent
python pacman.py -p AlphaBetaAgent -l smallClassic -a depth=3

# Expectimax agent
python pacman.py -p ExpectimaxAgent -l mediumClassic -a depth=2

# Better evaluation function with Expectimax
python pacman.py -p ExpectimaxAgent -a evalFn=better -l openClassic -a depth=2
```

---

## 📄 Notes
- Project starter code and framework: UC Berkeley CS188 Pacman Projects
- My implementation is focused only on the multi-agent search (Project 2) part.
- Solutions respect the educational use policy of UC Berkeley.
