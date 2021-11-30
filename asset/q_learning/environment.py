import os
import time
import numpy
import json
import random
import matplotlib.pyplot as plt


class ActionSpace:
    def __init__(self):
        self.data = numpy.array([0, 1, 2, 3, 4], dtype="int8")
        self.dict = {0: "A", 1: "W", 2: "D", 3: "S", 4: "B"}  # int -> Left, Up, Right, Down, Bomb
        self.size = 5

    def sample(self):
        return numpy.random.choice(a=self.data, size=1, replace=False)[0]


class StateSpace:
    def __init__(self):
        self.data = numpy.array([_ for _ in range(315)], dtype="int8")
        self.dict = {(r, c): r * 21 + c for r in range(15) for c in range(21)}  # (row, col) -> int
        self.size = 15 * 21


class Environment:
    def __init__(self):
        # Q-Learning
        self.action_space = ActionSpace()
        self.state_space = StateSpace()
        # BomBot
        self.object_map = numpy.array(json.load(open("map.json", "r")), dtype="int8")
        self.object_dictionary = {0: "F", 1: "B", 2: "W", 3: "X"}  # int -> Floor, Wall, Brick, Player, Robot
        self.robot_position = (13, 1)
        self.robot_action = " "
        self.bomb_capacity = 1
        self.bomb_timer = 0
        self.bomb_position = []

    def __repr__(self):
        s = ""
        s += str(self.robot_position) + "\n"
        s += "*" * 45 + "\n"
        s += numpy.array2string(self.object_map, max_line_width=45, formatter={"int": lambda x: self.object_dictionary.get(x)}) + "\n"
        s += "*" * 45 + "\n"
        return s

    def reset(self):
        # Q-Learning
        self.action_space = ActionSpace()
        self.state_space = StateSpace()
        # BomBot
        self.object_map = numpy.array(json.load(open("map.json", "r")), dtype="int8")
        self.object_dictionary = {0: "F", 1: "B", 2: "W", 3: "X"}  # int -> Floor, Wall, Brick, Player, Robot
        self.robot_position = (13, 1)
        self.robot_action = " "
        self.bomb_timer = 0
        self.bomb_position = []
        return self.state_space.dict[self.robot_position]

    def step(self, action):
        # move
        if action == 0:
            r, c = self.robot_position
            if 0 <= c - 1 < len(self.object_map[0]) and not self.object_map[r][c - 1]: self.robot_position = (r, c - 1)
        if action == 1:
            r, c = self.robot_position
            if 0 <= r - 1 < len(self.object_map) and not self.object_map[r - 1][c]: self.robot_position = (r - 1, c)
        if action == 2:
            r, c = self.robot_position
            if 0 <= c + 1 < len(self.object_map[0]) and not self.object_map[r][c + 1]: self.robot_position = (r, c + 1)
        if action == 3:
            r, c = self.robot_position
            if 0 <= r + 1 < len(self.object_map) and not self.object_map[r + 1][c]: self.robot_position = (r + 1, c)
        # bomb
        if self.bomb_timer: self.bomb_timer -= 1
        if action == 4:
            self.bomb_timer = 3
            r, c = self.robot_position
            if 0 <= c - 1 < len(self.object_map[0]): self.bomb_position.append((r, c - 1))
            if 0 <= r - 1 < len(self.object_map): self.bomb_position.append((r - 1, c))
            if 0 <= c + 1 < len(self.object_map[0]): self.bomb_position.append((r, c + 1))
            if 0 <= r + 1 < len(self.object_map): self.bomb_position.append((r + 1, c))
        # reward
        reward = 0
        for r, c in self.bomb_position:
            if self.object_map[r][c] == 1 and not self.bomb_timer:
                reward += 5
                self.object_map[r][c] = 0
        # done
        done = False
        if not self.bomb_timer:
            if self.robot_position in self.bomb_position:
                done, reward = True, 0
            self.bomb_position = []
        # heuristic
        return self.state_space.dict[self.robot_position], reward, done

    def render(self):
        os.system('cls')
        print(self)
        time.sleep(0.3)


def train(num_episodes, max_steps_per_episode, learning_rate, discount_rate, exploration_rate, max_exploration_rate, min_exploration_rate, exploration_decay_rate):
    # initialize environment
    env = Environment()
    # initialize q_table
    q_table = numpy.zeros((env.state_space.size, env.action_space.size))
    # initialize reward
    rewards_all_episodes = []
    # Q-learning algorithm
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        rewards_current_episode = 0
        for step in range(max_steps_per_episode):
            # exploration-exploitation trade-off
            exploration_rate_threshold = random.uniform(0, 1)
            if exploration_rate_threshold > exploration_rate: action = numpy.argmax(q_table[state, :])
            else: action = env.action_space.sample()
            # agent performs action
            new_state, reward, done = env.step(action)
            # update q_table for Q(s, a)
            q_table[state, action] = q_table[state, action] * (1 - learning_rate) + learning_rate * (reward + discount_rate * numpy.max(q_table[new_state, :]))
            # update state, reward
            state = new_state
            rewards_current_episode += reward
            # move to next episode if done
            if done: break
        # exploration rate decay
        exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * numpy.exp(-exploration_decay_rate * episode)
        # update reward
        rewards_all_episodes.append(rewards_current_episode)
    # store q_table
    with open(f"ne={num_episodes}_ms={max_steps_per_episode}_lr={learning_rate}_dr={discount_rate}_edr={exploration_decay_rate}_mer={min_exploration_rate}.json", "w") as f:
        json.dump(q_table.tolist(), f)
    # visualize
    x, y, count = [], [], 1000
    rewards_per_thousand_episodes = numpy.split(numpy.array(rewards_all_episodes), num_episodes / 1000)
    for r in rewards_per_thousand_episodes:
        x += [count]; y += [sum(r / 1000)]; count += 1000
    plt.plot(x, y); plt.xlabel("Episode"); plt.ylabel("Reward")
    plt.title(f"ne={num_episodes}_ms={max_steps_per_episode}_lr={learning_rate}_dr={discount_rate}_edr={exploration_decay_rate}_mer={min_exploration_rate}")
    plt.savefig(f"ne={num_episodes}_ms={max_steps_per_episode}_lr={learning_rate}_dr={discount_rate}_edr={exploration_decay_rate}_mer={min_exploration_rate}.png")
    plt.show()


train(
    num_episodes=20000,
    max_steps_per_episode=3500,
    learning_rate=0.05,
    discount_rate=0.89,
    exploration_rate=1,
    max_exploration_rate=1,
    min_exploration_rate=1e-3,
    exploration_decay_rate=1e-4,
)

# initialize q_learning
# num_episodes_list = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000]
# max_steps_per_episode_list = [2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000]
# learning_rate_list = [0.02, 0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 0.97]
# discount_rate_list = [0.02, 0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 0.97]
# exploration_rate = max_exploration_rate = 1
# min_exploration_rate_list = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]
# exploration_decay_rate_list = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]
# heuristics = dict()
# for num_episodes in num_episodes_list:
#     for max_steps_per_episode in max_steps_per_episode_list:
#         for learning_rate in learning_rate_list:
#             for discount_rate in discount_rate_list:
#                 for min_exploration_rate in min_exploration_rate_list:
#                     for exploration_decay_rate in exploration_decay_rate_list:
#                         train(num_episodes, max_steps_per_episode, learning_rate, discount_rate, exploration_rate,
#                               max_exploration_rate, min_exploration_rate, exploration_decay_rate, heuristics)
#                         print(heuristics)
# with open("heuristics.json", "w") as f:
#     json.dump(heuristics, f)
