var http = required('http');

http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    req.write('Hello World\n');
    res.end('Hello World\n');
}).listen(8080);