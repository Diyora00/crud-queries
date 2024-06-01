from validators import check_validators
from dto import UserRegisterDTO
from db import commit
from db import cur, conn
from typing import Optional
import bcrypt
from models import User, UserStatus, UserRole, TodoType
from sessions import Session
import utils

session = Session()
session_id = 0


def hash_password(raw_password: Optional[str] = None):
    assert raw_password, 'Raw password can not be None'
    return bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(raw_password: Optional[str] = None, encoded_password: Optional[str] = None):
    assert raw_password, 'Raw password can not be None'
    assert encoded_password, 'Encoded password can not be None'
    return bcrypt.checkpw(raw_password.encode('utf-8'), encoded_password.encode('utf-8'))


def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.session:
            b = utils.BadRequest('Unauthorized')
            return b.message()
        res = func(*args, **kwargs)
        return res
    return wrapper


@commit
def login(username_i: str, password_i: str):
    if username_i == session.session:
        p1 = utils.BadRequest('You already logged in', status_code=401)
        return p1.message()

    get_user_by_username = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username, (username_i,))
    user_data = cur.fetchone()
    if not user_data:
        d = utils.BadRequest('Bad credentials', status_code=401)
        return d.message()

    _user = User()
    _user.assign(user_data)
    global session_id
    session_id = _user.id

    if not check_password(password_i, _user.password):
        update_count_query = """update users set login_try_count = login_try_count + 1 where username = %s;"""
        cur.execute(update_count_query, (_user.username,))
        b = utils.BadRequest('Bad credentials')
        return b.message()

    if _user.login_try_count >= 3:
        c = utils.BadRequest('You are locked!')
        return c.message()

    session.add_session(_user.username)
    f = utils.ResponseData('User Successfully Logged in')
    return f.message()


@commit
def register(dto_: UserRegisterDTO):
    try:
        check_validators(dto_)
        user_info = """SELECT * FROM users WHERE username = %s;"""
        cur.execute(user_info, (dto_.username,))
        user = cur.fetchone()
        if user:
            b = utils.BadRequest('User already exists')
            return b.message()
        insert_q = """insert into users (username, password, role, status, login_try_count)
                      values (%s, %s, %s, %s, 0);"""
        cur.execute(insert_q, (dto_.username, hash_password(dto_.password),
                               UserRole.USER.value, UserStatus.ACTIVE.value,))
        r = utils.ResponseData('User Successfully Registered')
        return r.message()
    except AssertionError as e:
        b = utils.BadRequest(e)
        return b.message()


def log_out():
    global session
    if session.check_session():
        session.session = None
        r = utils.ResponseData('User successfully logged Out')
        return r.message()


def show_todos():
    q = """SELECT * FROM todos WHERE user_id = %s;"""
    cur.execute(q, (session_id,))
    all_ = cur.fetchall()
    for i in all_:
        print(i)


@commit
def add_todo():
    title: str = input('Enter name: ')
    add_query = """INSERT INTO todos (name, todo_type, user_id) VALUES (%s, %s, %s);"""
    cur.execute(add_query, (title, TodoType.Personal.value, session_id))


@commit
def update_todo():
    old_name = input('Enter todo name to be updated: ')
    s_q = """ SELECT * FROM todos WHERE name = %s;"""
    cur.execute(s_q, (old_name,))
    todo = cur.fetchone()
    if todo:
        new_name = input('Enter new todo name: ')
        u_q = """UPDATE todos SET name = %s WHERE name = %s;"""
        cur.execute(u_q, (new_name, old_name))
        r = utils.ResponseData('Todo successfully updated')
        return r.message()
    else:
        b = utils.BadRequest('Todo does not exist!')
        return b.message()


@commit
def delete_todo():
    td_id = input('Enter todo\'s id to be deleted: ')
    d_q = """DELETE FROM todos WHERE id = %s;"""
    cur.execute(d_q, (td_id,))
    r = utils.ResponseData('Todo successfully deleted.')
    return r.message()


def block_user():
    username = input('Which user to be blocked?: ')
    u = """SELECT * FROM users WHERE username = %s;"""
    cur.execute(u, (username,))
    user = cur.fetchone()
    if user:
        b_q = """UPDATE users SET login_try_count = 4 WHERE username = %s;"""
        cur.execute(b_q, (username,))
        r = utils.ResponseData('User blocked')
        return r.message()
    r = utils.BadRequest('User not found!')
    return r.message()
