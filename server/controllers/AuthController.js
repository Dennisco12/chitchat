const sha1 = require("sha1");
const dbClient = require("../engine/db_storage");
const redisClient = require("../engine/redis");
const userQueue = require("../worker");
const { v4: uuidv4 } = require("uuid");
const UsersController = require("./UsersController");

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

    response.status(201).json({ id: userId, email });
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

  async getLogin(request, response) {
    let { identifier } = request.body;
    let { password } = request.body;

    if (!identifier) {
      response
        .status(401)
        .json({ error: "Please provide an email address or username" });
      return;
    }

    if (!password) {
      response.status(401).json({ error: "Please provide a password" });
      return;
    }

    const hashedPassword = sha1(password);
    const users = await dbClient.usersCollection();

    let user;

    // check if identifier is an email address
    if (identifier.includes("@")) {
      user = await users.findOne({
        email: identifier,
        password: hashedPassword,
      });
    } else {
      // assume identifier is a username
      user = await users.findOne({
        username: identifier,
        password: hashedPassword,
      });
    }

    if (user) {
      if (user.isVerified) {
        const token = uuidv4();
        const key = `auth_${token}`;
        redisClient.set(key, user._id.toString(), 60 * 60 * 24);
        response.status(200).json({ message: "Login Successful", token, user });
        return;
      } else {
        UsersController.generateOTP(user.email, user.username);
        response
          .status(202)
          .json({ message: "Verification otp sent to your email" });
      }
    } else {
      response
        .status(400)
        .json({ error: "Email/Username or Password incorrect" });
      return;
    }
  },
};

module.exports = AuthController;
