import socket

HOST = '127.0.0.1'
PORT = 12345

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"[*] Connected to Server {HOST}:{PORT}")
        print("--------------------------------------------------")
        print("Available Commands: DEF <word>, SYN <word>, QUIT")
        print("Example: DEF APPLE")
        print("--------------------------------------------------")
        
        while True:
            user_input = input("\nEnter command: ")
            if not user_input.strip():
                continue
                
            s.sendall(user_input.encode('utf-8'))
            print(f"[-] Sent Message: '{user_input}'")
            
            data = s.recv(1024)
            response_str = data.decode('utf-8')
            
            if not response_str:
                break
                
            response_parts = response_str.split('\n', 1)
            status_line = response_parts[0]
            body = response_parts[1] if len(response_parts) > 1 else ""
            
            print(f"[-] Received Status: {status_line}")
            print(f"[-] Response Data: {body}")
            
            if status_line.startswith("201"):
                print("[*] Disconnected from server.")
                break

if __name__ == "__main__":
    start_client()