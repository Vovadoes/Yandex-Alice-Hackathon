import CurseBase


class LoseTheLevel(CurseBase):
    def __init__(self):
        super(LoseTheLevel, self).__init__(
            'Потеряй уровень'
        )

    def use_bad_things(self, req, hero):  # проклятье на нас
        pass
