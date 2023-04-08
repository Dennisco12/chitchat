const express = require("express");
const router = express.Router();

const AuthController = require("../controllers/AuthController");
const UsersController = require("../controllers/UsersController");
const MessageController = require("../controllers/MessageController");

router.get("/", (req, res) => {
  res.status(201).send("Hi there");
});

router.post("/signup", AuthController.getSignup);
router.post("/login", AuthController.getLogin);
router.post("/resetPassword", AuthController.getResetPassword);
router.put("/resetPassword", AuthController.getUpdatePassword);
router.get("/users/me", UsersController.getMe);
router.get("/users/friends", UsersController.getFriends);
router.post("/users/checkUsernameExists", UsersController.checkUsernameExists);
router.post("/users/sendOTP", UsersController.sendOTP);
router.post("/users/confirmOTP", UsersController.confirmOTP);
router.put("/users/editProfile", UsersController.editProfile);
router.get("/startChat/:recepient", MessageController.startChat);
router.get("/users/search/:term", UsersController.searchUsers);

module.exports = router;
