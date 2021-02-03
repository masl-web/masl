# 실행법

## PIP install list
* pymongo
* haversine
* selenium
* pandas
* BeautifulSoup4
* flask

## mongodb install
[MongoDB Download](https://www.mongodb.com/try/download/community)

` $ cd masl `

` $ tar xvfz mongodb-macos-x86_64-4.2.0.tgz `

` $ sudo mv mongodb-osx-x86_64-4.2.0 /usr/local/mongodb `

` $ sudo chown {USER NAME} ./data/db `

` $ vi ~/.bash_profile `

        export MONGO_PATH=/usr/local/mongodb

        export PATH=$PATH:$MONGO_PATH/bin

## lunch

` $ cd masl `

` $ source ~/.bash_profile `

` $ mongod --dbpath=data/db `

` $ mongo (다른 터미널 창에서) `

` $ flask run -h localhost -p 8080 (다른 터미널 창에서) `
