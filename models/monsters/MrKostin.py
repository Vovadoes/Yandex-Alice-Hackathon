import MonsterBase


class MrKostin(MonsterBase):
    def __init__(self):
        super(MrKostin, self).__init__(2, 'Г-н Костин', 'Его костлявые прикосновения снимают с тебя 2 уровня.', 1, 1)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
