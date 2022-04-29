import MonsterBase


class Kalmadzilla(MonsterBase):
    def __init__(self):
        super(Kalmadzilla, self).__init__(18, 'Кальмадзилла', 'Ты схвачен, намочен,отфигачен и проглочен. Ты мертв. Мертвее мёртвого. Вопросы?', 4, 2)

    def fight_or_not(self, req, hero):  # убежать или драться? Сравнение силы
        pass

    def fight(self, req, hero):  # после использования бонусов, мы сражаемся и смотрим кто победил
        pass

    def do_bad_things(self, req, hero):  # он не убежал
        pass
