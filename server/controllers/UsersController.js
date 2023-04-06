const ObjectID = require("mongodb").ObjectID;
const dbClient = require("../engine/db_storage");
const redisClient = require("../engine/redis");
const otpGenerator = require("otp-generator");
const Mailer = require("../utils/mailer");

class UsersController {
  static async getMe(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const userId = await redisClient.get(key);
    if (userId) {
      const users = await dbClient.usersCollection();
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

    const users = await dbClient.usersCollection();
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

  static async checkUsernameExists(request, response) {
    let { username } = request.body;

    const users = await dbClient.usersCollection();
    const existingUser = await users.findOne({ username });
    if (existingUser) {
      response.status(400).json({ error: "Username already exists" });
      return;
    } else {
      response.status(200).json({ error: "Username is avaible" });
      return;
    }
  }

  static async generateOTP(email, username) {
    const otp = otpGenerator.generate(6, {
      upperCaseAlphabets: false,
      specialChars: false,
    });
    const users = await dbClient.usersCollection();
    const result = await users.updateOne(
      { email: email },
      { $set: { otp: otp } }
    );
    if (result.modifiedCount > 0) {
      Mailer.sendOpt(email, username, otp);
      return otp;
    } else {
      return null;
    }
  }

  static async sendOTP(request, response) {
    const { email, username } = request.body;
    if (!email) {
      response.status(400).json({ error: "Email is required" });
      return;
    }

    const opt = this.generateOTP(email, username);
    if (!opt) {
      response.status(400).json({ error: "User not found" });
      return;
    } else {
      response.status(200).json({ error: "Otp sent!" });
      return;
    }
  }

  static async confirmOTP(request, response) {
    let { email, otp } = request.body;
    if (!email || !otp) {
      response.status(400).json({ error: "Email and OTP are required" });
      return;
    }
    const users = await dbClient.usersCollection();
    const user = await users.findOne({ email });
    if (!user) {
      response.status(400).json({ error: "User not found" });
      return;
    }

    const otpData = user.otp;
    if (!otpData || otpData !== otp) {
      response.status(400).json({ error: "Invalid OTP" });
      return;
    }

    await users.updateOne({ email }, { $set: { isVerified: true } });

    response.status(200).json({ message: "OTP confirmed successfully" });
  }
}

module.exports = UsersController;
