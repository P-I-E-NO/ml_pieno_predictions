
docker buildx build -t api_distributori $(pwd) 

docker run \
    -w /app \
    -e MYSQL_USER=fre \
    -e MYSQL_PASSWORD=password \
    -e MYSQL_DATABASE=my_sql \
    --network secondo_docker_ml_pieno_net \
    api_distributori

echo "API_DISTRIBUTORI ok"