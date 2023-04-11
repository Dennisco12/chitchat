const sha1 = require("sha1");
const dbClient = require("../engine/db_storage");
const redisClient = require("../engine/redis");
const { v4: uuidv4 } = require("uuid");
const userQueue = require("../worker");
const Functions = require("../utils/functions");

const AuthController = {
  async getSignup(request, response) {
    console.log("request", request);
    let { email } = request.body;
    let { password } = request.body;
    let { username } = request.body;
    if (!email) {
      response.status(400).json({ error: "Please provide an email address" });
      return;
    }

    if (!password) {
      response.status(400).json({ error: "Please provide a password" });
      return;
    }

    if (!username) {
      response.status(400).json({ error: "Please provide a username" });
      return;
    }

    const users = await dbClient.usersCollection();
    const existingUser = await Functions.searchUser({ username });
    if (existingUser) {
      response.status(400).json({ error: "Username already exists" });
      return;
    }
    const user = await Functions.searchUser({ email });
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
    userQueue.add({ userId: userId, type: "sendOtp" });
    return;
  },

  async getLogout(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const id = await redisClient.get(key);
    if (id) {
      await redisClient.del(key);
      response.status(200).json({});
    } else {
      response.status(401).json({ error: "Unauthorized please login again" });
    }
  },

  async getLogin(request, response) {
    let { identifier } = request.body;
    let { password } = request.body;

    if (!identifier) {
      response
        .status(400)
        .json({ error: "Please provide an email address or username" });
      return;
    }

    if (!password) {
      response.status(400).json({ error: "Please provide a password" });
      return;
    }

    const hashedPassword = sha1(password);
    let user;

    // check if identifier is an email address
    if (identifier.includes("@")) {
      user = await Functions.searchUser({
        email: identifier,
        password: hashedPassword,
      });
    } else {
      // assume identifier is a username
      user = await Functions.searchUser({
        username: identifier,
        password: hashedPassword,
      });
    }

    if (user) {
      if (user.isVerified) {
        const token = uuidv4();
        const key = `auth_${token}`;
        redisClient.setex(key, user._id.toString(), 60 * 60 * 24);
        response.status(201).json({ message: "Login Successful", token, user });
        return;
      } else {
        Functions.generateOTP(user.email, user.username, "sendOtp");
        console.log({
          message: "Verification otp sent to your email",
          username: user.username,
        });
        response
          .status(202)
          .json({ message: "Verification otp sent to your email", user });
      }
    } else {
      response
        .status(400)
        .json({ error: "Email/Username or Password incorrect" });
      return;
    }
  },

  async getResetPassword(request, response) {
    let { identifier } = request.body;
    if (!identifier) {
      response
        .status(401)
        .json({ error: "Please provide an email address or username" });
      return;
    }
    let user;

    if (identifier.includes("@")) {
      user = await Functions.searchUser({
        email: identifier,
      });
    } else {
      // assume identifier is a username
      user = await Functions.searchUser({
        username: identifier,
      });
    }
    response.status(201).json({ message: "Otp sent to your email" });

    userQueue.add({ userId: user._id, type: "resetPassword" });
  },
  async getUpdatePassword(request, response) {
    const { otp, identifier, password } = request.body;
    if (!identifier) {
      response
        .status(401)
        .json({ error: "Please provide an email address or username" });
      return;
    }
    if (!otp) {
      response.status(401).json({ error: "OTP is required" });
      return;
    }
    if (!password) {
      response.status(401).json({ error: "Please provide a new password" });
      return;
    }

    const users = await dbClient.usersCollection();
    let user;

    if (identifier.includes("@")) {
      user = await Functions.searchUser({
        email: identifier,
      });
    } else {
      // assume identifier is a username
      user = await Functions.searchUser({
        username: identifier,
      });
    }
    if (!user) {
      response.status(400).json({ error: "User not found" });
      return;
    }
    const otpData = user.otp;
    if (!otpData || otpData !== otp) {
      response.status(400).json({ error: "Invalid OTP" });
      return;
    }
    const hashedPassword = sha1(password);

    if (identifier.includes("@")) {
      await users.updateOne(
        { email: identifier },
        { $set: { password: hashedPassword }, $unset: { otp: "" } }
      );
    } else {
      await users.updateOne(
        { username: identifier },
        { $set: { password: hashedPassword }, $unset: { otp: "" } }
      );
    }
    await redisClient.del(user._id);
    response.status(201).json({ message: "Password updated successfully" });
  },
};

module.exports = AuthController;
