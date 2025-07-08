import peewee as pw

db = pw.SqliteDatabase('database.db')  # встановлення БД


class BaseModel(pw.Model):
    user_id = pw.IntegerField(unique=True)

    class Meta:
        database = db


class State(BaseModel):
    """Users' states"""

    state = pw.TextField()

    class Meta:
        order_by = 'user_id'
        db_table = 'states'


class Superuser(BaseModel):
    """The list of superusers"""

    name = pw.TextField()
    tg_nick = pw.TextField()

    class Meta:
        order_by = 'user_id'
        db_table = 'superusers'


class Superstate(BaseModel):
    """Saves two important variables (q, q_info) for listing messages"""

    q = pw.TextField()
    q_info = pw.IntegerField()

    class Meta:
        order_by = 'user_id'
        db_table = 'superstates'

class Question(pw.Model):
    """The list of messages"""

    nom = pw.PrimaryKeyField(unique=True)
    section = pw.TextField()
    text = pw.TextField()
    like = pw.IntegerField()
    dislike = pw.IntegerField()

    class Meta:
        order_by = 'nom'
        db_table = 'questions'
        database = db

def create_tables():
    with db:
        db.create_tables([Superstate])

create_tables()