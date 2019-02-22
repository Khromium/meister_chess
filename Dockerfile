FROM python:3.7
MAINTAINER KEI
RUN apt update; apt -y install portaudio19-dev libffi-dev libssl-dev libmpg123-dev python3-dev python3-venv git sudo ; apt-get clean; rm -rf /var/lib/apt/lists/*
# python周りの依存関係のインストール
ADD requirements.txt /
RUN pip --no-cache-dir  install -r requirements.txt
# adafruit 周りのインストール
RUN git clone https://github.com/Khromium/Adafruit_Python_PCA9685.git ;\
	git clone https://github.com/adafruit/Adafruit_Python_GPIO.git ;\
	git clone https://github.com/adafruit/Adafruit_Python_PureIO.git 
RUN cd Adafruit_Python_PCA9685 ; sudo python setup.py install ;\
	cd ../Adafruit_Python_GPIO ; sudo python setup.py install ;\
	cd ../Adafruit_Python_PureIO ; sudo python setup.py install
# # google home 依存関係
# RUN mkdir -p /root/.config/google-oauthlib-tool/ 
# ADD credentials.json /root/.config/google-oauthlib-tool/