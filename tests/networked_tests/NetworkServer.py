import socket
import asyncio

async def transfer_data(reader, writer, data):
    writer.write(data.encode())
    await writer.drain()
    writer.write_eof()

async def next_connection(addr):
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('ACTUAL IP ON NETWORK', 8889)) 
        sock.connect(('ACTUAL IP ON NETWORK', 8889))
        
        reader, writer = await asyncio.open_connection(sock=sock)

        transfer_data(reader, writer, "hello again")

async def handle_connection(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close() 

async def main():
    server = await asyncio.start_server(handle_connection, 'ACTUAL IP ON NETWORK', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever() 

if __name__ == '__main__':
     asyncio.run(main())

