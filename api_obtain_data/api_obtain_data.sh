
docker buildx build -t api_obtain_data $(pwd) 

docker run \
    -w /app \
    -e MYSQL_USER=fre \
    -e MYSQL_PASSWORD=password \
    -e MYSQL_DATABASE=my_sql \
    --network secondo_docker_ml_pieno_net \
    api_obtain_data

echo "OBTAIN DATA ok"