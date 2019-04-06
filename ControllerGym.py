from __future__ import print_function
import gym
import time
import pygame

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

env = gym.make('LunarLander-v2')

env.reset()
tick_count = 0
while True:
    env.render()
    time.sleep(0.015)

    a = 0
    l_axis = j.get_axis(0)
    events = pygame.event.get()
    if l_axis < 0:
        a = 1
    if l_axis > 0:
        a = 3
    if j.get_button(7):
        a = 2
    # buttons = j.get_numbuttons()
    # for i in range(buttons):
    #     button = j.get_button(i)
    #     if button:
    #         print("Button {:>2} value: {}".format(i, button))

    obs, reward, done, info = env.step(a)
    if done:
        env.reset()