import signal

from app import *


def signal_handler(_signal, frame):
	import os
	os._exit(1)


signal.signal(signal.SIGINT, signal_handler)
communicator.start()
initiate_node(3000)


def send_tx():
	print("Input a message \n")
	print("9. Back")
	print("0. Quit")

	choice = input(" >>  ")
	print(choice)

	if choice != '9' or choice != '0':
		message = choice
		pri_key, pub_key = key.get_key()
		tx = transaction.create_tx(pub_key, pri_key, message)
		transaction.send_tx(tx)

	exec_menu(choice)
	return


def show_node_list():
	print("\nNode list\n")

	list_all_node()
	back()


def show_transaction_list():
	print("\nTransaction list\n")

	list_all_transaction()
	back()


def show_block_list():
	print("\nBlock list\n")

	list_all_block()
	back()

# Execute menu
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
	print("2. Show node list")
	print("3. Show transaction list")
	print("4. Show block list")

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
	'2': show_node_list,
	'3': show_transaction_list,
	'4': show_block_list,
	'9': back,
	'0': exit,
}

print("\nCommand line interface for private block chain.\n")

if __name__ == '__main__':
	main_menu()
