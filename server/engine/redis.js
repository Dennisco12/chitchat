const redis = require("redis");
const { promisify } = require("util");

class RedisClient {
  constructor() {
    this.init();
  }

  async init() {
    this.client = redis.createClient();
    await this.client.connect();
    this.client.on("error", (err) => {
      console.error("Redis error:", err);
    });
  }

  async get(key) {
    return promisify(this.client.GET).bind(this.client)(key);
  }

  set(key, value, duration) {
    this.client.set(key, value, "EX", duration, (err, result) => {
      if (err) {
        console.error(err);
      } else {
        console.log("Key set with expiry:", result);
      }
    });
  }

  async del(key) {
    await promisify(this.client.DEL).bind(this.client)(key);
  }
}

const redisClient = new RedisClient();

module.exports = redisClient;
