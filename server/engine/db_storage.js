const { MongoClient } = require("mongodb");

class DBClient {
  constructor() {
    const database = process.env.DB_DATABASE || "chit_chat";
    const uri = process.env.DB_URL;
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
