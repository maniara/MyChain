import click

import transaction
from app.MainController import MainController
import key
import click

import key
import transaction
from app.MainController import MainController


@click.group()
def cli():
	"""Command line interface for private block chain."""
	pass

@cli.command()
@click.option('--port', '-p', is_flag=True, help="Port number for socket.")
def run(port=None):
	if port:
		MainController.initiate_node(port)
	else:
		MainController.initiate_node(3000)

@cli.command()
@click.option('--addr', '-a', multiple=True, help="Address for sending a transaction.")
@click.option('--message', '-m', multiple=True, help="Message included in transaction.")
def sendtx(addr, message):
	MainController.set_my_node()

	if len(addr) != len(message):
		click.echo('arrggg')

	for idx in range(len(addr)):
		pri_key, pub_key = key.get_key()
		tx = transaction.create_tx(pub_key, pri_key, addr[idx], message[idx])
		transaction.send_tx(tx)


@cli.command()
@click.argument('target')
def list(target):
	if target == 'block':
		click.echo('list of blocks')
		MainController.list_all_block()

	elif target == 'transaction':
		click.echo('list of transactions')
		MainController.list_all_transaction()

	elif target == 'node':
		click.echo('list of nodes')
		MainController.list_all_node()

	else:
		click.echo('unknown list type')
		click.echo('list type should be one of [block|transaction|node]')

@cli.command()
def quit():
	exit(0)
