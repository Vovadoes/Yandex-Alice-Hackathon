import BonusBase


class InvisibilityPotion(BonusBase):
    def __init__(self):
        super(InvisibilityPotion, self).__init__(
            'Зелье невидимости',
            'Играй, когда ты провалил смывку, чтобы автоматически смыться от одного монстра и получить сокровищя',
            200
        )

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        pass
    