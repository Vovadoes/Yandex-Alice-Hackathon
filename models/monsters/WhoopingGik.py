import MonsterBase


class WhoopingGik(MonsterBase):
    def __init__(self):
        super(WhoopingGik, self).__init__(6, 'Гикающий Гик', 'Стань нормальным. Потеряй расу', 2, 1)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
