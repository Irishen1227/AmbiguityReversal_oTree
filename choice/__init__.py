from http.client import PAYMENT_REQUIRED
from otree.api import *

import random

class C(BaseConstants):
    NAME_IN_URL = 'choice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3
    risk_m = [[0,0.4,40,0.6,1, 10],[0,0.4,20,0.8,1,8], [0,1,24,0.8,1,12]]

class Subsession(BaseSubsession):
    prob_win_d = models.FloatField()
    prob_win_p = models.FloatField()
    pay_d = models.FloatField()
    pay_p = models.FloatField()
    prob_win_d_max = models.FloatField()
    prob_win_d_min = models.FloatField()
    prob_win_p_max = models.FloatField()
    prob_win_p_min = models.FloatField()

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payoff1 = models.FloatField()
    para_select = models.IntegerField()
    A_pay = models.FloatField()
    B_pay = models.FloatField()

    choice = models.StringField(
        choices = [
            ['dollar bet', 'A'],
            ['prob bet', 'B']
        ],
        widget=widgets.RadioSelectHorizontal
    )

    
        
#FUNCTIONS
def creating_session(subsession):
        if subsession.round_number == 1:
            subsession.session.vars['seq_noinfo'] = random.sample(range(C.NUM_ROUNDS),C.NUM_ROUNDS)
            
        parameter_select = subsession.session.vars['seq_noinfo'][subsession.round_number - 1]
        
        subsession.prob_win_d_min = C.risk_m[parameter_select][0]
        subsession.prob_win_d_max = C.risk_m[parameter_select][1]
        subsession.pay_d = C.risk_m[parameter_select][2]

        subsession.prob_win_p_min = C.risk_m[parameter_select][3]
        subsession.prob_win_p_max = C.risk_m[parameter_select][4]
        subsession.pay_p = C.risk_m[parameter_select][5]

        subsession.prob_win_d = random.uniform(subsession.prob_win_d_min, subsession.prob_win_d_max)
        subsession.prob_win_p = random.uniform(subsession.prob_win_p_min, subsession.prob_win_p_max)
        for player in subsession.get_players():
            player.A_pay = random.choices([0,subsession.pay_d],[1-subsession.prob_win_d, subsession.prob_win_d])[0]
            player.B_pay = random.choices([0,subsession.pay_p],[1-subsession.prob_win_p, subsession.prob_win_p])[0]
            player.para_select = parameter_select + 1
            if subsession.round_number == 1:
                temp = random.sample(range(1, C.NUM_ROUNDS + 1), 1)
                temp.sort()
                player.participant.vars['choice_paying_round'] = temp
                player.participant.vars['choice_paying_round_noinfo'] = temp

                

#def set_payoffs(player):
        #if player.choice == 'dollar bet':
            #player.payoff1 = player.A_pay
        #else:
            #player.payoff1 = player.B_pay
        
        #if player.round_number == player.participant.vars['choice_paying_round_noinfo']:
         #   player.participant.vars['choice_pay_select']= player.payoff1
          #  print(player.participant.vars['choice_pay_select'])

# PAGES
class Intro(Page):
    def is_displayed(player):
        return player.round_number == 1

class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']


    def before_next_page(player,timeout_happened):   
        if player.choice == 'dollar bet':
            player.payoff1 = player.A_pay
        else:
            player.payoff1 = player.B_pay
        
        if player.round_number in player.participant.vars['choice_paying_round_noinfo']:
            player.participant.vars['choice_pay_select'] = player.payoff1
               
       

class Result(Page):
    pass
 
page_sequence = [Intro, Choice, Result]