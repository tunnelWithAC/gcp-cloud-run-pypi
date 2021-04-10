FROM pypiserver/pypiserver:latest
WORKDIR /src
ADD packages /src/packages
ADD entrypoint.sh /src
ENTRYPOINT ["./entrypoint.sh"]