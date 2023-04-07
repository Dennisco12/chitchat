const redis = require("redis");

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

  get(key) {
    return this.client.get(key, (err, result) => {
      if (err) {
        console.log(err);
      }
    });
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

  del(key) {
    return new Promise((resolve, reject) => {
      this.client.del(key, (err, result) => {
        if (err) {
          reject(err);
        } else {
          console.log("Key deleted:", result);
          resolve(result);
        }
      });
    });
  }
}

const redisClient = new RedisClient();

module.exports = redisClient;
