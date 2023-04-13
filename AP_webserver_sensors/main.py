from microserver import MicroPyServer


def hello_world(request):
    ''' request handler '''
    server.send("HELLO WORLD!")

server = MicroPyServer()
''' add route '''
server.add_route("/", hello_world)
''' start server '''
server.start()