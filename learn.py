def say_hi(name):
    if name == '':
        print("You didn't enter your name!")
    else:
        print('Hello, ' + name + '!')

while True:
    name = input('Enter your name: ')
    say_hi(name)
