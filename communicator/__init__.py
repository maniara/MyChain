# import argparse
# import os
# from threading import Thread
#
# from click._compat import raw_input
# from netifaces import interfaces, ifaddresses, AF_INET  # dependency, not in stdlib
#
# import zmq
#
#
# def listen(masked):
#     """listen for messages
#
#     masked is the first three parts of an IP address:
#
#         192.168.1
#
#     The socket will connect to all of X.Y.Z.{1-254}.
#     """
#     ctx = zmq.Context.instance()
#     listener = ctx.socket(zmq.SUB)
#     for last in range(1, 255):
#         listener.connect("tcp://{0}.{1}:9000".format(masked, last))
#
#     listener.setsockopt(zmq.SUBSCRIBE, b'')
#     while True:
#         try:
#             print(listener.recv_string())
#         except (KeyboardInterrupt, zmq.ContextTerminated):
#             break
#
#
# def main():
#
#     inet = ifaddresses('en0')[AF_INET]
#     addr = inet[0]['addr']
#     masked = addr.rsplit('.', 1)[0]
#
#     ctx = zmq.Context.instance()
#
#     listen_thread = Thread(target=listen, args=(masked,))
#     listen_thread.start()
#
#     bcast = ctx.socket(zmq.PUB)
#     bcast.bind("tcp://%s:9000" % 'en0')
#
#     while True:
#         try:
#             msg = raw_input()
#             bcast.send_string("%s" % (msg))
#         except KeyboardInterrupt:
#             break
#     bcast.close(linger=0)
#     ctx.term()
#
#
# if __name__ == '__main__':
#     main()