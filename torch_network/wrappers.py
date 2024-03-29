# gym environment
import gymnasium as gym
from gymnasium import spaces

import torch
import random, datetime, numpy as np
from skimage import transform

class ResizeObservation(gym.ObservationWrapper):
    def __init__(self, env, shape):
        super().__init__(env)
        if isinstance(shape, int):
            self.shape = (shape, shape)
        else:
            self.shape = tuple(shape)

        obs_shape = self.shape + self.observation_space.shape[2:]
        print(obs_shape)
        self.observation_space = spaces.Box(low=0, high=255, shape=obs_shape, dtype=np.uint8)

    def observation(self, observation):
        resize_obs = transform.resize(observation, self.shape)
        # cast float back to uint8
        resize_obs *= 255
        resize_obs = resize_obs.astype(np.uint8)
        return resize_obs


# class GrayScaleObservation(gym.ObservationWrapper):
#     def __init__(self, env):
#         super().__init__(env)
#         obs_shape = self.observation_space.shape[:2]
#         self.observation_space = Box(low=0, high=255, shape=obs_shape, dtype=np.uint8)

#     def permute_orientation(self, observation):
#         # permute [H, W, C] array to [C, H, W] tensor
#         observation = np.transpose(observation, (2, 0, 1))
#         observation = torch.tensor(observation.copy(), dtype=torch.float)
#         return observation

#     def observation(self, observation):
#         observation = self.permute_orientation(observation)
#         transform = T.Grayscale()
#         observation = transform(observation)
#         return observation

class SkipFrame(gym.Wrapper):
    def __init__(self, env, skip):
        """Return only every `skip`-th frame"""
        super().__init__(env)
        self._skip = skip

    def step(self, action):
        """Repeat action, and sum reward"""
        total_reward = 0.0
        done = False
        for i in range(self._skip):
            # Accumulate reward and repeat the same action
            obs, reward, done, truncated, info = self.env.step(action)
            total_reward += reward
            if done:
                break
        return obs, total_reward, done, truncated, info
