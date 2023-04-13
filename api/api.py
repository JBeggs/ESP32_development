
def api(request, conn):
    request_data = request.decode("utf-8")
    print(request_data)

    request_test = str(request)
    test = request_test.find('test=') > -1
    print(test)
    if test:
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall('<h1>Hello World</h1>')
        conn.close()
        print('done')
    return '<h1>Hello World</h1>'