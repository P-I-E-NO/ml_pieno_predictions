
docker buildx build -t pieno_preds $(pwd) 

docker run \
    -w /code \
    -e MYSQL_USER=fre \
    -e MYSQL_PASSWORD=password \
    -e MYSQL_DATABASE=my_sql \
    --network secondo_docker_ml_pieno_net \
    pieno_preds

echo "preds ok"
