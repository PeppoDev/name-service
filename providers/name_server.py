import socket
import ast
from typing import Tuple
from constants import DNS_HOST, DNS_PORT


services = []


def register(name: str, address: Tuple[str, str]):
    for service in services:
        if service[0] == name:
            services.remove(service)

    services.append((name, address[0], address[1]))
    print("Registered service: {0} on address {1}:{2}".format(
        name, address[0], address[1]))


def lookup(name):
    for service in services:
        if service[0] == name:
            return service
    return None


def print_services():
    for service in services:
        print(service)


def handle_message(data: bytes, conn: socket) -> None:
    msg = ast.literal_eval(data.decode())

    match msg['action']:
        case "register":
            address: Tuple[str, str] = (msg['ip'], msg['port'])
            register(msg["name"], address)
            conn.sendall(b"OK")
            print_services()
        case "lookup":
            service = lookup(msg["name"])
            if service is None:
                conn.send(b"SERVICE_NOT_FOUND")
            else:
                conn.send(str({"ip": service[1], "port": service[2]}).encode())

        case _:
            conn.send(b"COMMAND_NOT_FOUND")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((DNS_HOST, DNS_PORT))
        s.listen()

        print("Listening on {0}:{1}".format(DNS_HOST, DNS_PORT))

        while True:
            conn, _ = s.accept()
            data = conn.recv(1024)
            if not data:
                break
            handle_message(data, conn)


if __name__ == '__main__':
    main()
