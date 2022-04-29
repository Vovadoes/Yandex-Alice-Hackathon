import MonsterBase


class PaleBrothers(MonsterBase):
    def __init__(self):
        super(PaleBrothers, self).__init__(16, 'Бледные братья', 'Вернись на 1-ый уровень.', 4, 2)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
