from selenium import webdriver
from itertools import combinations
import math
import random
import time

driver = webdriver.Firefox(executable_path="C://Users//yiliu//PycharmProjects//online_set//geckodriver.exe")
# driver.get(input("Set Link: "))

while True:
    input_setting = input("Press h for highlight and p for auto press (default: h)")
    if input_setting != "h" and input_setting != 'p':
        input_setting = 'h'

    try:
        elem_found = True
        index = 1
        while True:
            try:
                card_elem = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div[{}]/div'.format(index))
            except:
                print("Card elements not found")
                elem_found = False
                break
            card_class = card_elem.get_attribute("class")
            if " " in card_class:
                card_class = card_class.split(" ")[1]
                break
            index += 1
        if not elem_found:
            continue

        last_combo = []
        last_styles = []
        while True:
            cards = []

            try:
                cards_found = driver.find_elements_by_class_name(card_class)
            except:
                print("Cards not found")
                break

            if len(cards_found) == 0:
                break
            for e in cards_found:
                html = e.get_attribute("innerHTML")
                number = html.count("svg") // 2
                if "squiggle" in html:
                    shape = "squiggle"
                elif "diamond" in html:
                    shape = "diamond"
                elif "oval" in html:
                    shape = "oval"
                else:
                    continue
                if "#008002" in html:
                    color = "green"
                elif "#800080" in html:
                    color = "purple"
                elif "#ff0101" in html:
                    color = "red"
                else:
                    continue
                if "transparent" in html:
                    fill = "transparent"
                elif "#mask-stripe" in html:
                    fill = "lined"
                else:
                    fill = "solid"
                cards.append([e, number, shape, color, fill])

            for combo in combinations(cards, 3):
                flag = True
                for attribute in range(1, 5):
                    s = set()
                    for card in combo:
                        s.add(card[attribute])
                    if len(s) == 2:
                        flag = False
                        break
                if flag:
                    if last_combo != combo:
                        for i, c in enumerate(last_combo):
                            driver.execute_script(
                                "arguments[0].setAttribute('style', '{}')".format(last_styles[i]), c[0])
                    for c in combo:
                        style = c[0].get_attribute("style")
                        driver.execute_script(
                            "arguments[0].setAttribute('style', '{}')".format(style + "box-shadow: 0px 0px 10px 5px yellow;"),
                            c[0])
                        last_styles.append(style)
                    last_combo = combo

                    if input_setting == "p":
                        for c in combo:
                            c[0].click()
                        time.sleep(0.3)
                    break
            time.sleep(0.3)
    except:
        continue
