const AuthController = require("../controllers/AuthController");
/**
 * Binds the routes to the appropriate handler in the
 * given Express application.
 * @param {Express} app The Express application.
 */

const authRoutes = (app) => {
  app.get("/", AuthController.getHomepage);
};

module.exports = authRoutes;
