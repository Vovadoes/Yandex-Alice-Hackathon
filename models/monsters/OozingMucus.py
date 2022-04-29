import MonsterBase


class OozingMucus(MonsterBase):
    def __init__(self):
        super(OozingMucus, self).__init__(1, 'Сочащаяся слизь', 'Потеряй надетую обувку. Если нет обуви, потеряй уровень.', 1, 1)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
