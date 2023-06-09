const { ObjectId } = require("mongodb");
const dbClient = require("../engine/db_storage");
const redisClient = require("../engine/redis");
const otpGenerator = require("otp-generator");
const Mailer = require("../utils/mailer");
const { v4: uuidv4 } = require("uuid");
const { userQueue } = require("../worker");
const Functions = require("../utils/functions");

class UsersController {
  static async searchUsers(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const id = await redisClient.get(key);
    if (id) {
      const { term } = request.body;
      console.log("Searching for", term);
      if (!term) {
        return response.status(400).json({ error: "Search term is required" });
      }
      const users = await dbClient.usersCollection();
      const terms = term.split(" ");
      const query = {
        profileDetails: { $exists: true, $ne: {} },
        $or: [
          { username: { $regex: terms.join("|"), $options: "i" } },
          { email: { $regex: terms.join("|"), $options: "i" } },
          {
            "profileDetails.firstName": {
              $regex: terms.join("|"),
              $options: "i",
            },
          },
          {
            "profileDetails.lastName": {
              $regex: terms.join("|"),
              $options: "i",
            },
          },
          { "profileDetails.bio": { $regex: terms.join("|"), $options: "i" } },
          {
            "profileDetails.techStack": {
              $regex: terms.join("|"),
              $options: "i",
            },
          },
          {
            "profileDetails.level": { $regex: terms.join("|"), $options: "i" },
          },
        ],
      };
      try {
        const results = await users.find(query).toArray();
        console.log("results", results);
        const usersFound = results.map(
          ({ password, otp, isVerified, ...rest }) => rest
        );
        response.status(201).json(usersFound);
      } catch (err) {
        console.error(err);
        response.status(500).json({ error: "Internal server error" });
      }
    } else {
      response.status(401).json({ error: "Unauthorized please login again" });
      return;
    }
  }
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
      response.status(401).json({ error: "Unauthorized please login again" });
    }
  }
  static async getUser(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const userId = await redisClient.get(key);
    if (userId) {
      const { username } = request.params;

      const user = await Functions.searchUser({ username });
      if (user) {
        response.status(201).json({ id: userId, user: user });
      } else {
        response.status(401).json({ error: "User not found" });
      }
    } else {
      response.status(401).json({ error: "Unauthorized please login again" });
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
        const user = await users.findOne({ _id: idObject });
        const profileDetails = user?.profileDetails ?? {};
        const result = await users.updateOne(
          { _id: idObject },
          { $set: { profileDetails: { ...profileDetails, ...updates } } }
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
      response.status(401).json({ error: "Unauthorized please login again" });
    }
  }

  static async deleteUser(request, response) {
    const token = request.header("X-Token");
    const key = `auth_${token}`;
    const userId = await redisClient.get(key);

    if (!userId) {
      response.status(401).json({ error: "Unauthorized please login again" });
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
      response.status(401).json({ error: "Unauthorized please login again" });
    }
  }
}

module.exports = UsersController;
