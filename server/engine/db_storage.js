const { MongoClient } = require("mongodb");

class DBClient {
  constructor() {
    const host = process.env.DB_HOST || "localhost";
    const port = process.env.DB_PORT || 27017;
    const database = process.env.DB_DATABASE || "chit_chat";
    const uri =
      "mongodb+srv://chit_chatuser:5wOV4K083ZdGYfdM@cluster0.iy1lmun.mongodb.net/chit_chat?retryWrites=true&w=majority";
    this.client = new MongoClient(uri, {
      useUnifiedTopology: true,
    });

    this.client
      .connect()
      .then(() => {
        this.db = this.client.db(`${database}`);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  async usersCollection() {
    return this.client.db().collection("users");
  }

  async chatroomsCollection() {
    return this.client.db().collection("chatrooms");
  }
}

const dbClient = new DBClient();
module.exports = dbClient;
