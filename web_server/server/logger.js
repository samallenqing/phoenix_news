// 'use strict';
const {format, transports, createLogger} = require('winston');
const fs = require('fs');
const env = process.env.NODE_ENV || 'development';
const logDir = 'log';
const {combine, timestamp, prettyPrint, colorize} = format;

// Create the log directory if it does not exist
if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir);
}

const logger = new (createLogger)({
    format: combine(
        timestamp(),
        prettyPrint(),
        colorize()
    ),
    transports: [
        new transports.Console({colorize: true}),
        new (transports.File)({
            filename: `${logDir}/combined.log`,
            level: env === 'development' ? 'debug' : 'info'
        })
        , new transports.File({filename: `${logDir}/error.log`, level: 'error'})
    ],
});

module.exports = logger;