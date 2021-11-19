import socket
import sys
import pickle
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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
    SERVER = sys.argv[1]
except:
    print(F'Usage: python {sys.argv[0]} <IP> <PORT>')

# Connect to the server
Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Client.connect((SERVER,PORT))

# PROTOCOL STEP 1 Recive Server Public KEY
msg_len = Client.recv(128).decode('utf-8')
if msg_len:
    print('[DEBUGING] Server KEY LEN' + msg_len)
    Server_key = Client.recv(int(msg_len))
    
    # Import Server public Key and gen a cipher object with Server key
    KEY = RSA.import_key(Server_key)
    cipher_rsa = PKCS1_OAEP.new(KEY)
    print('[PROTOCOL] 1 Recive Server Public KEY')


# PROTOCOL STEP 2 Send Client Public_Key
    Client.send(bin_exported_Key_len)
    Client.send(bin_exported_Key)
    print('[PROTOCOL] 2 Send Encrypted Client Public_Key')

# PROTOCOL STEP 3 Sart Encrypted Shell

    print('[PROTOCOL] 3 Sart Encrypted Shell')
while True:
    # Cypher Command With Server Public_Key
    RawMessage = input('SNSSH > ')
    message = cipher_rsa.encrypt(RawMessage.encode('utf-8'))

    msg_len = len(message)
    send_len = str(msg_len).encode('utf-8')
    send_len += b' ' * (128 - len(send_len))

    Client.send(send_len)
    Client.send(message)

    # Recive Message
    msg_len = Client.recv(128).decode('utf-8')
    if msg_len:
        msg_len = int(msg_len)
        msg = Client.recv(msg_len)

        dec_data = decipher_rsa.decrypt(msg).decode('utf-8')[0:-1]
        print(dec_data)