import MonsterBase


class PitBull(MonsterBase):
    def __init__(self):
        super(PitBull, self).__init__(2, 'Питбуль', 'В зад укушенный герой - позорище. Потеряй 2 уровня.', 1, 1)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
