#!/usr/bin/env bash
mongoexport -d phoenix-news -c news -o ./news_topic_modeling_service/data/news.csv
(cd news_topic_modeling_service/trainer && exec python3 news_class_trainer.py) &