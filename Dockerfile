FROM ubuntu:bionic

RUN apt-get update -y && \
  apt-get install -y tor idle3 curl python3-dev \
   python3-distutils  \
   wget gpg libdbus-glib-1-2 libgtk-3-0 


ENV TOR_VERSION=10.0.16
ENV APP_NAME="Tor Browser ${TOR_VERSION}" \
    TOR_BINARY=https://www.torproject.org/dist/torbrowser/${TOR_VERSION}/tor-browser-linux64-${TOR_VERSION}_en-US.tar.xz \
    TOR_SIGNATURE=https://www.torproject.org/dist/torbrowser/${TOR_VERSION}/tor-browser-linux64-${TOR_VERSION}_en-US.tar.xz.asc \
    TOR_FINGERPRINT=0xEF6E286DDA85EA2A4BA7DE684E2C6E8793298290 \
    DEBIAN_FRONTEND=noninteractive


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

RUN mkdir -p /opt/pystock

# Copy over the torrc created above and set the owner to `tor`
COPY torrc /etc/tor/torrc
#RUN systemctl enable tor && systemctl start tor 
#RUN tor -f /etc/tor/torrc

COPY screeners /opt/pystock/screeners
COPY sends /opt/pystock/sends
COPY main.py /opt/pystock/.
COPY tor_scraper.py /opt/pystock/.

RUN curl https://bootstrap.pypa.io/get-pip.py | python3        
RUN pip3 install --no-cache-dir --upgrade pip 
RUN pip3 --version         
RUN    pip3 install timeunit 
RUN    pip3 install pillow
RUN    pip3 install finvizfinance 
RUN    pip3 install tbselenium 
RUN    pip3 install pathlib 
RUN    pip3 install pandas 
RUN    pip3 install bs4  
RUN    pip3 install requests  



