const { ObjectId } = require("mongodb");
const dbClient = require("../engine/db_storage");
const redisClient = require("../engine/redis");
const otpGenerator = require("otp-generator");
const Mailer = require("../utils/mailer");
const { v4: uuidv4 } = require("uuid");
const userQueue = require("../worker");
const Functions = require("../utils/functions");

class UsersController {
  static async getMe(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const userId = await redisClient.get(key);
    if (userId) {
      const idObject = new ObjectId(userId);
      const user = await Functions.searchUser({ _id: idObject });
      if (user) {
        response.status(201).json({ id: userId, user: user });
      } else {
        response.status(401).json({ error: "User not found" });
      }
    } else {
      response.status(401).json({ error: "Unauthorized" });
    }
  }

  static async editProfile(request, response) {
    const updates = request.body;
    const token = request.header("X-Token");
    const key = `auth_${token}`;

    const userId = await redisClient.get(key);

    if (userId) {
      if (!updates) {
        response.status(400).json({ error: "No items passed" });
        return;
      }
      try {
        const users = await dbClient.usersCollection();
        const idObject = new ObjectId(userId);
        const result = await users.updateOne(
          { _id: idObject },
          { $set: { profileDetails: updates } }
        );

        if (result.modifiedCount === 1) {
          response
            .status(201)
            .json({ success: true, message: "Profile updated successfully" });
        } else {
          response.status(400).json({ error: "User not found" });
        }
      } catch (error) {
        response.status(500).json({ error: error.message });
      }
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

    const existingUser = await Functions.searchUser({ username });
    if (existingUser) {
      response.status(400).json({ error: "Username already exists" });
      return;
    } else {
      response.status(201).json({ message: "Username is avaible" });
      return;
    }
  }

  static async sendOTP(request, response) {
    const { email, username } = request.body;
    if (!email) {
      response.status(400).json({ error: "Email is required" });
      return;
    }

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
      response.status(201).json({ message: "Otp sent!" });

      return;
    } else {
      response.status(400).json({ error: "User not found" });

      return null;
    }
  }

  static async confirmOTP(request, response) {
    let { identifier, otp } = request.body;
    if (!identifier || !otp) {
      response
        .status(400)
        .json({ error: "Email/Username and OTP are required" });
      return;
    }
    const users = await dbClient.usersCollection();
    let user;
    if (identifier.includes("@")) {
      user = await Functions.searchUser({ email: identifier });
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

    if (identifier.includes("@")) {
      await users.updateOne(
        { email: identifier },
        { $set: { isVerified: true }, $unset: { otp: "" } }
      );
    } else {
      await users.updateOne(
        { username: identifier },
        { $set: { isVerified: true }, $unset: { otp: "" } }
      );
    }

    const token = uuidv4();
    const key = `auth_${token}`;
    redisClient.setex(key, user._id.toString(), 60 * 60 * 24);

    response
      .status(201)
      .json({ message: "OTP confirmed successfully", token, user });
    userQueue.add({ userId: user._id, type: "welcome" });
    return;
  }
  static async getFriends(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const userId = await redisClient.get(key);
    if (userId) {
      const users = await dbClient.usersCollection();
      const idObject = new ObjectId(userId);
      const user = await Functions.searchUser({ _id: idObject });
      if (user) {
        const friendIds = user.friendlist || [];
        const friends = await users
          .find({ _id: { $in: friendIds.map((id) => ObjectId(id)) } })
          .toArray();
        response.status(201).json({ friends });
      } else {
        response.status(401).json({ error: "User not found" });
      }
    } else {
      response.status(401).json({ error: "Unauthorized" });
    }
  }
}

module.exports = UsersController;
