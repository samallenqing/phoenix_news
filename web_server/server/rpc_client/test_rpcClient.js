var client = require('./rpc_client');
client.add(1, 2, function (res) {
    console.assert(res === 3);
});

client.getNewsSummariesForUser('test', 1, function (response) {
    console.log(response);
    console.assert(response != null);
});

client.logNewsClickForUser('test_user', 'asdfjoqnewponadf');


