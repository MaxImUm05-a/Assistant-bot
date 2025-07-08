from models import *


states = ['main', 'osn', 'osob', 'propos']


def set_user(id):
    """Set user and state 'main menu' for him"""

    with db:
        State(user_id = id, state = 'main').save()

def change_state(id, state):
    """Set new state"""

    with db:
        State.update({State.state: state}).where(State.user_id == id).execute()

def get_state(id):
    """Get the state of the user"""

    with db:
        user = State.select(State.state).where(State.user_id == id)
        for u in user:
            uer = u.state

    return uer

def delete_user(id):
    """Delete the user"""

    with db:
        user = State.get(State.user_id == id)
        user.delete_instance()