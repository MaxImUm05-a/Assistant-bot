from models import *


def set_super(name, tg_nick, id):
    """Setting of the superuser"""

    if tg_nick == None:
        tg_nick = '|none|'

    with db:
        Superuser(name=name, tg_nick=tg_nick, user_id=id).save()


def get_super():
    """Get ids of all superusers"""

    super = []

    with db:
        users = Superuser.select(Superuser.user_id)

        for user in users:
            super.append(user.user_id)



    return super