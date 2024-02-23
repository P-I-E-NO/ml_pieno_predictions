
docker buildx build -t push_distributor $(pwd) 

docker run \
    -w /app \
    -e MYSQL_USER=fre \
    -e MYSQL_PASSWORD=password \
    -e MYSQL_DATABASE=my_sql \
    --network secondo_docker_ml_pieno_net \
    push_distributor

echo "API ok"