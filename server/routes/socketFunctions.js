module.exports = function (io) {
  io.use((socket, next) => {
    const token = socket.handshake.headers.authorization?.split(" ")[1];

    if (!token) {
      console.log("No token");
      return next(new Error("Authentication error: Missing token"));
    }

    next();
  });

  io.on("connection", (socket) => {
    console.log(`User ${socket.id} connected`);

    // Handle new messages from clients
    socket.on("new-message", (message) => {
      io.emit("message", message);
    });

    // Handle disconnection
    socket.on("disconnect", () => {
      console.log(`User ${socket.id} disconnected`);
    });
  });
};
