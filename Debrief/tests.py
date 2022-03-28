from otree.api import *

from Debrief import comment_submitted, end

class PlayerBot(Bot):
    def play_round(self):
        yield end, dict(comment = "great job!")