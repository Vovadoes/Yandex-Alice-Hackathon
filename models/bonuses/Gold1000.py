import BonusBase


class Gold1000(BonusBase):
    def __init__(self):
        super(Gold1000, self).__init__(
            '1000 Голдов',
            '1000 Голдов',
            1000
        ) # получи уровань

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        pass
