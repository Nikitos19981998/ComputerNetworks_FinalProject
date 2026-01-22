import socket
import threading

#
HOST = '127.0.0.1'
PORT = 5555

# : {username: client_socket}
clients = {}

def handle_client(client_socket):
    """
   (Thread)
    """
    username = ""
    try:
        # שלב 1: קבלת שם המשתמש מהלקוח
        username = client_socket.recv(1024).decode('utf-8')
        clients[username] = client_socket
        print(f"[NEW CONNECTION] {username} connected.")
        
        while True:
            # קבלת הודעה מהלקוח
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            # פורמט ההודעה המצופה: "TargetName: Message Content"
            if ':' in message:
                target_name, msg_content = message.split(':', 1)
                target_name = target_name.strip()
                
                # בדיקה אם הלקוח היעד מחובר
                if target_name in clients:
                    target_socket = clients[target_name]
                    final_msg = f"{username}: {msg_content}"
                    target_socket.send(final_msg.encode('utf-8'))
                else:
                    error_msg = f"User {target_name} not found."
                    client_socket.send(error_msg.encode('utf-8'))
            else:
                client_socket.send("Invalid format. Use 'Name: Message'".encode('utf-8'))

    except Exception as e:
        print(f"Error with client {username}: {e}")
    finally:
        # ניתוק הלקוח
        if username in clients:
            del clients[username]
        client_socket.close()
        print(f"[DISCONNECT] {username} disconnected.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP Protocol
    server.bind((HOST, PORT))
    server.listen(5) # האזנה ל-5 לקוחות לפחות [cite: 49]
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        client_sock, addr = server.accept()
        # יצירת Thread חדש לכל לקוח שמגיע [cite: 61]
        thread = threading.Thread(target=handle_client, args=(client_sock,))
        thread.start()

if __name__ == "__main__":
    start_server()
