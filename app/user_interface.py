import signal, time
from app import app_controller
#UI를 보여주기 위한 파일

#앱 종료
def terminate():
    app_controller.finish_app()

#블록 생성 인터페이스
def create_block_menu():
    app_controller.create_block()
    time.sleep(2)
    menu_actions['main_menu']()

#트랜잭션 생성 인터페이스
def send_tx():
    print("Input a message \n")
    print("9. Back")
    print("0. Quit")

    choice = input(" >>  ")
    print(choice)

    if choice != '9' or choice != '0':
        app_controller.send_transaction(choice)

    exec_menu(choice)
    return

#노드 리스트를 블러오는 인터페이스
def show_node_list():
    print("\nNode list\n")
    app_controller.list_all_node()
    time.sleep(2)
    menu_actions['main_menu']()
    return

#현재 트랜잭션 리스트를 불러오는 인터페이스
def show_transaction_list():
    print("\nTransaction list\n")
    app_controller.list_all_transaction()
    time.sleep(2)
    menu_actions['main_menu']()

#블록 리스트를 불러오는 인터페이스
def show_block_list():
    print("\nBlock list\n")
    app_controller.list_all_block()
    time.sleep(2)
    menu_actions['main_menu']()


#메뉴 실행
def exec_menu(choice):
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print
            "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return

#메뉴 보여주
def main_menu():
    print("\nPlease choose the menu you want to start:")
    print("1. Send a transaction")
    print("2. Create a block")
    print("3. Show node list")
    print("4. Show transaction list")
    print("5. Show block list")

    print("\n0. Quit\n")
    choice = input(" >>  ")
    exec_menu(choice)

    return


# Back to main menu
def back():
    menu_actions['main_menu']()

# Menu definition
menu_actions = {
	'main_menu': main_menu,
	'1': send_tx,
	'2': create_block_menu,
	'3': show_node_list,
	'4': show_transaction_list,
	'5': show_block_list,
	'6': back,
	'0': terminate,
}

if __name__ == '__main__':
	main_menu()






