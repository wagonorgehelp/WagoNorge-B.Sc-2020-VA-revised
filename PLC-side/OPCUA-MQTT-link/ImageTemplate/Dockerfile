FROM python:3.8

RUN pip --disable-pip-version-check --no-cache-dir install paho-mqtt \
    && pip --disable-pip-version-check --no-cache-dir install opcua
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN /usr/local/bin/python -m pip install 'cryptography==3.1.1'