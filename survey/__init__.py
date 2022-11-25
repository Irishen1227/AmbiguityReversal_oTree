from otree.api import *

import math

class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    total_pay = models.FloatField()

    
    year = models.StringField(
        choices=[
            ['Freshman', 'Freshman'],
            ['Sophomore', 'Sophomore'],
            ['Junior', 'Junior'],
            ['Senior', 'Senior'],
            ['Graduate Student', 'Graduate Student']
        ],
        widget=widgets.RadioSelect,
        label="What's your year based on Spring 2022?"
    )
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'],['Other', 'Other']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    area = models.StringField(
        choices=[
            ['Urban', 'Urban'],
            ['Rural', 'Rural']
        ],
        widget=widgets.RadioSelect,
        label="Does your family live in urban or rural areas?"
    )
        
    

    major = models.StringField(
        choices=[
            ['Arts-Related Majors', 'Arts-Related Majors'],
            ['Economics and Business-Related Majors', 'Economics and Business-Related Majors'],
            ['Engineering and Technology-Related Majors', 'Engineering and Technology-Related Majors'],
            ['Literature, Language, and Social Science', 'Literature, Language, and Social Science'],
            ['Science and Math-Related Majors', 'Science and Math-Related Majors'],
            ['Others', 'Others']
        ],
        widget=widgets.RadioSelect,
        label="What is your major?"
    )

    income = models.StringField(
        choices=[
            ['Less than 100,000', 'Less than 100,000'],
            ['100,000 - 300,000', '100,000 - 300,000'],
            ['300,000 - 500,000', '300,000 - 500,000'],
            ['500,000 - 1,000,000', '500,000 - 1,000,000'],
            ['More than 1,000,000', 'More than 1,000,000']
        ],
        widget=widgets.RadioSelect,
        label="What is your annual household income?"
    )

    disposable = models.StringField(
        choices=[
            ['Less than 1,000', 'Less than 1,000'],
            ['1,000 - 3,000', '1,000 - 3,000'],
            ['3,000 - 5,000', '3,000 - 5,000'],
            ['More than 5,000', 'More than 5,000']
        ],
        widget=widgets.RadioSelect,
        label="What is your monthly disposable money?"
    )

    income_not_cover = models.BooleanField(
        choices=[
            [False, 'No'],
            [True, 'Yes']
        ],
        widget=widgets.RadioSelect,
        label="Sometimes people find that their income does not quite cover their living costs. In the last 12 months, has this happened to you or your family?"
    )

    invest_or_not = models.BooleanField(
        choices=[
            [False, 'No'],
            [True, 'Yes']
        ],
        widget=widgets.RadioSelect,
        label='Does your family make any investment?'
    )

    proportion = models.StringField(
        label = 'What is the proportion of investment income in your family?'
    )

    Stock = models.BooleanField(blank = True)
    Real_Estate = models.BooleanField(blank = True)
    Bond = models.BooleanField(blank = True)
    Fund = models.BooleanField(blank = True)
    Other = models.BooleanField(blank = True)


# FUNCTIONS

# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['year', 'gender', 'area', 'major']


class Finance(Page):
    form_model = 'player'
    form_fields = ['income', 'disposable', 'income_not_cover','invest_or_not','proportion']

class Method(Page):
    form_model = 'player'
    form_fields = ['Stock', 'Real_Estate', 'Bond','Fund','Other']

class FinishPage(Page):
    @staticmethod
    def vars_for_template(player):
        pay0 = player.participant.vars['choice_pay_select'] + player.participant.vars['valuation_pay_select'] + 25
        player.total_pay = math.ceil(pay0)
        player.payoff = Currency(player.total_pay)
        valuation_round = sum(player.participant.vars['valuation_paying_round'])
        choice_round = sum(player.participant.vars['choice_paying_round'])
        return dict(
            final_payoff = player.payoff,
            valuation_round = valuation_round,
            choice_round = choice_round
        )

page_sequence = [Demographics, Finance, Method, FinishPage]
