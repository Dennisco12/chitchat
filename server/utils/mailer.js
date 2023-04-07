const nodemailer = require("nodemailer");
const Mail = require("nodemailer/lib/mailer");

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
                  Hello there ${username ?? ""},
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
  welcome(username) {
    return `<!DOCTYPE html>
    <html>
      <head>
        <title>Welcome to ChitChat!</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <table
          cellpadding="0"
          cellspacing="0"
          border="0"
          align="center"
          width="600"
          style="max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; border-collapse: collapse; background-color: #f5f5f5;"
        >
          <tr>
            <td
              style="text-align: center; padding: 20px; background-color: #ffffff; border-radius: 10px;"
            >
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
                Welcome to ChitChat
              </div>
              <p style="font-size: 18px; line-height: 1.5;">
                Hi ${username},<br />
                We're thrilled to have you join us here at ChitChat! You're now part
                of a global community of people who share your love for chatting and
                making new friends.
              </p>
              <p style="font-size: 18px; line-height: 1.5;">
                To get started, just log in to your account and start exploring! If
                you have any questions or feedback, feel free to reach out to our
                support team at chitchatcli@gmail.com.
              </p>
              <p style="font-size: 18px; line-height: 1.5;">
                Thanks for choosing ChitChat, and happy chatting!
              </p>
            </td>
          </tr>
          <tr>
            <td
              style="text-align: center; padding: 20px; background-color: #ffffff; border-radius: 10px;"
            >
              <p style="font-size: 16px;">
                If you didn't create an account with ChitChat, please disregard
                this email.
              </p>
            </td>
          </tr>
        </table>
      </body>
    </html>
    
    `;
  },
  resetpassword(code, username) {
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
           Reset Password
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
              Hello there ${username ?? ""},
            </p>
            <p
              style="
                font-size: 16px;
                line-height: 1.5;
                margin-bottom: 20px;
                text-align: center;
              "
            >
            You recently requested to reset your password for your ChitChat account. Use the following OTP to reset your password:
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
              This OTP will expire in 30 minutes. If you did not request this OTP,
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
    </html>  `;
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
  sendResetOpt(to, username, otp) {
    const mailOptions = {
      from: {
        name: "Chit Chat",
        address: "chitchatcli@gmail.com",
      },
      to,
      subject: "Reset ChitChat Password",
      html: HTMLTemp.resetpassword(otp, username),
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
  sendWelcomeEmail(to, username) {
    const mailOptions = {
      from: {
        name: "Chit Chat",
        address: "chitchatcli@gmail.com",
      },
      to,
      subject: "Welcome to ChitChat",
      html: HTMLTemp.welcome(username),
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
