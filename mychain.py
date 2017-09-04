import signal

import click

from app import *


@click.group()
def cli():
	"""Command line interface for private block chain."""
	pass


@cli.command()
@click.option('--port', '-p', help="Port number for socket.")
def run(port=None):
	if port:
		initiate_node(port)
	else:
		initiate_node(3000)



@cli.command()
@click.option('--message', '-m', help="Message included in transaction.")
def sendtx(message):
	pri_key, pub_key = key.get_key()
	tx = transaction.create_tx(pub_key, pri_key, message)
	transaction.send_tx(tx)


@cli.command()
@click.argument('target')
def list(target):
	if target == 'block':
		click.echo('list of blocks')
		list_all_block()

	elif target == 'transaction':
		click.echo('list of transactions')
		list_all_transaction()

	elif target == 'node':
		click.echo('list of nodes')
		list_all_node()

	else:
		click.echo('unknown list type')
		click.echo('list type should be one of [block|transaction|node]')


def signal_handler(_signal, frame):
	import os
	os._exit(1)


signal.signal(signal.SIGINT, signal_handler)


# Menu 1
def menu1():
	print("Input a port number \n")
	print("9. Back")
	print("0. Quit")
	choice = input(" >>  ")
	print(choice)

	if choice != '9' or choice != '0':
		port = int(choice)
		if port:
			initiate_node(port)
		else:
			initiate_node(3000)

		communicator.start()

	exec_menu(choice)
	return


# Menu 2
def menu2():
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
	print("Command line interface for private block chain.\n")
	print("Please choose the menu you want to start:")
	print("1. Run")
	print("2. Send a transaction")
	print("\n0. Quit")
	choice = input(" >>  ")
	exec_menu(choice)

	return


# Back to main menu
def back():
	menu_actions['main_menu']()


# Menu definition
menu_actions = {
	'main_menu': main_menu,
	'1': menu1,
	'2': menu2,
	'9': back,
	'0': exit,
}

if __name__ == '__main__':
	main_menu()
