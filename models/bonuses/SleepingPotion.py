import BonusBase


class SleepingPotion(BonusBase):
    def __init__(self):
        super(SleepingPotion, self).__init__(
            'Спячечное зелье',
            'Играй в любой бой. +2 любой стороне. Разовая шмотка.',
            100
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        pass
    