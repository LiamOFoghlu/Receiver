from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'debrief'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    comment = models.LongStringField()      
    stop_epochtime = models.IntegerField()
    stop_clocktime = models.StringField()
    total_time_to_completion = models.IntegerField()


# PAGES
class end(Page):
    form_model = Player
    form_fields = ['comment']

    def is_displayed(player):
        # record time player finished application
        import time 
        time_out = round(time.time())
        player.stop_epochtime = time_out
        player.total_time_to_completion = time_out - player.participant.start_epochtime
        player.stop_clocktime = time.strftime('%H:%M:%S', time.localtime(time_out))
        return True


class comment_submitted(Page):
    def is_displayed(player):
        # record time player finished application - updates the time details if they submit comment
        import time 
        time_out = round(time.time())
        player.stop_epochtime = time_out
        player.total_time_to_completion = time_out - player.participant.start_epochtime
        player.stop_clocktime = time.strftime('%H:%M:%S', time.localtime(time_out))
        return 1

page_sequence = [end, comment_submitted]
