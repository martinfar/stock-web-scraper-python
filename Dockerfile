FROM ubuntu:focal
#FROM dorowu/ubuntu-desktop-lxde-vnc:bionic


RUN apt-get update -y && \
  apt-get install -y tor idle3 curl python3-dev \
   python3-distutils netcat \
   wget gpg libdbus-glib-1-2 libgtk-3-0 libx11-xcb-dev \
   xserver-xorg xserver-xorg-video-all xserver-xephyr x11-xserver-utils xinit xvfb openbox \
   vim gpg \
   ca-certificates \
   supervisor \   
   cron


ENV TOR_VERSION=11.0.10
ENV APP_NAME="Tor Browser ${TOR_VERSION}" \
    TOR_BINARY=https://www.torproject.org/dist/torbrowser/${TOR_VERSION}/tor-browser-linux64-${TOR_VERSION}_en-US.tar.xz \
    TOR_SIGNATURE=https://www.torproject.org/dist/torbrowser/${TOR_VERSION}/tor-browser-linux64-${TOR_VERSION}_en-US.tar.xz.asc \
    TOR_FINGERPRINT=0xEF6E286DDA85EA2A4BA7DE684E2C6E8793298290 \
    DEBIAN_FRONTEND=noninteractive

RUN export GECKO_DRIVER_VERSION='v0.30.0' && wget https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz && tar -xvzf geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz && rm geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz && chmod +x geckodriver && cp geckodriver /usr/local/bin/ 

WORKDIR /app

# Download binary and signature
RUN wget --no-check-certificate $TOR_BINARY && \
    wget --no-check-certificate $TOR_SIGNATURE

# Verify GPG signature
RUN gpg --auto-key-locate nodefault,wkd --locate-keys torbrowser@torproject.org && \
    gpg --output ./tor.keyring --export $TOR_FINGERPRINT && \
    gpgv --keyring ./tor.keyring "${TOR_SIGNATURE##*/}" "${TOR_BINARY##*/}"

# Extract browser & cleanup
RUN tar --strip 1 -xvJf "${TOR_BINARY##*/}" && \
    chown -R ${USER_ID}:${GROUP_ID} /app && \
    rm "${TOR_BINARY##*/}" "${TOR_SIGNATURE##*/}"


RUN curl https://bootstrap.pypa.io/get-pip.py | python3       
RUN pip3 install --no-cache-dir --upgrade pip 
RUN pip3 --version              
RUN	pip3 install -U urllib3  \
          requests \
          requests[socks] \
          timeunit       \
          pillow         \
          finvizfinance  \
          tbselenium     \
          pandas         \
          bs4            \
          debugpy \
          pydevd-pycharm~=213.6777.50     \
          jinja2         

RUN mkdir -p /opt/pystock/stock-results

# Copy over the torrc created above and set the owner to `tor`
COPY torrc /etc/tor/torrc
#RUN systemctl enable tor && systemctl start tor 
#RUN tor -f /etc/tor/torrc

COPY screeners /opt/pystock/screeners
COPY sends /opt/pystock/sends
COPY main.py /opt/pystock/.
COPY tor_scraper.py /opt/pystock/.

RUN ls -ltra /opt/pystock/

WORKDIR /opt/pystock

COPY entrypoint.sh /opt/pystock/.
COPY start.sh /opt/pystock/.

RUN chmod 775 /opt/pystock/entrypoint.sh
RUN chmod 775 /opt/pystock/start.sh
COPY go-cron /usr/local/bin/go-cron
RUN chmod +x /usr/local/bin/go-cron

#COPY supervisord.conf /etc/supervisor/

ENTRYPOINT /opt/pystock/entrypoint.sh

# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]

