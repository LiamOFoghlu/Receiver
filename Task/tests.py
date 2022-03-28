from otree.api import *

from Task import Guess, Offer, Offer_Information, Condition, Post_Guess_Question

class PlayerBot(Bot):
    def play_round(self):
        import random
        control_level = self.player.participant.treatment[1]
        if control_level == "C":            # choice
            yield Offer_Information

            yield Condition

            prob = random.uniform(0,1)
            if prob < 0.25:
                yield Offer, dict(choice = "Reject")
            else:
                yield Offer, dict(choice = "Accept")

            prob = random.uniform(0,1)
            if prob < 0.33:
                yield Guess, dict(guess = "They drew a Task ball, and earned the money.")
            else:
                yield Guess, dict(guess = "They drew a No-task ball, and were gifted the money.")
            
            yield Post_Guess_Question, dict(guess_rationale = "I am a bot - no idea", fairness_rationale = "Why are you asking me? I'm a bot...")

        else:                   # no choice
            yield Offer_Information

            yield Condition

            yield Offer

            prob = random.uniform(0,1)
            if prob < 0.33:
                yield Guess, dict(guess = "They drew a Task ball, and earned the money.")
            else:
                yield Guess, dict(guess = "They drew a No-task ball, and were gifted the money.")
            
            yield Post_Guess_Question, dict(guess_rationale = "I am a bot - no idea", fairness_rationale = "Why are you asking me? I'm a bot...")