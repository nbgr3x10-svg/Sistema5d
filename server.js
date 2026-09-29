const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8080;

const mime = {
  '.html': 'text/html',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.js': 'text/javascript',
  '.css': 'text/css'
};

http.createServer((req, res) => {
  let file = req.url === '/'? '/index.html' : req.url;
  let filePath = path.join(__dirname, file);

  if (!fs.existsSync(filePath)) {
    res.writeHead(404);
    return res.end('404');
  }

  let ext = path.extname(filePath);
  res.writeHead(200, {'Content-Type': mime[ext] || 'text/plain'});
  fs.createReadStream(filePath).pipe(res);
}).listen(PORT, () => {
  console.log(`Lojão da Sofia online na porta ${PORT}`);
  console.log(`Acesse: http://localhost:${PORT}`);
});
