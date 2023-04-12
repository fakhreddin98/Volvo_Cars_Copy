import colorama
from colorama import Fore, Style

# initialize colorama
colorama.init()

# print text in different colors
print(Fore.RED + 'This text is red')
print(Fore.GREEN + 'This text is green')
print(Fore.BLUE + 'This text is blue')

# reset the color to default
print(Style.RESET_ALL + 'This text is back to the default color')
