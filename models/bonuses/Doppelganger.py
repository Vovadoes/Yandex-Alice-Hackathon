import BonusBase


class Doppelganger(BonusBase):
    def __init__(self):
        super(Doppelganger, self).__init__(
            'Доппельгангер',
            'Играй в свой бой. Призывает двойника:твоя боевая сила удваивается. Разовая шмотка.',
            300
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        pass
    