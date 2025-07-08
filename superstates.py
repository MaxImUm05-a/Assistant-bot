from models import *

def set_user(id, q_list, q_info):
    """Set a new superuser"""

    q = '-|-'.join(q_list)

    with db:
        Superstate(user_id = id, q = q, q_info = q_info).save()

def change_state(id, q_list, q_info):
    """Change variables q і q_info"""

    q = '-|-'.join(q_list)

    with db:
        Superstate.update({Superstate.q: q}).where(Superstate.user_id == id).execute()
        Superstate.update({Superstate.q_info: q_info}).where(Superstate.user_id == id).execute()


def get_state(id):
    """Get q & q_info"""

    with db:
        q_string = Superstate.select().where(Superstate.user_id == id)
        for q_str in q_string:
            q = q_str.q.split('-|-')
            q_info = q_str.q_info

    return q, q_info

def delete_user(id):
    """Delete superuser"""

    with db:
        user = Superstate.get(Superstate.user_id == id)
        user.delete_instance()

def delete_all_users():
    """Delete all superusers"""

    with db:
        users = Superstate.select()
        for user in users:
            user.delete_instance()