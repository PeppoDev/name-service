import socket
import ast
from constants import DNS_HOST, DNS_PORT
from typing import Dict

HOST = "localhost"
PORT = 65440


def calc_imc(metrics: Dict[any, any]) -> float:
    height = float(metrics['height'])
    weight = float(metrics['weight'])
    return weight / (height ** 2)


def handle_register(name: str, conn: socket) -> None:
    message = {'name': name, 'action': "register",
               'port': conn.getsockname()[1], 'ip': HOST}
    conn.send(str(message).encode())


def handle_response(data, conn) -> None:
    msg = ast.literal_eval(data.decode())

    print(msg)

    message = {'result': calc_imc(
        msg['data']), 'action': 'response'}
    conn.send(str(message).encode())


def main() -> None:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((DNS_HOST, DNS_PORT))
        handle_register("imc_calc", conn)
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
