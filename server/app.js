const http = require("http");
const express = require("express");
const authRoutes = require("./routes/auth");
const app = express();
const server = http.createServer(app);
const mysql = require("mysql");
const DBStorage = require("./engine/db_storage");
const admin = require("firebase-admin");
const serviceAccount = require("secret/serviceAccountKey.json");
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});
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

const con = mysql.createConnection({
  host: "localhost",
  user: "chit",
  password: "chitchat_pwd",
});

con.connect(function (err) {
  if (err) throw err;
  console.log("Connected!");
});

const dbcontroller = new DBStorage(con);
authRoutes(app);
require("./routes/socketFunctions")(io);

server.listen(3000);
