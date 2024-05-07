//
// server.js -- Server-side code written in Node.js
//
require("dotenv").config();

const multer = require("multer");
const express = require("express");
const http = require("http");
const axios = require("axios");
const socketIo = require("socket.io");
const cors = require("cors");
const amqp = require("amqplib");
const fs = require("fs-extra");
const path = require("path");
const winston = require("winston");
const mongoose = require('mongoose');
require("winston-syslog").Syslog;
const teamRoutes = require('./routes/teamRoutes');
const profileRoutes = require('./routes/profileRoutes');
const roleRoutes = require('./routes/roleRoutes');

const baseURL = process.env.PYTHON_SERVICE_URL || "http://127.0.0.1:8000";
const uploadDir = process.env.STORAGE_DIR + "/uploads";
const amqpDomain = process.env.AMQP_DOMAIN || "localhost";
const amqpPort = process.env.AMQP_PORT || "5672";
const amqpUsername = process.env.RABBITMQ_USER || "guest";
const amqpPassword = process.env.RABBITMQ_PASS || "guest";
const corsOrigin = process.env.CORS_ORIGIN || "http://localhost:5000";
const amqpURL = `amqp://${amqpUsername}:${amqpPassword}@${amqpDomain}:${amqpPort}/%2F`;
const nodeJsPort = 4000;
const dbUri = 'mongodb://127.0.0.1:27017/r1n_framework';



// Configure the logger
const logger = winston.createLogger({
    level: "info", // or whatever level you need
    format: winston.format.combine(
        winston.format.timestamp({
            format: "YYYY-MM-DD HH:mm:ss",
        }),
        winston.format.printf(
            (info) => `${info.timestamp} ${info.level.toUpperCase()}: ${info.message}`
        )
    ),
    transports: [
        new winston.transports.Console(),
        new winston.transports.Syslog({
            host: "logs3.papertrailapp.com",
            port: 23803,
            protocol: "udp4",
            localhost: "server.js", // Optional: identify your app in logs
            app_name: "Server", // Optional: a more formal app name
            eol: "\n",
        }),
    ],
});

logger.info("==== server.js started ====");

logger.info(`Configuration details:`);
logger.info(
    JSON.stringify({
        baseURL: baseURL,
        uploadDir: uploadDir,
        amqpDomain: amqpDomain,
        amqpPort: amqpPort,
        amqpUsername: amqpUsername,
        amqpURL: amqpURL,
        corsOrigin: corsOrigin,
        nodeJsPort: nodeJsPort,
        cwd: process.cwd(),
    })
);

// Connect to MongoDB
mongoose.connect(dbUri)
  .then(() => logger.info('MongoDB connected successfully.'))
  .catch(err => logger.error('MongoDB connection error:', err));

// Create an Express app
const app = express();
app.use(cors()); // Enable CORS for all routes
app.use(express.json()); // For parsing application/json
app.use('/api', teamRoutes);
app.use('/api', profileRoutes);
app.use('/api', roleRoutes);

let channel = null; // Global variable to hold the RabbitMQ channel

// Create an HTTP server and attach the Express app to it
const server = http.createServer(app);

// Create a Socket.IO server and attach it to the HTTP server
const io = socketIo(server, {
    cors: {
        origin: corsOrigin,
        methods: ["GET", "POST"],
    },
});

// Configure multer storage
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, uploadDir + "/");
    },
    filename: function (req, file, cb) {
        const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
        cb(
            null,
            file.fieldname + "-" + uniqueSuffix + path.extname(file.originalname)
        );
    },
});

// Create a multer instance with the storage configuration
const upload = multer({ storage: storage });



// Create cleanup features for graceful shutdown
function cleanup() {
    logger.info("Cleaning up before shutdown...");
    
    // dismiss the team
    dismissTeam();
    
    // TODO: This is lazy and should be improved
    // Introduce a delay of 2000 milliseconds (3 seconds) before continuing
    setTimeout(() => {
        process.exit(0);
    }, 3000); // 3000 milliseconds delay
}

// Handle Node.js shutdown signals:
process.on("SIGINT", () => {
    logger.info("Received SIGINT (Ctrl+C).");
    cleanup();
});

process.on("SIGTERM", () => {
    logger.info("Received SIGTERM from the system.");
    cleanup();
});

process.on("exit", (code) => {
    logger.info("Node.js process exiting with code: {code}", code);
    // Cleanup has already been triggered by SIGINT or SIGTERM handlers if needed
});

