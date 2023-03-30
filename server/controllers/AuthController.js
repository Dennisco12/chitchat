/**
 * Contains the miscellaneous route handlers.
 */

const AuthController = {
  getHomepage(request, response) {
    response.status(200).send("Hello Welcome!");
  },
};

module.exports = AuthController;
