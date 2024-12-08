const express = require("express");
const authController = require("./controllers/authController")
const tokenController = require("./controllers/tokenController")

require("dotenv").config();

const app = express();

app.use(express.json());
app.use("/auth", authController);
app.use("/token", tokenController);

function notFound(req, res, next) {
    res.status(404);
    const error = new Error("Not Found - " + req.originalUrl);
    next(error);
}

function errorHandler(err, req, res, next) {
    res.status(res.statusCode || 500);
    res.json({
        message: err.message,
        stack: err.stack,
    });
}

app.use(notFound);
app.use(errorHandler);

const port = 8081;
app.listen(port, () => {
    console.log("Listening on port", port);
});
