import socket, os
from threading import Thread

cur_client = None
try:
    print("Forward", pod_port, "to", f"{host}:{port}", flush=True)

    with open("/tmp/tunnel_pid", "w") as f:
        f.write(str(os.getpid()))

    def responses(conn):
        global cur_client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))
            print("Sucessfully connected to", f"{host}:{port}", flush=True)
            cur_client = client
            while True:
                try:
                    data = client.recv(1024)
                except Exception:
                    data = None
                if not data:
                    break
                else:
                    try:
                        print("<", data.decode(), flush=True)
                    except:
                        print("< --binary data--")
                    conn.send(data)
            cur_client = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", pod_port))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connection from {addr}", flush=True)
                Thread(target=responses, args=[conn], daemon=True).start()
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    try:
                        print(">", data.decode(), flush=True)
                    except:
                        print("> --binary data--")
                    try:
                        cur_client.send(data)
                    except Exception:
                        break
                try:
                    cur_client.close()
                except:
                    ...
                print("-------------", flush=True)
                print("", flush=True)

except Exception as e:
    print(e)
    exit(1)
