import multiprocessing
import enchant
import pyautogui
import time
import numpy as np

letters = input("Letters: ")
letters = np.array([[l for l in letters[j: j + 4]] for j in range(0, len(letters), 4)]).T
print(letters)

d = enchant.Dict("en_US")
found_words = []


def check_rule(x, y):
    return 0 <= x < 4 and 0 <= y < 4


def find_words(word_pos_pair, string, positions, limit, lower_limit):
    if limit <= 0:
        return
    limit -= 1
    if len(string) >= lower_limit and d.check(string) and string not in found_words:
        word_pos_pair.put([string, positions])
        found_words.append(string)
    last_pos_x = positions[-1][0]
    last_pos_y = positions[-1][1]

    incs = [-1, 0, 1]
    for x in incs:
        for y in incs:
            if not (x == 0 and y == 0):
                pos_x = last_pos_x + x
                pos_y = last_pos_y + y
                if check_rule(pos_x, pos_y) and [pos_x, pos_y] not in positions:
                    find_words(word_pos_pair, string + letters[pos_x][pos_y], positions + [[pos_x, pos_y]], limit,
                               lower_limit)


queue = multiprocessing.Queue()

p = []
for i in range(4):
    for j in range(4):
        p.append(multiprocessing.Process(target=find_words, args=(queue, letters[i][j], [[i, j]], 8, 2)))
for process in p:
    process.start()
for process in p:
    process.join()

words = []
while queue.qsize() != 0:
    words.append(queue.get())
words = sorted(words, key=lambda x: -len(x[0]))
for pair in words:
    print(pair)

print("Ready?")
print("2")
time.sleep(1)
print("1")
time.sleep(1)
mouse_x, mouse_y = pyautogui.position()
print(mouse_x, mouse_y)

print("Ready?")
print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
temp_x, temp_y = pyautogui.position()
width = temp_x - mouse_x
print(width)

# eartwegtdkvirnsi
for i in range(len(words)):
    word, positions = words[i]
    pyautogui.moveTo(mouse_x + width * positions[0][0], mouse_y + width * positions[0][1])
    pyautogui.mouseDown()
    for j in range(1, len(positions)):
        pyautogui.moveTo(mouse_x + width * positions[j][0], mouse_y + width * positions[j][1])
    pyautogui.mouseUp()
    if i % 20 == 0 and i != 0:
        if input("Stop? (y/n) ") == "y":
            break
