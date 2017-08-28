import logging
from venv import logger

import click

import transaction
from app.MainController import MainController
import key

@click.group()
def cli():
	pass


@cli.command()
@click.option('--port', '-p', help="Will print verbose messages.")
def run(port):
	MainController.initiate_node(port)


@cli.command()
@click.option('--addr', '-a', multiple=True, help="Will print verbose messages.")
@click.option('--message', '-m', multiple=True, help="Will print verbose messages.")
def sendtx(addr, message):
	MainController.set_my_node()

	if len(addr) != len(message):
		click.echo('arrggg')

	for idx in range(len(addr)):
		pri_key, pub_key = key.get_key()
		tx = transaction.create_tx(pub_key, pri_key, addr[idx], message[idx])
		transaction.send_tx(tx)


@cli.command()
def quit():
	exit(0)
