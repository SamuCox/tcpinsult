import asyncio
import random

def load_words(filename):
    with open(filename) as f:
        return f.read().splitlines()

insults1 = load_words("insults1.txt")
insults2 = load_words("insults2.txt")
insults3 = load_words("insults3.txt")

async def handle_echo(reader, writer):

    writer.write(b"What is your name?\n")
    name = await reader.readline()
    name = name.decode().strip()

    addr = writer.get_extra_info('peername')
    
    try: 
        while True:
            data = colourise(generate_insult(name)).encode()
            writer.write(data)
            await writer.drain()
    except BrokenPipeError:
        print("Close the client socket")

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '0.0.0.0', 8888, loop=loop)
server = loop.run_until_complete(coro) 

def generate_insult(name):
    c = random.choice
    return f"{name}, thou {c(insults1)} {c(insults2)} {c(insults3)}! "

def colourise(s):
    colour = random.randint(31,37)
    if not random.randint(0,4):
        s = s.upper() 
    return f"\x1b[{colour}m{s}\x1b[0m"



# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()