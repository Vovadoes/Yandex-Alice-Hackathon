import BonusBase


class BoilTheAnthill(BonusBase):
    def __init__(self):
        super(BoilTheAnthill, self).__init__(
            'Вскипяти муравейник',
            'Вскипяти муравейник',
            1000
        ) # получи уровень

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        pass
