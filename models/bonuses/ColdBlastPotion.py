import BonusBase


class ColdBlastPotion(BonusBase):
    def __init__(self):
        super(ColdBlastPotion, self).__init__(
            'Зелье холодного взрыва',
            'Играй в любой бой. +3 любой стороне. Разовая шмотка.',
            100
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        pass
    