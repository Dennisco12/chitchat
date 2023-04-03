module.exports = function (io) {
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
