# Local Test
`nohup /usr/bin/python3 /home/vtx/pystock/main.py > log-scrape.out 2> error-scrape.err &`



# Docker Env

```bash
docker build --progress plain -t registry.gitlab.com/vatrox05/pystock/ubuntu-tor:1.0 .



docker run -it -d --name tmp-py -e SCHEDULE=@daily -m 5G --shm-size 4G --restart always registry.gitlab.com/vatrox05/pystock/ubuntu-tor:1.0


docker run -it -d --name tmp-py -e SCHEDULE="0 0 0 */3 * *" -m 2G --cpus=1 --shm-size 4G --restart always registry.gitlab.com/vatrox05/pystock/ubuntu-tor:1.0


docker-compose down && sudo rm -rf stock-results/05-*-2022/* && docker-compose up -d && docker-compose logs -f

docker exec -it -u 0 pystock_tms_stock_api_1 bash


```
# Csv Parse

`nohup python3 main.py >> init.log 2>&1 & `