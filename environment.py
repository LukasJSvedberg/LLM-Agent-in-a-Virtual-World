import numpy as np

class Environment:
    def __init__(
        self,
        x_start, y_start,
        has_box,
        box_pos_x, box_pos_y,
        x_end, y_end,
        grid_length_x, grid_length_y
    ):
        self.grid = [["." for _ in range(grid_length_x)] for _ in range(grid_length_y)]
        self.agent_pos = (x_start, y_start)
        self.deliver_pos = (x_end, y_end)
        self.has_box = has_box
        if self.has_box == False:
            self.box_pos = (box_pos_x, box_pos_y)
        else:
            self.box_pos = None

        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y

        self.start_agent_pos = self.agent_pos
        self.start_deliver_pos = self.deliver_pos
        self.start_has_box = self.has_box
        self.start_box_pos = self.box_pos


        self.task_complete = False

    def at_deliver(self):
        return self.agent_pos == self.deliver_pos

    def reached_goal(self):
        return self.has_box and self.at_deliver()

    def move(self, direction):
        x, y = self.agent_pos

        if direction == "up" and y < self.grid_length_y - 1:
            y += 1
        elif direction == "down" and y > 0:
            y -= 1
        elif direction == "right" and x < self.grid_length_x - 1:
            x += 1
        elif direction == "left" and x > 0:
            x -= 1

        self.agent_pos = (x, y)

    def pick_up(self):
        if (not self.has_box) and (self.agent_pos == self.box_pos):
            self.has_box = True
            self.box_pos = None

    def drop(self):
        if self.has_box and self.at_deliver():
            self.has_box = False
            self.box_pos = self.deliver_pos
            self.task_complete = True

    def is_complete(self):
        return self.task_complete

    def step(self, action):
        if action == "MOVE_UP":
            self.move("up")
        elif action == "MOVE_DOWN":
            self.move("down")
        elif action == "MOVE_RIGHT":
            self.move("right")
        elif action == "MOVE_LEFT":
            self.move("left")
        elif (action == "PICK_UP"):
            self.pick_up()
        elif (action == "DROP"):
            self.drop()
        observation = self.observe()
        reward = 1 if self.task_complete else 0
        done = self.task_complete
        return observation, reward, done

    def observe(self):
        return {
            "agent_pos": self.agent_pos,
            "box_pos": self.box_pos,
            "deliver_pos": self.deliver_pos,
            "has_box": self.has_box,
            "at_deliver": self.at_deliver(),
            "goal": "Pick up the box and deliver it to the delivery location",
            "x_dist_to_target":
                (self.box_pos[0] - self.agent_pos[0])
                if not self.has_box
                else
                (self.deliver_pos[0] - self.agent_pos[0]),

            "y_dist_to_target":
                (self.box_pos[1] - self.agent_pos[1])
                if not self.has_box
                else
                (self.deliver_pos[1] - self.agent_pos[1])



        }

    def valid_actions(self):
        actions = []
        x, y = self.agent_pos
        if (x > 0):
            actions.append("MOVE_LEFT")
        if (x < self.grid_length_x - 1):
            actions.append("MOVE_RIGHT")
        if (y > 0):
            actions.append("MOVE_DOWN")
        if (y < self.grid_length_y - 1):
            actions.append("MOVE_UP")
        if (not self.has_box) and (self.agent_pos == self.box_pos):
            actions.append("PICK_UP")
        if (self.has_box) and (self.deliver_pos == self.agent_pos):
            actions.append("DROP")
        return actions

    def reset(self):
        self.agent_pos = self.start_agent_pos
        self.has_box = self.start_has_box
        self.box_pos = self.start_box_pos
        self.task_complete = False
        return self.observe()

    def render(self):
        grid = [
            ["."] * self.grid_length_x
            for _ in range(self.grid_length_y)
        ]

        ax, ay = self.agent_pos

        if self.box_pos is not None and self.agent_pos == self.box_pos:
            grid[ay][ax] = "AB"
        elif self.agent_pos == self.deliver_pos:
            grid[ay][ax] = "AD"
        else:
            grid[ay][ax] = "A"

        if self.box_pos is not None and self.agent_pos != self.box_pos:
            bx, by = self.box_pos
            grid[by][bx] = "B"

        dx, dy = self.deliver_pos
        if self.agent_pos != self.deliver_pos:
            grid[dy][dx] = "D"

        for row in reversed(grid):
            print(" ".join(f"{cell:>2}" for cell in row))

        print(f"Has box: {self.has_box}")
        print(f"Task complete: {self.task_complete}")
        print()



