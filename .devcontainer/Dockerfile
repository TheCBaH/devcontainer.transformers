ARG VARIANT=11
FROM debian:${VARIANT}
RUN set -eux;\
    apt-get update;\
    export DEBIAN_FRONTEND=noninteractive; apt-get install -y --no-install-recommends\
  ca-certificates\
  curl\
  git\
  python3-pip\
  wget\
  xz-utils\
;\
    apt-get autoremove -y; apt-get clean -y ; apt-get clean; rm -rf /var/lib/apt/lists/*;\
    echo DONE
