import CurseBase


class UnbearablyVileCurseLoseYourRandomStuff(CurseBase):
    def __init__(self):
        super(UnbearablyVileCurseLoseYourRandomStuff, self).__init__(
            'Невыносимо гнусное проклятие! Потеряй рандомную шмотку!'
        )

    def use_bad_things(self, req, hero):  # проклятье на нас
        pass
