# SNSSH
A very basic SSH implementation in python

**Dont try to execute commands as nano or vim**

# Usage
### Server
First, you need to start the server and specify an IP address and a port as a parameter
```
cd SNSSH/src/server
python server.py 127.0.0.1 5050
```

### Client
You need to do the same but chaging server.py by client.py
```
cd SNSSH/src/client
python client.py 127.0.0.1 5050
```
