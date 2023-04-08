const redisClient = require("../engine/redis");

module.exports = function (io) {
  const checkToken = async (socket, next) => {
    const token = socket.handshake.headers["x-token"];
    if (!token) {
      return next(new Error("Authentication error: no token provided"));
    }
    const key = `auth_${token}`;
    const userId = await redisClient.get(key);
    socket.userId = userId;
    const newkey = `socket_${userId}`;
    redisClient.set(newkey, socket.id);
    next();
  };

  io.use(checkToken);

  io.on("connection", (socket) => {
    console.log(`User ${socket.id} userId: ${socket.userId} connected`);

    socket.on("new-message", async (data) => {
      const { message, receiver } = data;
      const recipientSocket = await redisClient.get(`socket_${receiver}`);
      if (recipientSocket) {
        console.log(
          "message",
          message,
          "recipientSocket",
          recipientSocket,
          "sendID",
          socket.userId
        );
        io.to(recipientSocket).emit("new-message", {
          message,
          sender: socket.userId,
        });
      }
    });

    socket.on("disconnect", async () => {
      console.log(`User ${socket.id} disconnected`);
      await redisClient.delSocketValue(socket.id);
    });
  });
};
