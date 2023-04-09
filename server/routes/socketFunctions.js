const MessageController = require("../controllers/MessageController");
const redisClient = require("../engine/redis");
const Functions = require("../utils/functions");
const { ObjectId } = require("mongodb");

module.exports = function (io) {
  const checkToken = async (socket, next) => {
    console.log("Checking token");
    const token = socket.handshake.headers["x-token"];
    if (!token) {
      console.log("Not authorized");
      return next(new Error("Authentication error: no token provided"));
    }
    const key = `auth_${token}`;
    const userId = await redisClient.get(key);
    if (!userId) {
      console.log("Not authorized");
      return next(new Error("Authentication error: no token provided"));
    }
    const idObject = new ObjectId(userId);
    const user = await Functions.searchUser({ _id: idObject });
    socket.userID = userId;
    socket.username = user.username;
    const newkey = `socket_${userId}`;
    redisClient.set(newkey, socket.id);
    next();
  };

  io.use(checkToken);

  io.on("connection", (socket) => {
    console.log(
      `User ${socket.id} userId: ${socket.userID} username: ${socket.username} connected`
    );

    socket.on("message", async (data) => {
      const { message, chatroomID, recepientID } = data;
      const recipientSocket = await redisClient.get(`socket_${recepientID}`);
      if (recipientSocket) {
        io.to(recipientSocket).emit("message", {
          message,
          senderID: socket.userID,
          recepientID: recepientID,
          createdAt: new Date().getTime(),
          senderusername: socket.username,
        });
      }
      console.log(
        "message",
        message,
        "recipientSocket",
        recipientSocket,
        "sendID",
        socket.userID
      );
      const messageData = {
        senderID: socket.userID,
        message: message.toString(),
        recepientID: recepientID,
        senderusername: socket.username,
      };
      MessageController.appendMessage(chatroomID, messageData);
    });

    socket.on("disconnect", async () => {
      console.log(`User ${socket.id} disconnected`);
      await redisClient.delSocketValue(socket.id);
    });
  });
};
