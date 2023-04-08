const MessageController = require("../controllers/MessageController");
const redisClient = require("../engine/redis");

module.exports = function (io) {
  const checkToken = async (socket, next) => {
    const token = socket.handshake.headers["x-token"];
    if (!token) {
      return next(new Error("Authentication error: no token provided"));
    }
    const key = `auth_${token}`;
    const userId = await redisClient.get(key);
    socket.userID = userId;
    const newkey = `socket_${userId}`;
    redisClient.set(newkey, socket.id);
    next();
  };

  io.use(checkToken);

  io.on("connection", (socket) => {
    console.log(`User ${socket.id} userId: ${socket.userID} connected`);

    socket.on("new-message", async (data) => {
      const { message, chatroomID, recepientID } = data;
      const recipientSocket = await redisClient.get(`socket_${recepientID}`);
      if (recipientSocket) {
        console.log(
          "message",
          message,
          "recipientSocket",
          recipientSocket,
          "sendID",
          socket.userID
        );
        io.to(recipientSocket).emit("new-message", {
          message,
          senderID: socket.userID,
          recepientID: recepientID,
          createdAt: new Date(),
        });
        const messageData = {
          senderID: socket.userID,
          message: message,
          recepientID: recepientID,
        };
        MessageController.appendMessage(chatroomID, messageData);
      }
    });

    socket.on("disconnect", async () => {
      console.log(`User ${socket.id} disconnected`);
      await redisClient.delSocketValue(socket.id);
    });
  });
};
