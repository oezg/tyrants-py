import datetime
import typing


class Player:
    def __init__(self, name=None, score=0, robots=3, scan_titanium=False, scan_enemy=False, **kwargs) -> None:
        self.name: str = name
        self.score: int = score
        self.robots: int = robots
        self.scan_titanium: bool = scan_titanium
        self.scan_enemy: bool = scan_enemy

    @classmethod
    def load(cls, slot: "SavedPlayer") -> "Player":
        return cls(**slot.__dict__)

    def save(self) -> "SavedPlayer":
        return SavedPlayer(self)


class SavedPlayer(Player):
    def __init__(self, player: "Player") -> None:
        super().__init__(**player.__dict__)
        self.save_time: float = datetime.datetime.now().timestamp()

    def __str__(self) -> str:
        return (
            f"{self.name} Titanium: {self.score} Robots: {self.robots} "
            f"Last save: {datetime.datetime.fromtimestamp(self.save_time).strftime('%Y-%m-%d %H:%M')}"
            f"{' Upgrades:' if self.scan_titanium or self.scan_enemy else ''}"
            f"{' titanium_info' if self.scan_titanium else ''}"
            f"{' enemy_info' if self.scan_enemy else ''}"
        )

    @classmethod
    def from_json(cls, dct: dict[str, str | int | bool | float]) -> typing.Optional["SavedPlayer"]:
        if dct:
            player: "SavedPlayer" = cls(Player(**dct))
            player.save_time = dct['save_time']
            return player
