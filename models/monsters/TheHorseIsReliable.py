import MonsterBase


class TheHorseIsReliable(MonsterBase):
    def __init__(self):
        super(TheHorseIsReliable, self).__init__(4, 'Конь адедный', 'Лягает, кусает и жутко воняет. Потеряй 2 уровня.', 2, 1)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
