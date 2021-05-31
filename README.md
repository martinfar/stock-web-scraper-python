nohup /usr/bin/python3 /home/vtx/pystock/main.py > log-scrape.out 2> error-scrape.err &

docker build --progress plain -t registry.gitlab.com/vatrox05/pystock/ubuntu-tor:1.0 .



docker run -it -d --name tmp-py -e SCHEDULE=@daily -m 5G --shm-size 4G --restart always registry.gitlab.com/vatrox05/pystock/ubuntu-tor:1.0
