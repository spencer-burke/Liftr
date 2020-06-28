import socket
import asyncio

async def next_connection(addr):
    pass

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

