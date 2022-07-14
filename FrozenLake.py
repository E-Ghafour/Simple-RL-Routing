import gym
env = gym.make("FrozenLake-v1")
observation = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, done = env.step(action)

    if done:
        observation = env.reset(return_info=True)
env.close()