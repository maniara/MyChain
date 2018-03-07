import signal
from app import user_interface
from app import app_controller

def signal_handler(_signal, frame):
	app_controller.finish_app()

app_controller.start_app()
signal.signal(signal.SIGINT, signal_handler)
user_interface.main_menu()





