const express = require("express");
const router = express.Router();

const AuthController = require("../controllers/AuthController");
const UsersController = require("../controllers/UsersController");

router.post("/signup", AuthController.getSignup);

router.get("/users/me", UsersController.getMe);
router.post("/users/checkUsernameExists", UsersController.checkUsernameExists);
module.exports = router;
