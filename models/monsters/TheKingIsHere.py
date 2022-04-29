import MonsterBase


class TheKingIsHere(MonsterBase):
    def __init__(self):
        super(TheKingIsHere, self).__init__(16, 'Царь тут', 'Сбрось все свои шмотки и всю руку!', 4, 2)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
