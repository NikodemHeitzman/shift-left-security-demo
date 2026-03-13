FROM ubuntu:latest
LABEL authors="nikod"

ENTRYPOINT ["top", "-b"]