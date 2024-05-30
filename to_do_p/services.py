from db import cur, conn
from models import User
from sessions import Session
import utils

session = Session()


def login(username: str, password: str):
    # user = session.check_session()
    if session.session == username:
        p = utils.BadRequest('You already logged in', status_code=401)
        return p.message()

    get_user_by_username = '''select * from users where username = %s;'''
    cur.execute(get_user_by_username, (username,))
    user_data = cur.fetchone()
    if not user_data:
        d = utils.BadRequest('Username not found in my DB')
        return d.message()
    # _user = User(username=user_data[1], password=user_data[2], role=user_data[3], status=user_data[4],
    #              login_try_count=user_data[5])
    _user = User()
    _user.assign(user_data)
    if password != _user.password:
        update_count_query = """update users set login_try_count = login_try_count + 1 where username = %s;"""
        cur.execute(update_count_query, (_user.username,))
        conn.commit()
        if _user.login_try_count >= 3:
            c = utils.BadRequest('You are locked!')
            return c.message()
        b = utils.BadRequest('Invalid password')
        return b.message()

    session.add_session(_user.username)
    f = utils.ResponseData('User Successfully Logged in')
    return f.message()


while True:
    choice = input('Enter your choice: ')
    if choice == '1':
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        login(username, password)
    else:
        break
