import argparse
import json
import os
import random
import sys
import typing

import string_utils
import player_utils


def parse_arguments() -> list[str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('arguments', nargs='*')
    args = parser.parse_args().arguments
    if len(args) > 0:
        random.seed(args[0])
    if len(args) > 1:
        locations = string_utils.split_commas(args[-1])
    else:
        locations = ['One Utrecht', 'Two Zürich', 'Three Kazan', 'Four Lund', 'Five Tübingen', 'Six Denizli']
    return locations


def exit_game() -> None:
    print('Thanks for playing, bye!')
    sys.exit(0)


def get_saved_players() -> dict[str, typing.Optional[player_utils.SavedPlayer]]:
    saved_players: dict[str, typing.Optional[player_utils.SavedPlayer]] = {}.fromkeys('123')
    if os.path.isfile('save_file.json'):
        with open('save_file.json') as json_file:
            try:
                slots: dict[str, typing.Optional[dict[str, str | int | bool | float]]] = json.load(json_file)
            except json.decoder.JSONDecodeError:
                pass
            else:
                saved_players = {k: player_utils.SavedPlayer.from_json(v) for k, v in slots.items()}
    string_utils.print_slots(saved_players)
    return saved_players


def get_high_scores() -> list[player_utils.SavedPlayer]:
    high_scores: list[player_utils.SavedPlayer] = []
    if os.path.isfile('high_scores.json'):
        with open('high_scores.json') as json_file:
            try:
                high_scores = json.load(json_file, object_hook=player_utils.SavedPlayer.from_json)
            except json.decoder.JSONDecodeError:
                pass
    return high_scores


def save_high_scores(high_scores: list[player_utils.SavedPlayer]) -> None:
    with open('high_scores.json', 'w') as json_file:
        json.dump(high_scores, json_file, default=lambda score: score.__dict__, indent=4)


def update_high(candidate: player_utils.SavedPlayer) -> None:
    high_scores: list[player_utils.SavedPlayer] = get_high_scores()
    high_scores.append(candidate)
    high_scores.sort(key=lambda score: (-score.score, score.save_time))
    while len(high_scores) > 10:
        high_scores.pop()
    save_high_scores(high_scores)
