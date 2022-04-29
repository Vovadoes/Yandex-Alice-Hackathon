import CurseBase


class YourWeaponWasStolenWhatSlobYouAre(CurseBase):
    def __init__(self):
        super(YourWeaponWasStolenWhatSlobYouAre, self).__init__(
            'У тебя украли оружие! Какой ты растяпа!'
        )

    def use_bad_things(self, req, hero):  # проклятье на нас
        pass
