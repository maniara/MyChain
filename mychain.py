import signal
from app import user_interface
from app import app_controller

def signal_handler(_signal, frame):
	app_controller.finish_app()

#프라이빗 블록체인의 경우 ip 리스트가 필요함
ip_list = ["192.168.0.37","192.168.0.20"]
app_controller.start_app(ip_list, isPrivate=True)

#앱 종료를 위한 시그널 생성 (ctrl+c)
signal.signal(signal.SIGINT, signal_handler)

#메뉴 호출
user_interface.main_menu()