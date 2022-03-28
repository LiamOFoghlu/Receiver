from otree.api import *

from Intro import Consent, Introduction, ProlificID

class PlayerBot(Bot):
    def play_round(self):
        yield Consent

        yield ProlificID, dict(ProlificID = "bot")

        yield Introduction