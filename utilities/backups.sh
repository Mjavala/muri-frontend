#!/usr/bin/bash

rm -rf {path_to_folder}/*

docker exec -t ded09c43d5f1 pg_dumpall -c -U postgres | gzip > {path_to_folder}/dump_$(date +"%Y-%m-%d_%H_%M_%S").gz

scp -i ~/.ssh/{KEY} /home/data_dump/* {USER}@{IP}:~/{dir}

aws s3 cp {path_to_folder} s3://{bucket_name}/ --recursive


