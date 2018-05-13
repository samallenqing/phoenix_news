#!/bin/bash
brew services start redis
brew services start mongodb

pip3 install -r requirements.txt

cd news_pipeline
python3 news_monitor.py &
python3 news_fetcher.py &
python3 news_deduper.py &

echo "======================================"
read -p "Press [ENTER] To Terminate Process." PRESSKEY

sudo killall Python