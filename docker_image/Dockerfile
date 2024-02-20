ARG flavor=alpine

FROM turbointegrations/base:1-$flavor

COPY entrypoint.sh /entrypoint.sh
# COPY server.py /server.py
RUN apk update && \
    apk --no-cache add bash git openssh augeas shadow jq curl && \
    apk --no-cache add build-base postgresql-dev gcc python3-dev musl-dev
RUN groupadd -g 1000 turbo && \
    useradd -r -m -p '' -u 1000 -g 1000 -c 'SSHD User' -s /bin/bash turbo && \
    mkdir -p /etc/authorized_keys && \
    mkdir -p /etc/ssh/keys && \
    mkdir -p /opt/turbonomic/actionscripts && \
    chown -R turbo:turbo /opt/turbonomic/actionscripts 
RUN augtool 'set /files/etc/ssh/sshd_config/AuthorizedKeysFile "/etc/authorized_keys/%u"' && \
    augtool 'set /files/etc/ssh/sshd_config/HostKey[1] /etc/ssh/keys/hostkey' && \
    echo -e "Port 22\n" >> /etc/ssh/sshd_config 
RUN pip install pyvmomi && \
    pip install requests  && \
    pip install requests-oauthlib && \
    pip install psycopg2-binary
RUN chmod +x /entrypoint.sh && \
    mkfifo /var/log/stdout && \
    chmod 0666 /var/log/stdout && \
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/usr/sbin/sshd", "-D", "-e", "-f", "/etc/ssh/sshd_config"]

COPY ./actionscripts/. /opt/turbonomic/actionscripts
