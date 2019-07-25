import json

file = '../json/heroes.json'

heroes = json.load(open(file, 'r'))

her_inp_list = ['Io', 'Axe', 'Invoker', 'Lion', 'Phoenix']
lines_list = ['h', 'e', 'm', 'r', 'f']
lines_list_marked = ['h', 'h', 'e', 'e', 'm']
her_list_copy = her_inp_list.copy()



for ll in lines_list:
    line_tag = ''
    line_value = -1
    line_her = ''
    
    for h in her_list_copy:
        for l in lines_list_marked:
            val = heroes[h]['lines'][l]
            
            if val > line_value:
                line_her = h
                line_value = val
                line_tag = l
    
    lines_list_marked.remove(line_tag)
    her_list_copy.remove(line_her)
    
    print(line_her)
    print(line_value)
    print(line_tag)
    print(lines_list_marked)
    print('\n\n')