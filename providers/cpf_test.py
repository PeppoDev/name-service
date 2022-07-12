import socket
import ast
from constants import DNS_HOST, DNS_PORT

HOST = "localhost"


def validation_cpf(cpf: str) -> bool:
    if len(cpf) != 11:
        return False
    else:
        return True


def handle_register(name: str, conn: socket) -> None:
    message = {'name': name, 'action': "register"}
    conn.send(str(message).encode())


def handle_response(data, conn) -> None:
    msg = ast.literal_eval(data.decode())

    print(msg)

    message = {'result': validation_cpf(
        msg['data']['cpf']), 'action': 'response'}
    conn.send(str(message).encode())


def main() -> None:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((DNS_HOST, DNS_PORT))
        handle_register("cpf_validation", conn)
        conn.close

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.bind((HOST, 0))
        conn.listen()

        conn, addr = conn.accept()
        while True:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if not data:
                break
            handle_response(data, conn)


if __name__ == '__main__':
    main()
