import MonsterBase


class PaganDemon(MonsterBase):
    def __init__(self):
        super(PaganDemon, self).__init__(12, 'Языческий демон', 'Отвратительный поцелуй лишает тебя двух (а если ты эльф - трех) уровней.', 3, 1)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
