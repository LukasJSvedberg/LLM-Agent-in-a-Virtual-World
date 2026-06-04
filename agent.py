from openai import OpenAI
import os
class Agent:

    def __init__(self):
        self.client = OpenAI()

    def act(self, observation, valid_actions):
        prompt = (
            f"You are a delivery robot.\n\n"

            f"Agent position: {observation['agent_pos']}\n"
            f"Has box: {observation['has_box']}\n"
            f"x_dist_to_target: {observation['x_dist_to_target']}\n"
            f"y_dist_to_target: {observation['y_dist_to_target']}\n"
            f"Valid actions: {valid_actions}\n\n"

            f"Robot Rules:\n"
            f"- If x_dist_to_target > 0, prefer MOVE_RIGHT.\n"
            f"- If x_dist_to_target < 0, prefer MOVE_LEFT.\n"
            f"- If y_dist_to_target > 0, prefer MOVE_UP.\n"
            f"- If y_dist_to_target < 0, prefer MOVE_DOWN.\n"
            f"- if x_dist_to_target == 0, avoid MOVE_RIGHT and MOVE_LEFT.\n"
            f"- if x_dist_to_target == 0, avoid MOVE_UP and MOVE_DOWN.\n"
            f"- If standing on the box, choose PICK_UP.\n"
            
            f"- If standing on the delivery location while holding the box, choose DROP.\n\n"

            f"Return exactly one action from Valid actions."
        )

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        action = response.output_text.strip()
        if action not in valid_actions:
            print("ACTION IS NOT VALID")
            return valid_actions[0]
        return action