function dismissTeam() {
    logger.info("Dismissing team...");
    
    const to_exchange = "broadcast_queue";
    
    // Define the message
    const message = JSON.stringify({
        from_name: "User Interface",
        from_queue: "user_interface",
        to_name: "Every Agent",
        to_queue: to_exchange,
        cc_queue: "",
        message_type: "team.dismiss",
        content: "",
        message_timestamp: Date.now(),
    });
    
    // Ensure channel is available
    if (!channel) {
        logger.error("Failed to dismiss team: RabbitMQ channel not established");
        throw new Error("RabbitMQ channel not established");
    }
    
    logger.info("Sending presence ping to all agents");
    logger.info(message);
    
    // Publish the message to the broadcast_queue exchange
    const routing_key = ""; // Routing key (empty string for fanout exchanges)
    
    try {
        // Check to see if the exchange exists. If not, create it.
        channel.assertExchange(to_exchange, "fanout", { durable: false });
        
        // Actual message publishing
        channel.publish(to_exchange, routing_key, Buffer.from(message), {
            persistent: true, // Optional: if you want the message to be persistent
        });
        
        logger.info("Message sent to broadcast_queue successfully");
    } catch (error) {
        logger.error("Failed to send message on RabbitMQ", {
            error: error.message,
            stack: error.stack,
            to_exchange,
            message,
        });
        throw error; // Re-throw the error after logging it
    }
}

// ======================== Middleware ========================

function ensureJson(req, res, next) {
    if (req.headers["content-type"] !== "application/json") {
        return res
        .status(400)
        .json({ message: "Bad request: Content-Type must be application/json" });
    }
    next();
}

// ======================== API Endpoints ========================


//
// Retrieve messages from the frontend and send them to RabbitMQ
//

app.post("/send-message", ensureJson, async (req, res) => {
    logger.info("/send-message received POST");
    logger.info(JSON.stringify(req.body));
    
    if (!channel) {
        logger.error("RabbitMQ channel not established");
        return res
        .status(500)
        .json({ message: "RabbitMQ channel not established" });
    }
    
    const {
        from_name,
        from_queue,
        from_persona,
        to_name,
        to_queue,
        to_persona,
        cc_queue,
        content,
        message_type,
        timestamp,
    } = req.body;
    
    try {
        const msg = JSON.stringify({
            from_name,
            from_queue,
            from_persona,
            to_name,
            to_queue,
            to_persona,
            cc_queue,
            content,
            message_type,
            timestamp,
        });
        channel.sendToQueue(to_queue, Buffer.from(msg));
        res.json({ message: "Message sent to RabbitMQ" });
    } catch (error) {
        logger.error("Error sending message to RabbitMQ:", {
            error: error.toString(),
            stack: error.stack,
        });
        res.status(500).json({
            message: "Error sending message to RabbitMQ (to queue: " + to_queue + ")",
        });
    }
});

app.post("/team/dismiss", async (req, res) => {
    try {
        dismissTeam();
        res.status(200).json({ message: "OK" });
    } catch (error) {
        logger.error(
            "server.js::/team-dismiss - Error sending message to broadcast_queue",
            JSON.stringify(error, Object.getOwnPropertyNames(error))
        );
        res.status(500).json({ error: "Internal server error" });
    }
});

app.post("/team/:uuid/launch", async (req, res) => {
    const teamUuid = req.params.uuid;
    const url = `${baseURL}/launch/${teamUuid}`;
    
    try {
        const response = await axios.post(url, {
            tile: false, // or pass any other needed data
        });
        
        // Handle response from the Flask service
        logger.info(`Response from POST ${url}: `);
        logger.info(JSON.stringify(response.data));
        
        res.status(200).json({
            message: "Team launch initiated successfully",
            details: response.data,
        });
    } catch (error) {
        logger.error("Unable to launch team");
        logger.error("URL: " + url);
        logger.error("Error: " + error);
        res.status(500).json({
            error: "Internal server error",
            details: error.message,
        });
    }
});

app.post("/ui-ready", async (req, res) => {
    try {
        to_exchange = "broadcast_queue";
        
        // Define the message
        const message = JSON.stringify({
            from_name: "User Interface",
            from_queue: "user_interface",
            to_name: "Every Agent",
            to_queue: to_exchange,
            cc_queue: "",
            message_type: "ui.ready",
            content: "",
            message_timestamp: Date.now(),
        });
        
        // Ensure channel is available
        if (!channel) {
            logger.info("RabbitMQ channel not established");
            throw new Error("RabbitMQ channel not established");
        }
        
        logger.info("sending presence ping to all agents");
        logger.info(message);
        
        // Publish the message to the broadcast_queue exchange
        routing_key = ""; // Routing key (empty string for fanout exchanges)
        
        // Check to see if the exchange exists.  If not, create it.
        channel.assertExchange(to_exchange, "fanout", { durable: false });
        
        channel.publish(to_exchange, routing_key, Buffer.from(message), {
            persistent: true, // Optional: if you want the message to be persistent
        });
        
        res.status(200).json({ message: "OK" });
    } catch (error) {
        logger.error(
            "server.js in /ui-ready - Error sending message to broadcast_queue"
        );
        res.status(500).json({ error: "Internal server error" });
    }
});

