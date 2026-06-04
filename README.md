# LLM Package Delivery Agent

## Overview

This project implements an LLM-powered agent operating in a virtual 2D grid world.

The agent receives structured observations from the environment, chooses actions using a language model, and interacts with the world until it completes a task.
### Goal

The agent must:

1. Navigate to a package.
2. Pick up the package.
3. Navigate to a specified delivery location.
4. Deliver the package.

---

## Environment

The environment is a discrete 2D grid world.

### Objects

| Symbol | Meaning           |
| ------ | ----------------- |
| A      | Agent             |
| B      | Package           |
| D      | Delivery location |
| .      | Empty space       |

Example:

```text
. . . . D
. . B . .
. . . . .
. . . . .
A . . . .
```

---

## Observation Space

The environment provides structured observations to the agent.

Example:

```json
{
  "agent_pos": [2, 3],
  "box_pos": [2, 2],
  "deliver_pos": [4, 4],
  "has_box": false,
  "x_dist_to_target": 0,
  "y_dist_to_target": -1
}
```

The active target is:

* the package if the agent is not carrying it
* the delivery location if the agent is carrying it
* The LLM tries to go in the direction to make (x_dist_to_target, y_dist_to_target) = (01, 01)

---

## Action Space

The agent can choose from the following actions:

```text
MOVE_LEFT
MOVE_RIGHT
MOVE_UP
MOVE_DOWN
PICK_UP
DROP
```

The environment validates all actions before applying them. We can only perform PICK_UP if we are at a box, DROP if we are at the delivery 
location, and we cannot perform MOVE_LEFT if agent_pos[0] = 0 (x coordinate of the agent), MOVE_DOWN if agent_pos[1] = 0 (y coordinate of the agent), etc.

---

## Agent Harness

The agent-environment interaction loop is:

```text
Observation
    ↓
LLM
    ↓
Action
    ↓
Environment Update
    ↓
New Observation
    ↓
(repeats until we reach the goal)
```

The language model receives:

* current observation
* valid actions
* distance-to-target information

and returns a single action.

We are currently using the gpt-4.1-mini model provided by OpenAI.

---

## Project Structure

```text
.
├── agent.py
├── environment.py
├── main.py
├── worlds/
│   └── easy_world.json
├── logs/
│   └── successful_run.txt
└── README.md
```

---

## Running

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your OpenAI API key:

```bash
OPENAI_API_KEY=<your_key>
```

Run:

```bash
python main.py
```
We can specify which world we want by setting the variable 'current_json' to another JSON file


---



## Example Output

```text
=== Step 1 ===
 .  .  .  .  D
 .  .  B  .  .
 .  .  .  .  .
 .  .  .  .  .
 A  .  .  .  .
Has box: False
Task complete: False

Observation:
{'agent_pos': (0, 0), 'box_pos': (2, 3), 'deliver_pos': (4, 4), 'has_box': False, 'at_deliver': False, 'goal': 'Pick up the box and deliver it to the delivery location', 'x_dist_to_target': 2, 'y_dist_to_target': 3}
Valid actions:
['MOVE_RIGHT', 'MOVE_UP']
Chosen action:
MOVE_RIGHT

=== Step 2 ===
 .  .  .  .  D
 .  .  B  .  .
 .  .  .  .  .
 .  .  .  .  .
 .  A  .  .  .
```

---

## Design Decisions

### Structured Observations

The environment provides structured state rather than raw text. This allows the LLM to work with distinct variables which are easier for them to reason with as opposed to text where LLM's need to interpret what the text actually means.
We only convert into the grid for rendering for the user, because we want as few useful parameters for the LLM to digest.

### Restricted Action Space

The agent can only choose from valid actions provided by the environment. We automatically warn the user if the LLM tries non specified actions. Using prompting, we make sure that we only return a one word answer which
should be the same as one of the agent current actions, so the LLM should always produce the right response.

### Separation of Responsibilities

* `environment.py` manages world state and rules.
* `agent.py` manages LLM interaction.
* `main.py` orchestrates the agent-environment loop.

### What worked well, and could be improved

The LLM is often able to move towards the relevant object effectively by using the x_dist_to_target and y_dist_to_target variables. As a result, it can solve the task in a number of moves that is close to the optimal solution. The separation of responsibilities across different components is also well designed, making it straightforward to modify the environment either by editing the JSON configuration or by changing the underlying model.

However, the model occasionally performs redundant actions as it approaches the goal. For example, in easy_world_log, the model does not immediately move to the delivery location even when it is only one square away. In addition, the model's limited memory would make it difficult to handle more complex environments, such as those containing walls or other obstacles. Supporting these extensions would likely require modifications to the prompting strategy.