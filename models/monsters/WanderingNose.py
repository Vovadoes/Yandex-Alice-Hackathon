import MonsterBase


class WanderingNose(MonsterBase):
    def __init__(self):
        super(WanderingNose, self).__init__(10, 'Блуждающий нос', 'Он ещё тот нюхач, от него нельзя смыться. Ничто не поможет избежать напотребства. Потеряй 3 уровня.', 3, 1)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
