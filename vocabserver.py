import socket

DATABASE = {
    'APPLE': {
        'DEF': 'A round fruit with red or green skin and a whitish interior.',
        'SYN': 'None'
    },
    'FAST': {
        'DEF': 'Moving or capable of moving at high speed.',
        'SYN': 'Quick, Rapid, Swift'
    },
    'HAPPY': {
        'DEF': 'Feeling or showing pleasure or contentment.',
        'SYN': 'Joyful, Cheerful, Glad'
    }
}

HOST = '127.0.0.1'
PORT = 12345

def process_request(request_text):
    parts = request_text.strip().upper().split()
    if len(parts) == 0:
        return "400 BAD_REQUEST\nInvalid format."
    
    method = parts[0]
    
    if method == 'QUIT':
        return "201 GOODBYE\nConnection closed by client."
    
    if len(parts) < 2:
        return "400 BAD_REQUEST\nMissing word argument."
    
    word = parts[1]
    
    if method not in ['DEF', 'SYN']:
        return "400 BAD_REQUEST\nUnknown method."
    
    if word not in DATABASE:
        return f"404 NOT_FOUND\nWord '{word}' not found in database."
    
    data = DATABASE[word][method]
    return f"200 OK\n{data}"

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Server listening on {HOST}:{PORT} using TCP...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"\n[+] Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                        
                    request_str = data.decode('utf-8')
                    print(f"[-] Received Request: {request_str.strip()}")
                    
                    response_str = process_request(request_str)
                    
                    status_line = response_str.split('\n')[0]
                    print(f"[-] Sending Response Status: {status_line}")
                    
                    conn.sendall(response_str.encode('utf-8'))
                    
                    if "201 GOODBYE" in response_str:
                        print(f"[*] Closing connection with {addr}")
                        break

if __name__ == "__main__":
    start_server()