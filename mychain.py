import signal

from app import communicator
from app import storage
import app

def terminate():
	import os
	storage.session.commit()
	storage.session.close()
	app.stop_communicator()
	os._exit(1)


def create_block_menu():
	app.create_block()
	back()


def send_tx():
	print("Input a message \n")
	print("9. Back")
	print("0. Quit")

	choice = input(" >>  ")
	print(choice)

	if choice != '9' or choice != '0':
		app.send_transaction(choice)


	exec_menu(choice)
	return


def show_node_list():
	print("\nNode list\n")

	app.list_all_node()
	back()


def show_transaction_list():
	print("\nTransaction list\n")

	app.list_all_transaction()
	back()


def show_block_list():
	print("\nBlock list\n")

	app.list_all_block()
	back()


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


def signal_handler(_signal, frame):
	terminate()


app.app_start()
signal.signal(signal.SIGINT, signal_handler)

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

print("\nCommand line interface for private block chain.\n")

if __name__ == '__main__':
	main_menu()






