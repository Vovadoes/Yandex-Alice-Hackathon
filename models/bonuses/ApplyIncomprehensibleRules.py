import BonusBase


class ApplyIncomprehensibleRules(BonusBase):
    def __init__(self):
        super(ApplyIncomprehensibleRules, self).__init__(
            'Примени непонятные правила',
            'Примени непонятные правила',
            1000
        ) # получи уровень

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        pass
