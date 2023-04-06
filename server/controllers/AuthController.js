const sha1 = require("sha1");
const { v4: uuidv4 } = require("uuid");
const dbClient = require("../engine/db_storage");
const redisClient = require("../engine/redis");
const userQueue = require("../worker");

const AuthController = {
  async getSignup(request, response) {
    let { email } = request.body;
    let { password } = request.body;
    let { username } = request.body;
    if (!email) {
      response.status(401).json({ error: "Please provide an email address" });
      return;
    }

    if (!password) {
      response.status(401).json({ error: "Please provide a password" });
      return;
    }

    if (!username) {
      response.status(401).json({ error: "Please provide a username" });
      return;
    }

    const users = await dbClient.usersCollection();
    const existingUser = await users.findOne({ username });
    if (existingUser) {
      response.status(400).json({ error: "Username already exists" });
      return;
    }
    const user = await users.findOne({ email });
    if (user) {
      response.status(400).json({ error: "Already exist" });
      return;
    }
    const hashedPassword = sha1(password);
    const insertionInfo = await users.insertOne({
      email,
      password: hashedPassword,
      username,
      isVerified: false,
    });
    const userId = insertionInfo.insertedId.toString();
    const token = uuidv4();
    const key = `auth_${token}`;
    redisClient.set(key, userId, 60 * 60 * 24);
    response.status(201).json({ id: userId, email, token });
    userQueue.add({ userId: userId });
    return;
  },

  async getLogout(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const id = await redisClient.get(key);
    if (id) {
      await redisClient.del(key);
      response.status(204).json({});
    } else {
      response.status(401).json({ error: "Unauthorized" });
    }
  },
};

module.exports = AuthController;
