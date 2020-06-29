import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('192.168.1.49', 8888)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

async def client():
    await tcp_echo_client('Hello World!')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('IP 0N NETWORK', 8889))
        sock.listen()
        conn, addr = sock.accept()

        reader, writer = await asyncio.open_connection(sock=conn)

        data = await reader.read()
        print(data.decode())
        

#asyncio.run(tcp_echo_client('Hello World!'))
asyncio.run(client())

