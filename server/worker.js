const { ObjectId } = require("mongodb");
const dbClient = require("./engine/db_storage");
const Mailer = require("./utils/mailer");
const Functions = require("./utils/functions");
const Queue = require("bull");

const userQueue = new Queue("userQueue", "redis://127.0.0.1:6379");

userQueue.process(async (job, done) => {
  const { userId, type } = job.data;

  if (!userId) done(new Error("Missing userId"));
  const users = await dbClient.usersCollection();
  const idObject = new ObjectId(userId);
  const user = await users.findOne({ _id: idObject });
  if (user) {
    console.log(`Welcome ${user.email}!`);
    console.log(`Sending otp to ${user.email}!`);
    if (type === "welcome") {
      Mailer.sendWelcomeEmail(user.email, user.username);
    } else {
      Functions.generateOTP(user.email, user.username, type);
    }
    done();
  } else {
    done(new Error("User not found"));
  }
});

module.exports = userQueue;
