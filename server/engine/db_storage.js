const { MongoClient } = require("mongodb");

class DBClient {
  constructor() {
    const host = process.env.DB_HOST || "localhost";
    const port = process.env.DB_PORT || 27017;
    const database = process.env.DB_DATABASE || "chit_chat";
    const uri = `mongodb://${host}:${port}/${database}`;
    this.client = new MongoClient(uri, {
      useUnifiedTopology: true,
      useNewUrlParser: true,
    });

    this.client.connect().catch((err) => {
      console.log(err);
    });
  }

  async isAlive() {
    return this.client.isConnected();
  }

  async nbUsers() {
    try {
      const users = this.usersCollection();
      const count = await users.countDocuments();
      return count;
    } catch (error) {
      return -1;
    }
  }

  async usersCollection() {
    return this.client.db().collection("users");
  }
}

const dbClient = new DBClient();
module.exports = dbClient;
