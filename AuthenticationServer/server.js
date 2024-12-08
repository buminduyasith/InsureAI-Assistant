const express = require("express");

require("dotenv").config();

const app = express();
app.use(express.json());

app.get("/", (req, res) => {
    res.json({
        msg: "hello world"
    });
});

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
