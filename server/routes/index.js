const express = require("express");
const router = express.Router();

const AuthController = require("../controllers/AuthController");
const UsersController = require("../controllers/UsersController");
router.get("/", (req, res) => {
  res.status(200).send("Hi there");
});

router.post("/signup", AuthController.getSignup);

router.get("/users/me", UsersController.getMe);
router.post("/users/checkUsernameExists", UsersController.checkUsernameExists);
router.post("/users/sendOTP", UsersController.sendOTP);

module.exports = router;
