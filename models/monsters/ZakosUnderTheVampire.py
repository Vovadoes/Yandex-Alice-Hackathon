import MonsterBase


class ZakosUnderTheVampire(MonsterBase):
    def __init__(self):
        super(ZakosUnderTheVampire, self).__init__(12, 'Закос под вампира', 'Загородив выход, рассказывает о себе. Потеряй 3 уровня.', 3, 1)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
