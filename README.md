# Local Test
`nohup /usr/bin/python3 /home/vtx/pystock/main.py > log-scrape.out 2> error-scrape.err &`



# Docker Env

```bash
docker build --progress plain -t registry.gitlab.com/vatrox05/pystock/ubuntu-tor:1.0 .



docker run -it -d --name tmp-py -e SCHEDULE=@daily -m 5G --shm-size 4G --restart always registry.gitlab.com/vatrox05/pystock/ubuntu-tor:1.0

docker-compose up

docker exec -it -u 0 pystock_tms_stock_api_1 bash


```
# Csv Parse

`nohup python3 csvstocks.py >> csv.log 2>&1 & `