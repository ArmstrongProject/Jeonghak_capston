import socket

host = '127.0.0.1'
port = 4000

def run():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        while True:
            msg = str(input())
            if not msg or (msg == '1'):
                sock.sendall(msg.encode())
                sock.close()
                break
            sock.sendall(msg.encode())

if __name__ == '__main__':
    run()
