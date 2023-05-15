import json
import random
import typing

import player_utils
import resources
import string_utils
import file_utils


class Game:
    def __init__(self) -> None:
        self.locations: list[str] = file_utils.parse_arguments()
        self.player: typing.Optional[player_utils.Player] = None
        self.entry()

    def load(self) -> None:
        saved_players, load_command = self.get_saved_players()
        if saved_players[load_command] is not None:
            self.player = player_utils.Player.load(saved_players[load_command])
            print(resources.game_loaded)
            print(f'Welcome back, commander {self.player.name}!')
        self.hub()

    def save(self) -> None:
        saved_players, save_command = self.get_saved_players()
        saved_players[save_command] = self.player.save()
        with open('save_file.json', 'w') as json_file:
            json.dump(saved_players, json_file, default=lambda slot: slot.__dict__, indent=4)
        print(resources.game_saved)

    def get_saved_players(self) -> tuple[dict[str, typing.Optional[player_utils.SavedPlayer]], str]:
        saved_players: dict[str, typing.Optional[player_utils.SavedPlayer]] = file_utils.get_saved_players()
        save_command: str = string_utils.get_command(*saved_players.keys())
        if save_command == 'back':
            self.entry()
        else:
            return saved_players, save_command

    def play(self) -> None:
        self.player = player_utils.Player(name=input("Enter your name: "))
        print(resources.new_game(self.player.name))
        while (command := string_utils.get_command('yes', 'no', 'menu')) == 'no':
            print('How about now.')
        match command:
            case 'yes':
                self.hub()
            case 'menu' | 'back':
                self.entry()

    def menu(self) -> None:
        print(resources.menu)
        menu_command: str = string_utils.get_command('back', 'main', 'save', 'exit')
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

    def hub(self) -> None:
        print(resources.hub(self.player))
        hub_command: str = string_utils.get_command('ex', 'up', 'save', 'm')
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

    def explore(self) -> None:
        class Target:
            def __init__(self, target_index, target_location) -> None:
                self.idx: str = str(target_index)
                self.location: str = target_location
                self.titanium: int = random.randint(10, 100)
                self.encounter: float = random.random()

        if not self.locations:
            print(resources.no_locations.strip())
            string_utils.get_command()
            self.hub()

        targets: list[Target] = []
        idx: int = 1
        number_locations: int = random.randint(1, 9)
        searching: bool = True

        while searching:
            location: str = random.choice(self.locations)
            targets.append(Target(idx, location))
            chosen_location: str = string_utils.choose_location(targets, self.player)
            if chosen_location == 's' and idx < number_locations:
                idx += 1
                continue
            searching = False

            while chosen_location == 's':
                print(resources.no_locations.strip())
                chosen_location = string_utils.get_command('s', *(target.idx for target in targets))
            if chosen_location != 'back':
                target: Target = next(filter(lambda target: target.idx == chosen_location, targets))
                if target.encounter < random.random():
                    self.get_titanium(target)
                elif self.player.robots == 1:
                    self.game_over()
                else:
                    self.get_titanium(target, True)
                    self.player.robots -= 1
            self.hub()

    def game_over(self) -> None:
        print(resources.game_over.strip())
        file_utils.update_high(self.player.save())
        self.player = None
        self.entry()

    def get_titanium(self, target: "Target", encounter: bool = False) -> None:
        self.player.score += target.titanium
        print(resources.deploy(encounter, target))

    def high(self) -> None:
        string_utils.display_high_scores()
        string_utils.get_command()
        self.entry()

    def entry(self) -> None:
        print(resources.entry)
        entry_command: str = string_utils.get_command('new', 'load', 'high', 'help', 'exit')
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

    def upgrade(self) -> None:
        print(resources.upgrade_store)
        self.upgrade_loop()

    def upgrade_loop(self) -> None:
        upgrade_command: str = string_utils.get_command('1', '2', '3')
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

    def help(self) -> None:
        print(resources.help_text)
        self.entry()


if __name__ == '__main__':
    Game()
