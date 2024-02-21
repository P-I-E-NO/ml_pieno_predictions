
docker buildx build -t pieno_seed $(pwd) 

docker run \
    -w /code \
    -e MYSQL_USER=fre \
    -e MYSQL_PASSWORD=password \
    -e MYSQL_DATABASE=my_sql \
    --network secondo_docker_ml_pieno_net \
    pieno_seed

echo "migraitons ok"
