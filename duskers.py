import argparse
import random
import sys

entry_string = """+=====================================================================+
     ████████╗██╗░░░██╗██████╗░░█████╗░███╗░░██╗████████╗░██████╗
     ╚══██╔══╝╚██╗░██╔╝██╔══██╗██╔══██╗████╗░██║╚══██╔══╝██╔════╝
     ░░░██║░░░░╚████╔╝░██████╔╝███████║██╔██╗██║░░░██║░░░╚█████╗░
     ░░░██║░░░░░╚██╔╝░░██╔══██╗██╔══██║██║╚████║░░░██║░░░░╚═══██╗
     ░░░██║░░░░░░██║░░░██║░░██║██║░░██║██║░╚███║░░░██║░░░██████╔╝
     ░░░╚═╝░░░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚═════╝░
+=====================================================================+

[New]  Game
[Load] Game
[High] Scores
[Help]
[Exit]
"""

hub_string = """+==============================================================================+
  $   $$$$$$$   $  |  $   $$$$$$$   $  |  $   $$$$$$$   $
  $$$$$     $$$$$  |  $$$$$     $$$$$  |  $$$$$     $$$$$
      $$$$$$$      |      $$$$$$$      |      $$$$$$$
     $$$   $$$     |     $$$   $$$     |     $$$   $$$
     $       $     |     $       $     |     $       $
+==============================================================================+
| Titanium: {}                                                                  |
+==============================================================================+
|                  [Ex]plore                          [Up]grade                |
|                  [Save]                             [M]enu                   |
+==============================================================================+"""

menu_string = """
                          |==========================|
                          |            MENU          |
                          |                          |
                          | [Back] to game           |
                          | Return to [Main] Menu    |
                          | [Save] and exit          |
                          | [Exit] game              |
                          |==========================|
"""

robot_string = """
  $   $$$$$$$   $  
  $$$$$     $$$$$  
      $$$$$$$      
     $$$   $$$     
     $       $     
"""

deploying_string = """Deploying robots
{0} explored successfully, with no damage taken.
Acquired {1} lumps of titanium"""


class Tyrants:
    def __init__(self, locations):
        self.locations: list[str] = locations
        self.titanium = 0

    def run(self):
        self.entry()

    def play(self):
        name = input("Enter your name:\n")
        print(f"Greetings, commander {name}!")
        while True:
            print("Are you ready to begin?")
            print("[Yes] [No] Return to Main[Menu]")
            command = self.get_command('yes', 'no', 'menu')
            match command:
                case 'yes':
                    self.hub()
                case 'no':
                    print('\nHow about now.')
                case 'menu':
                    self.entry()
                    break

    def menu(self):
        print(menu_string)
        menu_command = self.get_command('back', 'main', 'save', 'exit')
        match menu_command:
            case 'back':
                self.hub()
            case 'main':
                self.entry()
            case 'exit':
                exit_game()
            case 'save':
                not_implemented()

    def hub(self):
        print(hub_string.format(self.titanium))
        hub_command = self.get_command('ex', 'up', 'save', 'm')
        match hub_command:
            case 'm':
                self.menu()
            case 'ex':
                self.explore()
            case _:
                not_implemented()

    def explore(self):
        if not self.locations:
            print('Nothing more in sight.')
            print('       [Back]')
            self.get_command()

        data = {}
        idx = 1
        number_locations = random.randint(1, 9)
        finished = False

        while not finished:
            location = random.choice(self.locations)
            titanium = random.randint(10, 100)
            data[idx] = {
                'location': location,
                'titanium': titanium,
            }
            chosen_location = self.choose_location(data)
            if chosen_location == 's' and idx < number_locations:
                idx += 1
                continue

            while chosen_location == 's':
                print('Nothing more in sight.')
                print('       [Back]')
                chosen_location = self.get_command('s', *map(str, data.keys()))

            target = data[int(chosen_location)]
            print(deploying_string.format(
                target['location'],
                target['titanium'],
            ))
            self.titanium += target['titanium']
            # self.locations.remove(target['location'])
            finished = True
            self.hub()

    def high(self):
        print('No scores to display.')
        print('        [Back]')
        self.get_command(back_to_hub=False)

    def entry(self):
        print(entry_string)
        entry_command = self.get_command('play', 'high', 'help', 'exit')
        match entry_command:
            case 'exit':
                exit_game()
            case 'play':
                self.play()
            case 'high':
                self.high()
            case 'help':
                not_implemented()

    def choose_location(self, data):
        print("Searching")
        for key, value in data.items():
            print(f"[{key}] {value['location']}")
        print("\n[S] to continue searching")
        return self.get_command('s', *map(str, data.keys()))

    def get_command(self, *options, back_to_hub=True):
        while True:
            t = input("Your command: ").lower()
            if t == 'back':
                self.hub() if back_to_hub else self.entry()
            if t in options:
                return t
            print('Invalid input', end='')


def exit_game():
    print('Thanks for playing, bye!')
    sys.exit(0)


def not_implemented():
    print('Coming SOON! Thanks for playing!')
    sys.exit(0)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('seed')
    parser.add_argument('start')
    parser.add_argument('end')
    parser.add_argument('locations')
    return parser.parse_args()


def main():
    args = parse()
    random.seed(args.seed)
    locations = split_commas(args.locations)
    Tyrants(locations).run()


def split_commas(text):
    return text.replace('_', ' ').split(',')


if __name__ == '__main__':
    main()