app.post("/upload", upload.single("file"), async (req, res) => {

    logger.info("POST /upload received");

    if (!req.file) {
        return res.status(400).send({ message: "No file uploaded." });
    }
    
    // get the agent uuid from the request
    const agent_uuid = req.body.agent_uuid;
    const agent_name = req.body.agent_name;
    const agent_queue = req.body.agent_queue;
    const context = req.body.context;
    
    const file_path = req.file.path;
    const file_name = path.basename(file_path);

    const payload_json_string = JSON.stringify({
        file_path: req.file.path,
        file_name: file_name,
        original_file_name: req.file.originalname,
        file_size: req.file.size,
        agent_uuid: agent_uuid,
        agent_name: agent_name,
        context: context
    });
    
    // Using the rabbitMQ message bus, send a message to the agent to process the file
    const message = JSON.stringify({
        from_name: "User Interface",
        from_queue: "user_interface",
        to_name: agent_name,
        to_queue: agent_queue,
        cc_queue: "",
        message_type: "file.upload",
        content: payload_json_string,
        message_timestamp: Date.now(),
    });
    
    // logger.info uploaded file and notified {agent}[{agent_uuid}]
    logger.info(`Notifying ${agent_name}[${agent_queue}] about the uploaded file ${req.file.path}`);
    logger.info(`message: ${message}`);
    
    try {
        // Ensure channel is available
        if (!channel) {
            logger.info("RabbitMQ channel not established");
            throw new Error("RabbitMQ channel not established");
        }
        
        // Publish the message to the agent's queue
        channel.sendToQueue(agent_queue, Buffer.from(message));
        
        res.status(200).send({ message: "File uploaded successfully" });
    } catch (error) {
        logger.error("Error sending message to RabbitMQ:");
        res.status(500).send({ message: "Error sending message to RabbitMQ" });
    }
});

app.post("/api/teams", async (req, res) => {

});

// ======================== Socket.IO and RabbitMQ ========================

// Socket.IO connection
io.on("connection", (socket) => {
    logger.info("New client connected");
    socket.on("disconnect", () => {
        logger.info("Client disconnected");
    });
});

async function waitForRabbitMQ() {
    let attempts = 0;
    const maxAttempts = 7000; // Maximum number of connection attempts
    const delay = 4000; // Delay in milliseconds between each attempt
    
    while (true) {
        try {
            logger.info(
                `Attempting to connect to RabbitMQ on domain ${amqpDomain}, port ${amqpPort} (Attempt ${
                    attempts + 1
                }/${maxAttempts})...`
            );
            const connection = await amqp.connect(amqpURL); // Use the existing amqpURL variable
            logger.info("Successfully connected to RabbitMQ!");
            await connection.close();
            return; // Exit the function once connection is successful
        } catch (error) {
            attempts++;
            if (attempts >= maxAttempts) {
                logger.error("Unable to connect to RabbitMQ after maximum attempts.");
                throw new Error("Failed to connect to RabbitMQ"); // Throw an error to be caught by the caller
            }
            logger.info(`Waiting for ${delay / 1000} seconds before next attempt...`);
            await new Promise((resolve) => setTimeout(resolve, delay)); // Wait before the next attempt
        }
    }
}

// RabbitMQ setup
async function startRabbitMQ() {
    try {
        await waitForRabbitMQ(); // Ensure RabbitMQ is ready before proceeding
        
        logger.info("Attempting to connect to RabbitMQ on URL: " + amqpURL);
        const connection = await amqp.connect(amqpURL);
        
        if (!connection) {
            throw new Error("Failed to connect to RabbitMQ");
        }
        logger.info("Connected to RabbitMQ");
        
        // This "channel" is a global variable
        channel = await connection.createChannel();
        if (!channel) {
            throw new Error("Failed to create RabbitMQ channel");
        }
        logger.info("Created RabbitMQ channel");
        
        const queue = "user_interface";
        await channel.assertQueue(queue, { durable: false });
        logger.info(`Waiting for messages in ${queue}. To exit press CTRL+C`);
        
        // Consume messages from RabbitMQ
        // Then emit the messages to all connected Socket.IO clients
        
        channel.consume(queue, (msg) => {
            if (msg) {
                const msg_content = msg.content;
                const messageStr = msg.content.toString();
                logger.info(
                    `server.js::channel.consume - Received message from queue: ${queue}`,
                    { msg_content }
                );
                io.emit("FromServer", messageStr);
            } else {
                logger.info(
                    `server.js::channel.consume - Received null message from queue: ${queue}`
                );
            }
            channel.ack(msg);
        });
    } catch (error) {
        logger.error("Error in RabbitMQ connection:", error);
        process.exit(1);
    }
}

async function startServer() {
    try {
        await startRabbitMQ(); // Wait for RabbitMQ setup to complete
        server.listen(nodeJsPort, () => {
            logger.info(`Node.js server running on port ${nodeJsPort}`);
        });
    } catch (error) {
        logger.error("Failed to start the server");
    }
}

startServer();
