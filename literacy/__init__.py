from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'literacy'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    key = [2,1,1,3]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    correct = models.IntegerField()

    q1 = models.IntegerField(
        choices=[
            [1, 'Demand'],
            [2, 'Interest'],
            [3, 'Credit'],
            [4, 'Depreciation']
        ],
        widget=widgets.RadioSelect,
        label="(1) What is the price of money that is saved or borrowed?"
    )

    q2 = models.IntegerField(
        choices=[
            [1, 'The growth in the value of an investment'],
            [2, 'The risk associated with an investment'],
            [3, 'The process of returning the stock to the corporation that issued it'],
            [4, 'The fee you need to pay for owning different financial products']
        ],
        widget=widgets.RadioSelect,
        label="(2) The return may be thought of as"
    )

    q3 = models.IntegerField(
        choices=[
            [1, 'Reduce risk'],
            [2, 'Increase return'],
            [3, 'Reduce tax liability']
        ],
        widget=widgets.RadioSelect,
        label="(3) The benefit of owning investments that are diversified is that it:"
    )

    q4 = models.IntegerField(
        choices=[
            [1, '100'],
            [2, '90.91'],
            [3, '0']
        ],
        widget=widgets.RadioSelect,
        label = '(4) Suppose you decide to invest $1,000 in a bond today (Year 0). You expect to get $100 coupon and the principal next year (Year 1). The discount rate is 10%. What is the NPV today?'
    )

    def set_payoffs(self):
        answer = [self.q1, self.q2, self.q3, self.q4]

        self.correct = 0
        for n in range(4):
            if answer[n] == C.key[n]:
                self.correct += 1
# PAGES
class Intro(Page):
    pass


class Literacy(Page):
    form_model = 'player'
    form_fields = ['q1','q2','q3','q4']
    
    def before_next_page(player,timeout_happened):  
        player.set_payoffs()

class Result(Page):
    pass
page_sequence = [Intro, Literacy, Result]
