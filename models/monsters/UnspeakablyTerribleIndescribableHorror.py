import MonsterBase


class UnspeakablyTerribleIndescribableHorror(MonsterBase):
    def __init__(self):
        super(UnspeakablyTerribleIndescribableHorror, self).__init__(14, 'Невыразимо жуткий неописуемый ужас', 'Невыразимо жуткая смерть для всех, кто проиграл ему, кроме Хафлингов.', 4, 1)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
