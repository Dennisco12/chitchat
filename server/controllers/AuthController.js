const sha1 = require("sha1");
const { v4: uuidv4 } = require("uuid");
const dbClient = require("../engine/db_storage");
const redisClient = require("../engine/redis");
const Queue = require("bull");

const userQueue = new Queue("userQueue", "redis://127.0.0.1:6379");

const AuthController = {
  async getSignup(request, response) {
    let { email } = request.body;
    let { password } = request.body;

    if (!email) {
      response.status(401).json({ error: "Please provide an email address" });
      return;
    }

    if (!password) {
      response.status(401).json({ error: "Please provide a password" });
      return;
    }
    const users = dbClient.usersCollection();

    users.findOne({ email }, (err, user) => {
      if (user) {
        response.status(400).json({ error: "Already exist" });
      } else {
        const hashedPassword = sha1(password);
        users
          .insertOne({
            email,
            password: hashedPassword,
          })
          .then(async (result) => {
            const token = uuidv4();
            const key = `auth_${token}`;
            await redisClient.set(
              key,
              result.insertedId.toString(),
              60 * 60 * 24
            );
            userQueue.add({ userId: result.insertedId });
            response.status(201).json({ id: result.insertedId, email, token });
          })
          .catch((error) => console.log(error));
      }
    });
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
