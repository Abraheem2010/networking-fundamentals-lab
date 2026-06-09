"""Simple TCP echo server used to test the RTT client (Task 1).

Listens on 127.0.0.1:5000, echoes back every byte it receives, and stops
once the client disconnects.
"""
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen(1)
print("Server listening on port 5000...")

conn, addr = server.accept()
print(f"Connected: {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.sendall(data)

conn.close()
server.close()
print("Connection closed.")
print("Server stopped.")
