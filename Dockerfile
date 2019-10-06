FROM ubuntu:18.04

# Install prerequisites
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
    libcurl3-dev \
    libleptonica-dev \
    liblog4cplus-dev \
    libopencv-dev \
    libtesseract-dev \
    wget

# Copy all data
COPY . /srv/openalpr

# Setup the build directory
RUN mkdir /srv/openalpr/src/build
WORKDIR /srv/openalpr/src/build

# Setup the compile environment
RUN cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc .. && \
    make -j2 && \
    make install

#Prereqs
RUN apt-get install python3-pip -qq
RUN pip3 install openalpr
RUN pip3 install numpy
RUN pip3 install requests
RUN pip3 install opencv-python
RUN pip3 install envs

#Fix the terrasact-ocr issue by updating the lib
RUN apt-get install software-properties-common -qq
RUN add-apt-repository ppa:alex-p/tesseract-ocr -y
RUN apt-get update
#RUN apt-get tesseract-ocr -qq
RUN apt install libtesseract-dev -y
#Configure ANPR Code
RUN mkdir /anpr
COPY readstream.py /anpr

CMD ["python3", "/anpr/readstream.py"]