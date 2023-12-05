import gym_mariokart64.mariokart64env as mk64gym
import subprocess
import threading
import time
import cv2

# paths
lib_path = "./gym_mariokart64/m64py/libmupen64plus.so.2"
plugin_path = "./gym_mariokart64/m64py/"
rom_path = "./rom/mariokart64.n64"
tensorboard_dir = 'logs/'
log_dir = 'tmp/'


env = mk64gym.MarioKart64Env()
env.set_game_screen(useDefault=True)
env.set_paths(lib_path, plugin_path, rom_path)
# env = SkipFrame(env, skip=3)
# env = FrameStack(env, num_stack=3)

# create thread for concurrency
thread = threading.Thread(target=env.start_game)
thread.start()
# sleep to prevent reading memory before emulator starts
time.sleep(9)


# check observation
# env.reset()
# # image = env.get_observation()
# image = env.get_observation_full()
# cv2.imshow('image', image)
# cv2.waitKey()
# time.sleep(5)

# test env
for episode in range(5):
    obs = env.reset()
    subprocess.call(["xdotool", "keydown", "Shift"])
    done = False
    totalReward = 0
    while not done:
        obs, reward, done, truncated, info = env.step(env.action_space.sample())
        print("Reward: " + str(reward))
        totalReward += reward
    print(f'Total reward for episode {episode} is {totalReward}')

# CHECKPOINT_DIR = './train/'
# LOG_DIR = './logs/'

# callback = mk64gym.TrainLoggingCallback(check_freq=1000, save_path=CHECKPOINT_DIR)

# # create dqn model
# model = DQN('CnnPolicy', env, tensorboard_log=LOG_DIR, verbose=1, buffer_size=10000, learning_starts=1000)

# # train
# model.learn(total_timesteps=5000, callback=callback)