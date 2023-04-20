import socket
import threading


HOST = '127.0.0.1' # 服务器 IP 地址
PORT = 5000 # 服务器端口号

def handle_client(client_socket,Data):
    while True:
        # 接收客户端消息
        data = client_socket.recv(1024)
        if not data:
            break
        print('收到消息：', data.decode())
        # 向客户端发送消息
        client_socket.send(str(Data).encode())

    # # 关闭连接
    # client_socket.close()

def start_server():
    # 创建TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定地址和端口
    server_socket.bind((HOST, PORT))

    # 监听连接
    server_socket.listen()

    print('服务器已启动，等待客户端连接...')

    while True:
        # 接受连接
        client_socket, client_address = server_socket.accept()

        print(f'客户端 {client_address} 已连接')
        for i in range(10):
            # 处理客户端连接
            client_thread = threading.Thread(target=handle_client, args=(client_socket,i))
            client_thread.start()


if __name__ == '__main__':
    start_server()
