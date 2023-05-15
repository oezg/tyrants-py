import player_utils
import random
import resources
import string_utils
import file_utils
import json


class Game:
    def __init__(self):
        self.locations: list[str] = file_utils.parse_arguments()
        self.player = None
        self.entry()

    def load(self):
        saved_slots = file_utils.get_saved_slots()
        load_command = string_utils.get_command(*saved_slots.keys())
        while load_command != 'back' and saved_slots[load_command] is None:
            self.player = player_utils.Player()
            self.hub()
            # load_command = string_utils.get_command(*saved_slots.keys())
        if load_command == 'back':
            self.entry()
        self.player = player_utils.Player.from_slot(saved_slots[load_command])
        print(resources.game_loaded)
        print(f'Welcome back, commander {self.player.name}!')
        self.hub()

    def save(self):
        saved_slots = file_utils.get_saved_slots()
        save_command = string_utils.get_command(*saved_slots.keys())
        if save_command == 'back':
            self.entry()
        saved_slots[save_command] = self.player.to_slot()
        with open('save_file.json', 'w') as json_file:
            json.dump(saved_slots, json_file, default=lambda slot: slot.__dict__, indent=4)
        print(resources.game_saved)

    def play(self):
        self.player = player_utils.Player(name=input("Enter your name: "))
        print(resources.new_game(self.player.name))
        while (command := string_utils.get_command('yes', 'no', 'menu')) == 'no':
            print('How about now.')
        match command:
            case 'yes':
                self.hub()
            case 'menu' | 'back':
                self.entry()

    def menu(self):
        print(resources.menu)
        menu_command = string_utils.get_command('back', 'main', 'save', 'exit')
        match menu_command:
            case 'back':
                self.hub()
            case 'main':
                self.entry()
            case 'exit':
                file_utils.exit_game()
            case 'save':
                self.save()
                file_utils.exit_game()

    def hub(self):
        print(resources.hub(self.player))
        hub_command = string_utils.get_command('ex', 'up', 'save', 'm')
        match hub_command:
            case 'm':
                self.menu()
            case 'ex':
                self.explore()
            case 'save':
                self.save()
                self.hub()
            case 'up':
                self.upgrade()
            case 'back':
                self.hub()

    def explore(self):
        class Target:
            def __init__(self, idx, location):
                self.idx = str(idx)
                self.location = location
                self.titanium = random.randint(10, 100)
                self.encounter = random.random()

        if not self.locations:
            print(resources.no_locations.strip())
            string_utils.get_command()
            self.hub()

        targets = []
        idx = 1
        number_locations = random.randint(1, 9)
        searching = True

        while searching:
            location = random.choice(self.locations)
            targets.append(Target(idx, location))
            chosen_location = string_utils.choose_location(targets, self.player)
            if chosen_location == 's' and idx < number_locations:
                idx += 1
                continue
            searching = False

            while chosen_location == 's':
                print(resources.no_locations.strip())
                chosen_location = string_utils.get_command('s', *(target.idx for target in targets))
            if chosen_location != 'back':
                target = next(filter(lambda target: target.idx == chosen_location, targets))
                if target.encounter < random.random():
                    self.get_titanium(target)
                elif self.player.robots == 1:
                    self.game_over()
                else:
                    self.get_titanium(target, True)
                    self.player.robots -= 1
            self.hub()

    def game_over(self):
        print(resources.game_over.strip())
        file_utils.update_high(self.player.to_slot())
        self.player = None
        self.entry()

    def get_titanium(self, target, encounter=False):
        self.player.score += target.titanium
        print(resources.deploy(encounter, target))

    def high(self):
        string_utils.display_high_scores()
        string_utils.get_command()
        self.entry()

    def entry(self):
        print(resources.entry)
        entry_command = string_utils.get_command('new', 'load', 'high', 'help', 'exit')
        match entry_command:
            case 'exit':
                file_utils.exit_game()
            case 'new':
                self.play()
            case 'load':
                self.load()
            case 'high':
                self.high()
            case 'help':
                self.help()
            case 'back':
                self.entry()

    def upgrade(self):
        print(resources.upgrade_store)
        self.upgrade_loop()

    def upgrade_loop(self):
        upgrade_command = string_utils.get_command('1', '2', '3')
        if upgrade_command == 'back':
            self.hub()
        else:
            if self.player.score < resources.upgrade_prices[upgrade_command]:
                print('Not enough titanium!')
                self.upgrade_loop()
            else:
                self.player.score -= resources.upgrade_prices[upgrade_command]
                match upgrade_command:
                    case '1':
                        self.player.scan_titanium = True
                        print(resources.purchase_titanium)
                    case '2':
                        self.player.scan_enemy = True
                        print(resources.purchase_enemy)
                    case '3':
                        self.player.robots += 1
                        print(resources.purchase_robot)
                self.hub()

    def help(self):
        print(resources.help_text)
        self.entry()


if __name__ == '__main__':
    Game()
