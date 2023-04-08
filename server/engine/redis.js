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

  setex(key, value, duration) {
    this.client.set(key, value, "EX", duration, (err, result) => {
      if (err) {
        console.error(err);
      } else {
        console.log("Key set with expiry:", result);
      }
    });
  }

  set(key, value) {
    this.client.set(key, value);
  }

  del(key) {
    return this.client.del(key, (err, result) => {
      if (err) {
        console.log(err);
      } else {
        console.log("Key deleted:", result);
      }
    });
  }

  async delSocketValue(value) {
    for await (const key of this.client.scanIterator()) {
      if (key.startsWith("socket_")) {
        const val = await this.get(key);
        if (val === value) {
          await this.del(key);
          return val;
        }
      }
    }
    return null;
  }
}

const redisClient = new RedisClient();

module.exports = redisClient;
