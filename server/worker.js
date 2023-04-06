const dbClient = require("../engine/db_storage");
const { ObjectID } = require("mongodb");
const Queue = require("bull");

const userQueue = new Queue("userQueue", "redis://127.0.0.1:6379");

userQueue.process(async (job, done) => {
  const { userId } = job.data;
  if (!userId) done(new Error("Missing userId"));
  const users = dbClient.usersCollection();
  const idObject = new ObjectID(userId);
  const user = await users.findOne({ _id: idObject });
  if (user) {
    console.log(`Welcome ${user.email}!`);
  } else {
    done(new Error("User not found"));
  }
});
