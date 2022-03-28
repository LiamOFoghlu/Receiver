from operator import mod
from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Task'
    players_per_group = None
    num_rounds = 1
    money = "£3.00"
    guess_money = "£1.00"
    total_balls = "three"
    no_task_balls = "two"

    # import proposer data
    import pandas as pd
    proposer_df = pd.read_csv("_static/proposer_df.csv")
    high_ineq_df = proposer_df.loc[proposer_df['offer'] == "10%"]
    high_ineq_df = high_ineq_df.reset_index(drop=True)
    low_ineq_df = proposer_df.loc[proposer_df['offer'] == "40%"]
    low_ineq_df = low_ineq_df.reset_index(drop=True)


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
        import random
        for player in subsession.get_players():

            # assign treeatment
            if (player.participant.treatment == "LN" or player.participant.treatment == "LC"):      # receiver in low inequality condition
                r = random.choice(list(range(len(Constants.low_ineq_df))))
                player.proposer_id = int(Constants.low_ineq_df.loc[r,"proposer_id"])
                player.proposer_merit = Constants.low_ineq_df.loc[r,"merit"]
                player.proposer_participant_code = Constants.low_ineq_df.loc[r,"proposer_participant_code"]
            elif (player.participant.treatment == "HN" or player.participant.treatment == "HC"):      # receiver in high inequality condition
                r = random.choice(list(range(len(Constants.high_ineq_df))))
                player.proposer_id = int(Constants.high_ineq_df.loc[r,"proposer_id"])    
                player.proposer_merit = Constants.high_ineq_df.loc[r,"merit"]   
                player.proposer_participant_code = Constants.high_ineq_df.loc[r,"proposer_participant_code"]



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    proposer_id = models.IntegerField()
    proposer_participant_code = models.StringField()
    proposer_merit = models.StringField()
    choice = models.StringField(
        label ="Do you accept or reject the offer?",
        choices = [
            "Accept",
            "Reject"
        ],
        widget = widgets.RadioSelectHorizontal)
    guess = models.StringField(
        label ="",
        widget = widgets.RadioSelectHorizontal)
    guess_rationale = models.LongStringField(label = "")
    fairness_rationale = models.LongStringField(label = "")
    fair_binary = models.StringField(
        label = "",
        widget = widgets.RadioSelectHorizontal)

def guess_choices(player):
    import random
    choices = [
            "They drew a Task ball, and earned the money.",
            "They drew a No-task ball, and were gifted the money."
        ]
    random.shuffle(choices)
    return choices

def fair_binary_choices(player):
    import random
    choices = [
            "Fair",
            "Unfair"
        ]
    random.shuffle(choices)
    return choices

# PAGES

class Offer_Information(Page):
    pass

class Condition(Page):  
    def vars_for_template(player):
        if (player.participant.treatment == "LC" or player.participant.treatment == "HC"):
            template = "Task/Choice.html" 
            condition = "Choice"
        else:
            template = "Task/No_choice.html"
            condition = "No-choice"
        return dict(
            template = template,
            condition = condition
        )

class Offer(Page):
    form_model = 'player'
    def get_form_fields(player):
        control_level = player.participant.treatment[1]
        if control_level == "C":
            return ['choice']

    def vars_for_template(player):
        inequality_level = player.participant.treatment[0]
        control_level = player.participant.treatment[1]
        if inequality_level == "H":         # high inequality
            offer_percent = "10%" 
        else:                               # low inequality
            offer_percent = "40%" 
        if control_level == "C":            # control
            template = "Task/Choice_Offer.html"
        else:                               # no control
            template = "Task/No_Choice_Offer.html"  
        offer_absolute = "£" + str(round((float(offer_percent[0:2])/100)*float(Constants.money[1:4]),2)) 
        if len(offer_absolute) < 5:
             offer_absolute = offer_absolute + "0"
        proposer_portion = "£" + str(float(Constants.money[1:5]) - float(offer_absolute[1:5]))
        if len(proposer_portion) < 5:
             proposer_portion = proposer_portion + "0"
        return dict(
            template = template,
            offer_percent = offer_percent,
            offer_absolute = offer_absolute,
            proposer_portion = proposer_portion,
            proposer_id = player.proposer_id
        )

class Guess(Page):
    form_model = 'player'
    form_fields = ['guess']

    def vars_for_template(player):
        inequality_level = player.participant.treatment[0]
        control_level = player.participant.treatment[1]
        if inequality_level == "H":         # high inequality
            offer_percent = "10%" 
        else:                               # low inequality
            offer_percent = "40%" 
        if control_level == "C":            # control
            choice_condition = "Choice"
            choice_explanation = "had the option to reject the offer"
        else:                               # no control
            choice_condition = "No-choice"  
            choice_explanation = "had to accept the offer"
        offer_absolute = "£" + str(round((float(offer_percent[0:2])/100)*float(Constants.money[1:4]),2)) 
        if len(offer_absolute) < 5:
             offer_absolute = offer_absolute + "0"
        proposer_portion = "£" + str(float(Constants.money[1:5]) - float(offer_absolute[1:5]))
        if len(proposer_portion) < 5:
             proposer_portion = proposer_portion + "0"
        return dict(
            offer_percent = offer_percent,
            offer_absolute = offer_absolute,
            proposer_portion = proposer_portion,
            proposer_id = player.proposer_id,
            choice_condition = choice_condition,
            choice_explanation = choice_explanation
        )

class Survey(Page):
    form_model = 'player'
    form_fields = ['guess_rationale','fairness_rationale', 'fair_binary']

    def vars_for_template(player):
        inequality_level = player.participant.treatment[0]
        if inequality_level == "H":         # high inequality
            offer_percent = "10%" 
        else:                               # low inequality
            offer_percent = "40%" 
        offer_absolute = "£" + str(round((float(offer_percent[0:2])/100)*float(Constants.money[1:4]),2)) 
        if len(offer_absolute) < 5:
             offer_absolute = offer_absolute + "0"
        proposer_portion = "£" + str(float(Constants.money[1:5]) - float(offer_absolute[1:5]))
        if len(proposer_portion) < 5:
             proposer_portion = proposer_portion + "0"
        if player.guess == "They drew a Task ball, and earned the money.":
            ball = "Task"
        else:
            ball = "No-task"
        return dict(
            ball = ball,
            offer_absolute = offer_absolute,
            proposer_portion = proposer_portion
        )

page_sequence = [Offer_Information, Condition, Offer, Guess, Survey]
