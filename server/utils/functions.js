const otpGenerator = require("otp-generator");
const dbClient = require("../engine/db_storage");
const Mailer = require("./mailer");

const Functions = {
  async generateOTP(email, username, type) {
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
      switch (type) {
        case "sendOtp": {
          Mailer.sendOpt(email, username, otp);
          break;
        }
        case "resetPassword": {
          Mailer.sendResetOpt(email, username, otp);
          break;
        }
      }
      return otp;
    } else {
      return null;
    }
  },

  async searchUser(param) {
    const users = await dbClient.usersCollection();
    return await users.findOne(param);
  },
};

module.exports = Functions;
