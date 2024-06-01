from dto import UserRegisterDTO
import services
from services import login_required
from db import commit
from db import conn


@login_required
@commit
def todo_operations():
    while True:
        print('View all todos ==> 1')
        print('Create todo ==> 2')
        print('Update todo ==> 3')
        print('Delete todo ==> 4')
        print('Exit ==> 0')
        ch = int(input(':...'))
        if ch == 1:
            services.show_todos()
        elif ch == 2:
            services.add_todo()
        elif ch == 3:
            services.update_todo()
        elif ch == 4:
            services.delete_todo()
        else:
            break


def menu():
    print('Log in          ==> 1')
    print('Register        ==> 2')
    print('Todo operations ==> 3')
    print('Log out         ==> 4')
    print('Block user      ==> 5')
    print('Exit            ==> 0')


def run():
    while True:
        menu()
        n = int(input('?...'))
        if n == 1:
            u = input('Enter username: ')
            p = input('Enter password: ')
            services.login(u, p)
        elif n == 2:
            u = input('Enter username: ')
            p = input('Enter password: ')
            dto = UserRegisterDTO(u, p)
            services.register(dto)
        elif n == 3:
            todo_operations()
        elif n == 4:
            services.log_out()
        elif n == 5:
            services.block_user()
        else:
            break


run()
