const express = require("express");
const router = express.Router();

const AuthController = require("../controllers/AuthController");
const UsersController = require("../controllers/UsersController");

router.post("/signup", AuthController.getSignup);

router.get("/users/me", UsersController.getMe);

module.exports = router;
