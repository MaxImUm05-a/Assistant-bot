from models import *

def set_question(text, section):
    """Sets the question into the table"""

    with db:
        questions = get_guestion(section)
        for q in questions:
            if q == text:
                return 'this question has already existed'
        Question(section = section, text = text, like = 0, dislike = 0).save()

def get_guestion(section):
    """Get all messages from a particular section"""

    q = []

    with db:
        queses = Question.select(Question.text).where(Question.section == section)

        for ques in queses:
            q.append(ques.text)

    return q

def delete_question(id):
    """Delete a particular message"""

    with db:
        q = Question.get(Question.nom == id)
        q.delete_instance()

def like(id):
    """Like a message"""

    with db:
        Question.update({Question.like: Question.like+1}).where(Question.nom == id).execute()

def dislike(id):
    """Dislike a message"""

    with db:
        Question.update({Question.dislike: Question.dislike + 1}).where(Question.nom == id).execute()

def get_id(q, q_info):
    """Get id from q & q_info"""

    text = q[q_info]

    with db:
        queses = Question.select().where(Question.text == text)
        for ques in queses:
            id = ques.nom

    return id