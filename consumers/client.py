from typing import Dict, Tuple
import socket
import ast
from providers.constants import DNS_HOST, DNS_PORT


def request(name: str, data: Dict[str, any]):
    service_address: Tuple(str, str) = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((DNS_HOST, DNS_PORT))
        handle_get_service(name, conn)
        response = conn.recv(1024)

        if not response:
            conn.close()

        msg = response.decode()

        if(msg != "SERVICE_NOT_FOUND"):
            msg = ast.literal_eval(msg)
            service_address = (msg['ip'], msg['port'])
            conn.close()

    print(service_address)
    if(service_address is not None):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            conn.connect(service_address)
            handle_request(data,  conn)
            response = conn.recv(1024)
            print(response.decode())
            conn.close()
    else:
        print("Service not found")


def handle_get_service(name: str, conn: socket) -> None:
    message = {'name': name, 'action': 'lookup'}
    conn.send(str(message).encode())


def handle_request(data: Dict[str, any], conn: socket) -> None:
    message = {'action': 'request', 'data': data}
    conn.send(str(message).encode())
