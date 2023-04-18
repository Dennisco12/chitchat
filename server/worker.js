const { ObjectId } = require("mongodb");
const dbClient = require("./engine/db_storage");
const Mailer = require("./utils/mailer");
const Functions = require("./utils/functions");
const Queue = require("bull");

const userQueue = new Queue("userQueue", process.env.REDIS_URL);

userQueue.process(async (job, done) => {
  const { userId, type } = job.data;

  if (!userId) done(new Error("Missing userId"));
  const idObject = new ObjectId(userId);
  const user = await Functions.searchUser({ _id: idObject });
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
