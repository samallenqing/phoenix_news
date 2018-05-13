# Phoenix News Recommendation System
- Frontend Service: Provide user interface.
- Backend Service: Process user requests, retrieve data from database, provide log info to log service.
- TensorFlow Service: Offline train data, provide online model serving, backfill latest fetched news.
- News Service:
- News Crawler: Fetching latest news from websites.
- News Fetcher: Getting latest news abstract info and send to News Crawler.
- News Deduper: Use tf-idf dedupe crawled news and save into database.
- Click log Service: Process user click information, build user preference model.
- Recommendation service: Provide user preferable news.

## Workflow
News Service works independently. It will fetch news from all major websites periodically, after data processing, 
such as dedupe, then save all news data into mongoDB.

Tensorflow Service works independently and it will retrain a new data at 14:00 on every Sunday to provide the more 
accuracy model. After each time it finished training data, it will upload model for other services to use. 
It will also use the latest model to backfill the latest scpared news.

When user login/signup, backend service will provide user the latest news based on user’s preference which has been 
produced by recommandation service, if user has no preference, backend service will provide the latest news.

Whenever user click on any news, backend service will send this click information to click log server to process 
data and let recommandation service rebuild user preference model and save into database.


## Design Diagrams
### System Design
![Overview](/System_Design.png)


## LICENSE

[MIT](./License.txt)
