import BonusBase


class Electro-acid-radiationPotion(BonusBase):
    def __init__(self):
        super(Electro-acid-radiationPotion, self).__init__(
            'Электро-кислотно-радиационное зелье',
            'Играй в любой бой. +5 любой стороне. Разовая шмотка.',
            200
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        pass
    