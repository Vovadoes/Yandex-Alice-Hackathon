import MonsterBase


class Orcs3872(MonsterBase):
    def __init__(self):
        super(Orcs3872, self).__init__(10, '3872 орка', 'Брось кубик. На 2 и меньше ты затопан до смерти, иначе потеряй столько уровней, сколько выпало.', 3, 1)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
