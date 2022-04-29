import BonusBase


class Wall-instant(BonusBase):
    def __init__(self):
        super(Wall-instant, self).__init__(
            'Стенка-мгновенка',
            'Все манчкины могут автоматически смыться из любого боя и получить сокровищя.',
            300
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        pass
    