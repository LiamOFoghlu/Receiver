from otree.api import *

from settings import SESSION_CONFIGS


doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'Intro'
    players_per_group = None
    num_rounds = 1
    max_payoff = "£2.20"
    money = "£3.00"
    total_balls = "five"
    no_task_balls = "three"

    # create a vector to randomise treatment
    num_participants = 350          # note this should be substantially larger than the number of participants I actually intend to hire, because some Prolificers will join the session but not complete
    num_blocks = -1*( -num_participants // 14) # I'm gonna create blocks within which the treatment is exactly balanced (2 in LC, 2 in LN, 5 in HC, 5 in HN). Then add the blocks together to get to the desired number of participants.
    import random

    treatment_block = list(range(1,15)) 
    treatment_assignment = [] 
    for i in range(num_blocks):
        treatment_assignment = treatment_assignment + treatment_block

    random.shuffle(treatment_assignment)
    for i in range(len(treatment_assignment)):
            if treatment_assignment[i] <= 2:
                treatment_assignment[i] = "LC"
            elif treatment_assignment[i] > 2 and treatment_assignment[i] <= 4:
                treatment_assignment[i] = "LN"
            elif treatment_assignment[i] > 4 and treatment_assignment[i] <= 9:
                treatment_assignment[i] = "HC"
            elif treatment_assignment[i] >9:
                treatment_assignment[i] = "HN"


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
        import itertools, random 

        treatment_assignment = itertools.cycle(Constants.treatment_assignment)
        for player in subsession.get_players():

            # determine treatment
            player.participant.treatment = next(treatment_assignment)
            player.treatment = player.participant.treatment

            # practice maths questions - randomly select two to show in instructions
            practice_maths_qs_index = list(range(4))
            random.shuffle(practice_maths_qs_index)
            player.participant.mathspractice_q1 = practice_maths_qs_index[0]
            player.participant.mathspractice_q2 = practice_maths_qs_index[1] 


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ProlificID = models.StringField()
    treatment = models.StringField()
    start_epochtime = models.IntegerField()
    start_clocktime = models.StringField()

    # maths practice questions
    q1 = models.StringField(
        label = "A shop has an offer: buy 8 kiwis, and every extra kiwi after that is half price. A man goes to the shop and pays £4.50 for some kiwis. The full price of a kiwi is £0.50. How many does he buy?",
        choices = [
            "9",
            "12",
            "10",
            "15"
        ],
        widget = widgets.RadioSelectHorizontal,
        blank=True) 
    q2 = models.StringField(
        label = "A hairdresser has an offer: every third visit is free. They charge £48 for a haircut. Last year Sarah paid £144 for a haaircut. How many times did she go?",
        choices = [
            "Two times",
            "Three times",
            "Four times",
            "Five times"
        ],
        widget = widgets.RadioSelectHorizontal,
        blank=True)     
    q3 = models.StringField(
        label = "A woman walks from the bottom to the top of a hill. She starts at 9.40am and arrives at the top at 10.20 am. She takes a rest for ten minutes. Then she walks back down. On the way down she walks twice as fast as she did on the way up. What time is it when she reaches the bottom of the hill?",
        choices = [
            "11.20",
            "10.40",
            "10.50",
            "11.10"
        ],
        widget = widgets.RadioSelectHorizontal,
        blank=True)   
    q4 = models.StringField(
        label = "A trader buys a painting for £120 and sells it for £170. They pay a £10 transaction fee. Their profit expressed as a percentage of total cost is:",
        choices = [
            "50%",
            "60%",
            "80%",
            "33%"
        ],
        widget = widgets.RadioSelectHorizontal,
        blank=True)     


# PAGES
class Consent(Page):
    def is_displayed(player):
        # record time player entered application
        import time 
        time_in = round(time.time())
        player.start_epochtime = time_in
        player.participant.start_epochtime = time_in
        player.start_clocktime = time.strftime('%H:%M:%S', time.localtime(time_in))
        return 1

class ProlificID(Page):
    form_model = 'player'
    form_fields = ['ProlificID']


class Introduction(Page):
    form_model = 'player'

    def get_form_fields(player: Player):
            questions = ['q1','q2','q3','q4']
            form_fields = [                                  
                        questions[player.participant.mathspractice_q1]
                        ]
            return form_fields


page_sequence = [Consent, ProlificID, Introduction]