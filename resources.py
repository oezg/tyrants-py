import string_utils

help_text = 'Placeholder to tell the player what the game is about and how to control the game.'

entry = """
+==============================================================================+
          ████████╗██╗░░░██╗██████╗░░█████╗░███╗░░██╗████████╗░██████╗
          ╚══██╔══╝╚██╗░██╔╝██╔══██╗██╔══██╗████╗░██║╚══██╔══╝██╔════╝
          ░░░██║░░░░╚████╔╝░██████╔╝███████║██╔██╗██║░░░██║░░░╚█████╗░
          ░░░██║░░░░░╚██╔╝░░██╔══██╗██╔══██║██║╚████║░░░██║░░░░╚═══██╗
          ░░░██║░░░░░░██║░░░██║░░██║██║░░██║██║░╚███║░░░██║░░░██████╔╝
          ░░░╚═╝░░░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚═════╝░
+==============================================================================+

[New]  Game
[Load] Game
[High] Scores
[Help]
[Exit]
"""


new_game_template = """
Welcome, commander {name}!
Are you ready to begin?
[Yes] [No] Return to Main[Menu]
"""


def new_game(name):
    return new_game_template.format(name=name)


hub_template = """
+==============================================================================+
{robots}
+==============================================================================+
| Titanium: {titanium:<12d}                                                       |
+==============================================================================+
|                  [Ex]plore                          [Up]grade                |
|                  [Save]                             [M]enu                   |
+==============================================================================+
"""


def hub(player):
    return hub_template.format(
        robots=string_utils.display_robots(player.robots),
        titanium=player.score
    )


menu = """
                          |==========================|
                          |            MENU          |
                          |                          |
                          | [Back] to game           |
                          | Return to [Main] Menu    |
                          | [Save] and exit          |
                          | [Exit] game              |
                          |==========================|
"""

robot = """
  $   $$$$$$$   $  
  $$$$$     $$$$$  
      $$$$$$$      
     $$$   $$$     
     $       $     
"""

upgrade_store = """
                       |================================|
                       |          UPGRADE STORE         |
                       |                         Price  |
                       | [1] Titanium Scan         250  |
                       | [2] Enemy Encounter Scan  500  |
                       | [3] New Robot            1000  |
                       |                                |
                       | [Back]                         |
                       |================================|
"""

deploy_template = """
Deploying robots{encounter}
{location} explored successfully, {damage}.
Acquired {titanium} lumps of titanium
"""


def deploy(encounter, target):
    return deploy_template.format(
        encounter='\nEnemy encounter' if encounter else '',
        location=target.location,
        damage='1 robot lost.' if encounter else 'with no damage taken',
        titanium=target.titanium
    ).strip()


game_saved = """
                        |==============================|
                        |    GAME SAVED SUCCESSFULLY   |
                        |==============================|
"""

game_loaded = """
                        |==============================|
                        |    GAME LOADED SUCCESSFULLY  |
                        |==============================|
"""

purchase_enemy = "Purchase successful. You will now see how likely you will encounter an enemy at each found location."

purchase_titanium = "Purchase successful. You can now see how much titanium you can get from each found location."

purchase_robot = "Purchase successful. You now have an additional robot"

time_format = "%Y-%m-%d %H:%M"

upgrade_prices = {'1': 250, '2': 500, '3': 1000}

game_over = """
Deploying robots...
Enemy encounter!!!
Mission aborted, the last robot lost...
                        |==============================|
                        |          GAME OVER!          |
                        |==============================|
"""

no_locations = """
Nothing more in sight.
       [Back]
"""
