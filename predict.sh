
docker buildx build -t pieno_predict $(pwd) 

docker run \
    -w /app \
    -e MYSQL_USER=fre \
    -e MYSQL_PASSWORD=password \
    -e MYSQL_DATABASE=my_sql \
    --network secondo_docker_ml_pieno_net \
    pieno_predict

echo "Predict ok"