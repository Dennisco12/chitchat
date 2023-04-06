const ObjectID = require("mongodb").ObjectID;
const dbClient = require("../engine/db_storage");
const redisClient = require("../engine/redis");

class UsersController {
  static async getMe(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const userId = await redisClient.get(key);
    if (userId) {
      const users = dbClient.usersCollection();
      const idObject = new ObjectID(userId);
      users.findOne({ _id: idObject }, (err, user) => {
        if (user) {
          response.status(200).json({ id: userId, email: user.email });
        } else {
          response.status(401).json({ error: "Unauthorized" });
        }
      });
    } else {
      response.status(401).json({ error: "Unauthorized" });
    }
  }

  static async deleteUser(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const userId = await redisClient.get(key);

    if (!userId) {
      response.status(401).json({ error: "Unauthorized" });
      return;
    }

    const users = dbClient.usersCollection();
    const idObject = new ObjectID(userId);
    users.deleteOne({ _id: idObject }, (err, result) => {
      if (err) {
        response.status(500).json({ error: "Server error" });
      } else if (result.deletedCount === 0) {
        response.status(404).json({ error: "User not found" });
      } else {
        response.status(204).send();
      }
    });
  }
}

module.exports = UsersController;
