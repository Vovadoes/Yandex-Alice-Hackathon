import CurseBase


class LoseTheArmorYoureWearing(CurseBase):
    def __init__(self):
        super(LoseTheArmorYoureWearing, self).__init__(
            'Потеряй надетый броник.'
        )

    def use_bad_things(self, req, hero):  # проклятье на нас
        pass
