const { ObjectId } = require("mongodb");
const dbClient = require("../engine/db_storage");
const redisClient = require("../engine/redis");
const Functions = require("../utils/functions");

async function getChatroom(userId1, userId2) {
  const chatrooms = await dbClient.chatroomsCollection();
  const result = await chatrooms.findOne({
    recepients: {
      $all: [new ObjectId(userId1), new ObjectId(userId2)],
    },
  });

  if (result) {
    return result;
  } else {
    const newChatroom = {
      recepients: [new ObjectId(userId1), new ObjectId(userId2)],
      messages: [],
    };
    const insertResult = await chatrooms.insertOne(newChatroom);
    return {
      _id: insertResult.insertedId.toString(),
      messages: [],
    };
  }
}

const MessageController = {
  async startChat(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const id = await redisClient.get(key);
    if (id) {
      const { recepient } = request.params;
      const recepientDetails = await Functions.searchUser({
        username: recepient,
      });
      if (!recepientDetails) {
        response.status(400).json({ error: "Recepient not found" });
        return;
      }

      if (id === recepientDetails._id.toString()) {
        response.status(400).json({ error: "Cannot start chat with yourself" });
        return;
      }
      const chatroom = await getChatroom(id, recepientDetails._id.toString());
      console.log("chatroom", chatroom);
      response.status(201).json({
        chatroomID: chatroom._id,
        messages: chatroom.messages,
        recepientID: recepientDetails._id.toString(),
      });
    } else {
      response.status(401).json({ error: "Unauthorized" });
      return;
    }
  },

  async appendMessage(chatroomID, messageData) {
    const chatrooms = await dbClient.chatroomsCollection();

    const message = {
      createdAt: new Date(),
      senderID: new ObjectId(messageData.senderID),
      message: messageData.message,
      recepientID: messageData.recepientID,
    };
    const result = await chatrooms.findOneAndUpdate(
      { _id: new ObjectId(chatroomID) },
      { $push: { messages: message } },
      { returnOriginal: false }
    );
    return result.value;
  },
};

module.exports = MessageController;
