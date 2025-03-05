import socket
import signal
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_sigterm(signum, frame):
    logging.info("SIGTERM received. Ignoring.")

def run_server(host='0.0.0.0', port=9090):
    """
    Runs a socket server that terminates when the client connection is closed.
    Ignores SIGTERM signals and logs them.
    """
    signal.signal(signal.SIGTERM, handle_sigterm)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # Only accept one connection
    logging.info(f"Server listening on {host}:{port} (PID: {os.getpid()})")

    try:
        client_socket, client_address = server_socket.accept()
        logging.info(f"Accepted connection from {client_address}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                logging.info(f"Connection from {client_address} closed by client.")
                break  # Client closed the connection

            # Process data (e.g., send a response)
            client_socket.sendall(b"OK\n") # send confirmation.
            logging.debug(f"Received data from {client_address}: {data.decode('utf-8').strip()}")

    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        if 'client_socket' in locals():
            client_socket.close()
        server_socket.close()
        logging.info("Server stopped.")

if __name__ == "__main__":
    run_server()