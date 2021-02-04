import random
import string
import json

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

def pass_generator(num_pass, length):
    pass_dict = {}
    for i in range(num_pass):
        pass_to = str(input('Please input what password for '))
        the_pass = ''.join(random.choice(chars) for i in range(length))
        pass_dict[pass_to] = the_pass
    with open('pass_list.txt', 'w') as file:
        file.write(json.dumps(pass_dict))

pass_generator(2, 20)