# MASL

**슬세권**은 슬리퍼를 신고 다닐 수 있는 거리에 자주 이용하는 시설들이 있는 권역을 의미합니다.  
MASL은 사용자의 선호에 따라 **슬세권**을 파악하여 꼭 맞는 거주지를 추천하는 웹 서비스입니다.

## Getting Started

프로젝트를 git clone 합니다.
```
> git clone https://kdt-gitlab.elice.io/Jungwoo/masl.git
```

### Prerequisites

해당하는 프로그램의 설치가 필요합니다.

- MongoDB  
```
> cd masl
> wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1804-4.4.4.tgz
> tar xvfz mongodb-linux-x86_64-ubuntu1804-4.4.4.tgz
> sudo mv mongodb-linux-x86_64-ubuntu1804-4.4.4 /usr/local/mongodb
> sudo chown {USER NAME} ./data/db
> vi ~/.bash_profile
```
환경변수를 작성합니다.
```
    export MONGO_PATH=/usr/local/mongodb

    export PATH=$PATH:$MONGO_PATH/bin
```
환경변수를 빌드합니다.
```
> source ~/.bash_profile
> mongod --dbpath=data/db
```
- Python  
```
> sudo apt-get install python3 python3-pip
```
- Node.js
```
> curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
> sudo apt-get install -y nodejs
```

### Installing

아래 사항들로 현 프로젝트에 관한 모듈들을 설치할 수 있습니다.

- Python Packages
```
> cd masl
> pip3 install -r requirements.txt
```
- Node Modules
```
> cd masl/client
> npm i
```

## Running

1. Terminal 1에서 다음 명령어를 실행합니다.
```
> cd masl
> mongo
```
2. Terminal 2에서 다음 명령어를 실행합니다.
```
> cd masl
> flask run -h localhost -p 8080
```
3. Terminal 3에서 다음 명령어를 실행합니다.
```
> cd masl/client
> npm start
```

## Deployment

- Microsoft Azure VM
- Ubuntu 18.04

## Built With

* [황정우](Link) - Product Owner
* [김수영](Link) - Back-End / Algorithm
* [하성민](Link) - Front-End / Data

## License