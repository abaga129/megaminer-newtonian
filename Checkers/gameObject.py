# Generated by Creer, git hash c6767247662bdc8024518de1aebc87bcf634ca49
# This is a simple class to represent the GameObject object in the game. You can extend it by adding utility functions here in this file.

from baseGameObject import BaseGameObject


# @class GameObject: An object in the game. The most basic class that all game classes should inherit from automatically.
class GameObject(BaseGameObject):
    ## initializes a GameObject with basic logic as provided by the Creer code generator
    # @param <dict> data: initialization data
    def __init__(self, data):
        BaseGameObject.__init__(self, data)

        self.logs = (data['logs'] if 'logs' in data else [])
        self.id = str(data['id'] if 'id' in data else "")



    ## adds a message to this game object's log. Intended for debugging purposes.
    # @param <string> message: A string to add to this GameObject's log. Intended for debugging.
    def log(self, message):
        return self.client.send_command(self, 'log', message=message)
