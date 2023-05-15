import datetime


class Player:
    def __init__(self, name=None, score=0, robots=3, scan_titanium=False, scan_enemy=False, **kwargs):
        self.name = name
        self.score = score
        self.robots = robots
        self.scan_titanium = scan_titanium
        self.scan_enemy = scan_enemy

    @classmethod
    def from_slot(cls, slot):
        return cls(**slot.__dict__)

    def to_slot(self):
        return SavedPlayer(self)


class SavedPlayer(Player):
    def __init__(self, player):
        super().__init__(**player.__dict__)
        self.save_time = datetime.datetime.now().timestamp()

    def __str__(self):
        return (
            f"{self.name} Titanium: {self.score} Robots: {self.robots} "
            f"Last save: {datetime.datetime.fromtimestamp(self.save_time).strftime('%Y-%m-%d %H:%M')}"
            f"{' Upgrades:' if self.scan_titanium or self.scan_enemy else ''}"
            f"{' titanium_info' if self.scan_titanium else ''}"
            f"{' enemy_info' if self.scan_enemy else ''}"
        )

    @classmethod
    def from_json(cls, dct):
        if dct:
            slot = cls(Player(**dct))
            slot.save_time = dct['save_time']
            return slot
