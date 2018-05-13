const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config/config.json');


module.exports = (req, res, next) => {
    console.log('auth_checker: req: ' + req.headers);

    if (!req.headers.authorization) {
        return res.status(401).end();
    }

    const token = req.headers.authorization.split(' ')[1];

    console.log('auth_checker: token: ' + token);

    return jwt.verify(token, config.jwtSecret, (err, decoded) => {
        if (err) {
            return res.status(402).end();
        }

        const id = decoded.sub;

        return User.findById(id, (userErr, user) => {
            if (userErr || !user) {
                return res.status(403).end();
            }

            return next();
        });
    });
};