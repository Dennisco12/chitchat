const nodemailer = require("nodemailer");

const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: "chitchatcli@gmail.com",
    pass: "hvmbtqhsadzhdrae",
  },
});
const HTMLTemp = {
  otp(code, username) {
    return `<!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>ChitChat OTP Verification</title>
          </head>
          <body style="background-color: #f6f6f6; font-family: Arial, sans-serif;">
            <div
              style="
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
              "
            >
              <!-- Header -->
              <div
                style="
                  background-color: #fc6c85;
                  color: #ffffff;
                  font-size: 28px;
                  font-weight: bold;
                  text-align: center;
                  padding: 40px;
                "
              >
                ChitChat OTP Verification
              </div>
        
              <!-- Body -->
              <div style="padding: 40px;">
                <p
                  style="
                    font-size: 18px;
                    line-height: 1.5;
                    margin-bottom: 20px;
                    text-align: center;
                  "
                >
                  Hello there ${username},
                </p>
                <p
                  style="
                    font-size: 16px;
                    line-height: 1.5;
                    margin-bottom: 20px;
                    text-align: center;
                  "
                >
                  Here is your OTP to verify your ChitChat account:
                </p>
                <div
                  style="
                    background-color: #fc6c85;
                    color: #ffffff;
                    font-size: 32px;
                    font-weight: bold;
                    text-align: center;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                  "
                >
                  ${code}
                </div>
                <p
                  style="
                    font-size: 16px;
                    line-height: 1.5;
                    margin-bottom: 20px;
                    text-align: center;
                  "
                >
                  This OTP will expire in 5 minutes. If you did not request this OTP,
                  please ignore this email.
                </p>
              </div>
        
              <!-- Footer -->
              <div
                style="
                  background-color: #fc6c85;
                  color: #ffffff;
                  font-size: 14px;
                  text-align: center;
                  padding: 20px;
                "
              >
                © ChitChat 2023. All Rights Reserved.
              </div>
            </div>
          </body>
        </html>        
        `;
  },
};

const Mailer = {
  sendOpt(to, username, otp) {
    const mailOptions = {
      from: {
        name: "Chit Chat",
        address: "chitchatcli@gmail.com",
      },
      to,
      subject: "Chit Chat Otp Verification",
      html: HTMLTemp.otp(otp, username),
    };

    try {
      transporter.sendMail(mailOptions, (err, info) => {
        if (err) {
          console.log(err);
        }
      });
    } catch (err) {
      console.log(err);
    }
  },
};

module.exports = Mailer;
