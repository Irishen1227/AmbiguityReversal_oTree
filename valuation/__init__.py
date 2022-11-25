from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'valuation'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 6
    risk_m = [[0,0.4,40],[0.6,1, 10],[0,0.4,20],[0.8,1,8], [0,1,24],[0.8,1,12]]


class Subsession(BaseSubsession):
    prob_win = models.FloatField()
    prob_win_min = models.FloatField()
    prob_win_max = models.FloatField()
    win_pay = models.FloatField()
    market_price = models.FloatField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payoff1 = models.FloatField()
    para_select = models.IntegerField()
    A_pay = models.FloatField()
    valuation = models.FloatField()

         

# FUNCTIONS
def creating_session(subsession):
        if subsession.round_number == 1:
            subsession.session.vars['seq_noinfo'] = random.sample(range(C.NUM_ROUNDS),C.NUM_ROUNDS)
            
        parameter_select = subsession.session.vars['seq_noinfo'][subsession.round_number - 1]
        
        subsession.prob_win_min = C.risk_m[parameter_select][0]
        subsession.prob_win_max = C.risk_m[parameter_select][1]
        subsession.win_pay = C.risk_m[parameter_select][2]

        subsession.prob_win = random.uniform(subsession.prob_win_min,subsession.prob_win_max)
        subsession.market_price = random.uniform(0, subsession.win_pay * subsession.prob_win_max)

        
        for player in subsession.get_players():
            #player.participation.vars['valuation_paying_round'] = []
            #player.participation.vars['valuation_pay_select'] = []
            player.A_pay = random.choices([0,subsession.win_pay],[1-subsession.prob_win, subsession.prob_win])[0]
            player.para_select = parameter_select + 1
            if subsession.round_number == 1:
                temp = random.sample(range(1, C.NUM_ROUNDS + 1), 1)
                temp.sort()
                player.participant.vars['valuation_paying_round'] = temp
                player.participant.vars['valuation_paying_round_noinfo'] = temp
                


#def set_payoffs(player):
        #if player.valuation > player.subsession.market_price:
            #player.payoff1 = player.A_pay
        #else:
            #player.payoff1 = player.subsession.market_price
        
        #if player.round_number == player.participant.vars['valuation_paying_round_noinfo']:
            #player.participant.vars['valuation_pay_select']= player.payoff1
            #print(player.participant.vars['valuation_pay_select'])

# PAGES
class Opening(Page):
    def is_displayed(player):
        return player.round_number == 1
class Intro(Page):
    def is_displayed(player):
        return player.round_number == 1

class Valuation(Page):
    form_model = 'player'
    form_fields = ['valuation']

    def before_next_page(player,timeout_happened): 
        if player.valuation > player.subsession.market_price:
            player.payoff1 = player.A_pay
        else:
            player.payoff1 = player.subsession.market_price
        
        if player.round_number in player.participant.vars['valuation_paying_round_noinfo']:
            player.participant.vars['valuation_pay_select']= player.payoff1
             
            
       

class Result(Page):
    pass
 
page_sequence = [Opening, Intro, Valuation, Result]