#!/usr/bin/bash

rm -rf /home/data_dump/*

docker exec -t ded09c43d5f1 pg_dumpall -c -U postgres | gzip > /home/data_dump/dump_$(date +"%Y-%m-%d_%H_%M_%S").gz

scp -i ~/.ssh/s2 /home/data_dump/* root@206.189.239.118:~/pg_dumps/

