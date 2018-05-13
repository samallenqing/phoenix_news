var express = require('express');
var rpc_client = require('../rpc_client/rpc_client');
var router = express.Router();
var logger = require('../logger');

/* GET news list. */
router.get('/userId=:userId&pageNum=:pageNum', function (req, res, next) {
    console.log('Fetching news');
    let user_id = req.params['userId'];
    let page_num = req.params['pageNum'];
    logger.info('User: ' + user_id + ' required new news. Current page: ' + page_num);
    rpc_client.getNewsSummariesForUser(user_id, page_num, function (response) {
        res.json(response);
    })
});

router.post('/userId=:userId&newsId=:newsId', function (req, res, next) {
    console.log("Logging news click...");
    let user_id = req.params['userId'];
    let news_id = req.params['newsId'];
    rpc_client.logNewsClickForUser(user_id, news_id);
    res.status(200)
});

module.exports = router;