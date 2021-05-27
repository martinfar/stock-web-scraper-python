nohup /usr/bin/python3 /home/vtx/pystock/main.py > log-scrape.out 2> error-scrape.err &

docker build --progress plain -t registry.gitlab.com/vatrox05/pystock/ubuntu-tor:1.0 .



docker run -it -d --name tmp-py --shm-size 4G registry.gitlab.com/vatrox05/pystock/ubuntu-tor:1.0
