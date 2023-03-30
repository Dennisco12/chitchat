const http = require("http");
const server = http.createServer();
const io = require("socket.io")(server, {
  cors: {
    origin: "*",
  },
});

io.use((socket, next) => {
  const token = socket.handshake.headers.authorization?.split(" ")[1];

  if (!token) {
    console.log("No token");
    return next(new Error("Authentication error: Missing token"));
  }

  next();
});

io.on("connection", (socket) => {
  console.log("connexted");
});

server.listen(3000);
