import os
import os.path
import shutil
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Runs the python 3 client doc generation script.')
parser.add_argument('game', action='store', help='the name of the game you want to document. Must exist in ../games/')

args = parser.parse_args()

game_name = args.game[0].upper() + args.game[1:]
lower_game_name = game_name[0].lower() + game_name[1:]

def camelcase(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

game_path = "../games/" + lower_game_name
only_files = [f for f in os.listdir(game_path) if os.path.isfile(os.path.join(game_path, f))]
game_classes = []

game_rst_path = "./temp"
if os.path.isdir(game_rst_path):
    shutil.rmtree(game_rst_path)
os.makedirs(game_rst_path)

for name in only_files:
    name = os.path.splitext(name)[0]
    cc = camelcase(name)
    not_inherit = (name == "ai" or name == "game" or name == "game_object")

    if name == "__init__":
        continue
    elif name == "ai":
        cc = "AI"

    if not not_inherit and name != "player":
        game_classes.append(name)

    with open(game_rst_path + "/" + name + ".rst", "w+") as f:
        f.write("""
{0}
========

.. autoclass:: games.{1}.{0}
    :members:{2}

""".format(cc, lower_game_name, "" if not_inherit else """
    :inherited-members:
    :show-inheritance:"""))

with open("./index.rst", "w+") as f:
    f.truncate()
    f.write("""
Welcome to the {game_name} Python 3 Client documentation!
=========================================================

Your AI:

.. toctree::
   :maxdepth: 2

   temp/ai.rst

Game Classes:

.. toctree::
   :maxdepth: 2

   temp/game.rst
   temp/game_object.rst
   temp/player.rst
{game_classes}


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
""".format(
    game_name=game_name,
    lower_game_name=lower_game_name,
    game_classes="\n".join(
        "   temp/{}.rst".format(game_class) for game_class in sorted(game_classes)
    )
))

subprocess.call(["sphinx-build -b html ./ ./output"], shell=True)

# cleanup files we made
shutil.rmtree(game_rst_path)
os.remove("./index.rst")