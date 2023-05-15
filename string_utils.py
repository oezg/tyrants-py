import file_utils


def display_robots(n):
    import resources
    return '\n'.join(
        ' | '.join([line] * n)
        for line in filter(None, resources.robot.splitlines())
    )


def display_high_scores():
    high_scores = file_utils.get_high_scores()
    if high_scores:
        print('\n	HIGH SCORES\n')
        [print(f"({i+1}) {score.name} {score.score}") for i, score in enumerate(high_scores)]
        print()
    else:
        print('No scores to display.')
    print('        [Back]')
    print()


def choose_location(targets, player):
    print("Searching")
    for target in targets:
        target_line = (
            f"[{target.idx}] {target.location}"
            f"{f' Titanium: {target.titanium}' if player.scan_titanium else ''}"
            f"{f' Encounter rate: {round(target.encounter * 100)}%' if player.scan_enemy else ''}"
        )
        print(target_line)
    print("\n[S] to continue searching")
    return get_command('s', *(target.idx for target in targets))


def get_command(*options):
    while True:
        t = input("Your command: ").lower()
        if t in options or t == 'back':
            return t
        print('Invalid input')


def print_slots(saved_slots):
    print('   Select save slot:')
    for key, slot in saved_slots.items():
        print(f"    [{key}] {slot if slot else 'empty'}")


def split_commas(text):
    return text.replace('_', ' ').split(',')

