SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

docker build -t godville-bot . && \
docker stop godville-bot && \
docker rm godville-bot && \
\
docker run \
--name godville-bot \
--restart unless-stopped \
-d godville-bot

docker logs godville-bot --follow
