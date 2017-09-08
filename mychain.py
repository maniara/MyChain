import signal
import sys

import click

import communicator
import key
from app import *

storage.init()

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

	communicator.find_nodes()


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
	try:
		stop_node()
		sys.exit(0)
	except:
		pass


signal.signal(signal.SIGINT, signal_handler)
