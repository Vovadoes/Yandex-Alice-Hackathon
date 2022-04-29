import MonsterBase


class PlutoniumDragon(MonsterBase):
    def __init__(self):
        super(PlutoniumDragon, self).__init__(20, 'Плутониевый дракон', 'Ты зажарен и съеден. Это верная смерть.', 5, 2)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
