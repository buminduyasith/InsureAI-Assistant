const express = require("express");
const cors = require("cors"); 
const authController = require("./controllers/authController")
const tokenController = require("./controllers/tokenController")
const bcrypt = require("bcrypt");

require("dotenv").config();

const app = express();

app.use(cors({
    origin: "http://localhost:3000", // Allow requests from port 3000
    methods: ["GET", "POST", "PUT", "DELETE", "PATCH"], // Allow these HTTP methods
}));

app.use(express.json());

app.get("/", async (req, res) => {
    var hash = await bcrypt.hashSync("egege@eE23", 10)
    res.status(200).json({hash});
})
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
