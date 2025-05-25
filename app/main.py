import socket  # noqa: F401

SUCCESSFUL_OK_RESPONSE = 'HTTP/1.1 200 OK\r\n'
CLIENT_ERROR_NOT_FOUND = 'HTTP/1.1 404 Not Found\r\n'

def response_with_body(body):
    status_line = SUCCESSFUL_OK_RESPONSE
    headers = f'Content-Type: text/plain\r\nContent-Length: {len(body)}\r\n\r\n'
    return status_line + headers + body

def echo(path):
    response_body = path.split('/echo/')
    return response_body[1]

def verify_endpoint(request_data):
    path = request_data["Request line"][1]

    if path == '/':
        return SUCCESSFUL_OK_RESPONSE + '\r\n'
    elif '/echo/' in path:
        body = echo(path)
        return response_with_body(body)
    elif '/user-agent' in path:
        body = request_data['User-Agent']
        return response_with_body(body)

    return CLIENT_ERROR_NOT_FOUND + '\r\n'

def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()

    while True:
        conn, addr = server_socket.accept()
        print(f'Connection from {addr}')
        data_from_request = conn.recv(4096)
        decoded_data = data_from_request.decode().split('\r\n')
        request_data = {'Request line': decoded_data[0].split(' ')}
        decoded_data.pop(0)
        for request_content in decoded_data:
            section = request_content.split(': ')
            if section[0] != '':
                request_data[section[0]] = section[1]
        
        print(request_data)
        response = verify_endpoint(request_data)
        conn.send(response.encode())
        conn.close()

if __name__ == "__main__":
    main()
