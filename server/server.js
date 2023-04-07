const http = require("http");
const express = require("express");
const app = express();
const server = http.createServer(app);
const routes = require("./routes");

const io = require("socket.io")(server, {
  cors: {
    origin: "*",
  },
});

app.use(express.json());
app.use(express.urlencoded());
app.use("/", routes);
require("./routes/socketFunctions")(io);

server.listen(3000, () => {
  console.log("Server started on port 3000");
});
