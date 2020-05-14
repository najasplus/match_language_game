# -*- coding: utf-8 -*-
#!/usr/bin/python3

import PySimpleGUI as sg
import random
import pandas

def parse_tab_delimited(input_tsv):
    """Read tab-delimited text file, 
    return first two columns as lists,
    store them in global variables list1 and list2"""
    global list1
    global list2
    input_df = pandas.read_csv(input_tsv, sep='\t', encoding='utf-8', header=None)
    list1 = list(input_df[input_df.columns[0]])
    list2 = list(input_df[input_df.columns[1]])
    return list1, list2

def find_element_in_lists(word):
    """Find element in 2 globally defined lists,
    return the element index and the list it belongs to"""
    if word in list1:
        return list1.index(word), 1
    elif word in list2:
        return list2.index(word), 2
    else:
        print("Word " + word + "not found in word lists")

def compare_pair(pair):
    """take a list of two words, check if it's a word-translation pair"""
    word1_i, list_num1 = find_element_in_lists(pair[0])    
    word2_i, list_num2 = find_element_in_lists(pair[1])    

    if list_num1 == list_num2:
        return False
    elif word1_i == word2_i:
        return True
    else:
        return False

def check_word_pair(pair, window):
    """Take the list of two words, if they are word-translation pair, return True and update buttons
    otherwise return False and return buttons to initial state"""
    is_match = compare_pair(pair)

    if is_match:
        window.FindElement(pair[0]).Update(disabled = True, button_color=('black', '#2cc406'))
        window.FindElement(pair[1]).Update(disabled = True, button_color=('black', '#2cc406'))
        return True
    else:
        window.FindElement(pair[0]).Update(button_color=('black', '#ffd22b'))
        window.FindElement(pair[1]).Update(button_color=('black', '#ffd22b'))
        return False


def get_random_list(num_elements):
    """takes integer num_elements, uses global list1 and list2 (words and translations) lists
    selects a number of pairs equal to num_elements or length of the list (if it's smaller,
    returns randomized list from selected pairs"""
    if num_elements > len(list1):
        num_elements = len(list1)

    mapIndexPosition = list(zip(list1, list2))
    random.shuffle(mapIndexPosition)
    input_list1, input_list2 = zip(*mapIndexPosition[0:num_elements])
    
    output_list = list(input_list1 + input_list2)
    random.shuffle(output_list)

    return output_list

def create_layout(input_rand_list, ncol, nrow):
    layout_list = []

    for i in range(nrow):
        new_row = []
        for j in range(ncol):
            list_element_num = i*ncol + j
            if list_element_num > len(input_rand_list) -1:
                break
            new_row.append(sg.Button(input_rand_list[list_element_num], border_width=2, 
                            font=18, key = input_rand_list[list_element_num], 
                            button_color=('black', '#ffd22b') ))
        layout_list.append(new_row)
    return layout_list

def create_window(input_list, ncol, nrow):
    sg.theme('DarkAmber')    

    layout = create_layout(input_list, ncol, nrow)
    layout = layout + [[sg.Button('New Game', font = 24, button_color=('black', 'orange')), sg.Exit(font = 24, button_color=('black', 'red'))]]      

    window = sg.Window('Íslenski', layout)
    return window      

def check_victory(match_count, input_list_len):
    victory_layout = [[sg.Text('Sigur!', font = 36, justification='center')], [sg.Exit('OK!',  font = 24, button_color=('black', 'orange'))]]
    victory_window = sg.Window('Sigur!', victory_layout)

    if match_count == input_list_len:
        while True:         # The Event Loop
            event, values = victory_window.read()            
            if event in (None, 'OK!'):
                break      
    victory_window.close()

def run_game(window, input_list):
    word_pair = []
    match_count = 0
    input_list_len = len(input_list)

    while True:  # The Event Loop
        
        event, values = window.read()
        if event in input_list:
            window.FindElement(event).Update(button_color=('black', 'yellow'))
            word_pair.append(event)
            if len(word_pair) == 2:
                if check_word_pair(word_pair, window):
                    match_count += 2
                    check_victory(match_count, input_list_len)
                word_pair = []
                  
        if event in (None, 'Exit'):      
            break 
        if event in ('New Game'):
            window.close()
            main()     
    window.close()

def main():
    list1, list2 = parse_tab_delimited("input_dict.tsv")
    nrow = 4
    ncol = 4
    rand_list = get_random_list(int(nrow*ncol/2))

    window = create_window(rand_list, nrow, ncol)
    run_game(window, rand_list)

main()