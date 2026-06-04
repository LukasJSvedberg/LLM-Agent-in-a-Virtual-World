import json
from environment import Environment
from agent import Agent

easy_json = "worlds/easy_world.json"
medium_json = "worlds/medium_world.json"
hard_json = "worlds/hard_world.json"

def create_environment(current_json):
    with open(current_json, "r") as f:
        world = json.load(f)


    x_start = world["agent_position"][0]
    y_start = world["agent_position"][1]

    x_end = world["delivery_position"][0]
    y_end = world["delivery_position"][1]

    if world["has_box"]:
        has_box = True
        x_box_pos = x_start
        y_box_pos = y_start
    else:
        has_box = False
        x_box_pos = world["box_position"][0]
        y_box_pos = world["box_position"][1]

    grid_length_x = world["grid_width"]
    grid_length_y = world["grid_height"]

    return Environment(
        x_start,
        y_start,
        has_box,
        x_box_pos,
        y_box_pos,
        x_end,
        y_end,
        grid_length_x,
        grid_length_y
    )

def main():

    current_json = "worlds/hard_world.json"
    env = create_environment(current_json)
    agent = Agent()
    observation = env.reset()
    done = False
    step_num = 1

    max_steps = 50

    while not done and step_num < max_steps:
        print(f"\n=== Step {step_num} ===")

        env.render()

        valid_actions = env.valid_actions()

        print("Observation:")
        print(observation)

        print("Valid actions:")
        print(valid_actions)

        action = agent.act(
            observation,
            valid_actions
        )

        print("Chosen action:")
        print(action)

        observation, reward, done = env.step(action)

        step_num += 1

    if done:
        print("Package delivered")
    else:
        print("Package not delivered")

if __name__ == "__main__":
    main()
