#!/usr/bin/env python3
import socket, sys, threading, _thread
import time
import paramiko

#generate keys with 'ssh-keygen -t rsa -f server.key'
HOST_KEY = paramiko.RSAKey(filename='server.key')
SSH_PORT = 2222
LOGFILE = 'sshlogins.txt' #File to log the user:password combinations to
LOGFILE_LOCK = threading.Lock()

# Function to write a string to the logfile
def log(logstr):
    LOGFILE_LOCK.acquire()
    try:
        logfile_handle = open(LOGFILE,"a")
        logfile_handle.write( logstr )
        logfile_handle.close()
    finally:
        LOGFILE_LOCK.release()

# Class to handle SSH requests
class SSHServerHandler (paramiko.ServerInterface):
    # constructor
    def __init__(self, logprefix):
        self.event = threading.Event()
        self.logprefix = logprefix

    # log username and password and return AUTH_FAILED on any request
    def check_auth_password(self, username, password):
        log( self.logprefix + "\"" + username + "\";\"" + password + "\"\n" )

        return paramiko.AUTH_FAILED

    # return allowed authentication methods = password
    def get_allowed_auths(self, username):
        return 'password'

# Function to handle a new connection
def handleConnection(client, logprefix):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    # we use an old SSH banner from Ubuntu
    transport.local_version = 'SSH-2.0-OpenSSH_7.7p1 Ubuntu-4'

    server_handler = SSHServerHandler( logprefix )
    transport.start_server(server=server_handler)
    channel = transport.accept(1)

    if not channel is None:
        channel.close()


# Main loop for hp ssh server
def main():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', SSH_PORT))
        server_socket.listen(100)

        paramiko.util.log_to_file ('paramiko.log', level= "WARN")

        while(True):
            try:
                client_socket, client_addr = server_socket.accept()

                ct = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime() )
                logprefix =  ct + ";" + str(client_addr[0]) + ";" + str(client_addr[1]) + ";"

                _thread.start_new_thread(handleConnection,(client_socket, logprefix,))
            except Exception as e:
                print("ERROR: Client handling")
                print(e)

    except Exception as e:
        print("ERROR: Failed to create socket")
        print(e)
        sys.exit(1)

main()
