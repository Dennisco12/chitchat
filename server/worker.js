const { ObjectId } = require("mongodb");
const Queue = require("bull");
const UsersController = require("./controllers/UsersController");
const dbClient = require("./engine/db_storage");

const userQueue = new Queue("userQueue", "redis://127.0.0.1:6379");

userQueue.process(async (job, done) => {
  const { userId } = job.data;

  if (!userId) done(new Error("Missing userId"));
  const users = await dbClient.usersCollection();
  const idObject = new ObjectId(userId);
  const user = await users.findOne({ _id: idObject });
  if (user) {
    console.log(`Welcome ${user.email}!`);
    console.log(`Sending otp to ${user.email}!`);
    UsersController.generateOTP(user.email, user.username);
    done();
  } else {
    done(new Error("User not found"));
  }
});

module.exports = userQueue;
