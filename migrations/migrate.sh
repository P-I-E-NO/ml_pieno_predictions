
docker buildx build -t pieno_migrations $(pwd) 

docker run \
    -w /code \
    -e MYSQL_USER=fre \
    -e MYSQL_PASSWORD=password \
    -e MYSQL_DATABASE=my_sql \
    --network secondo_docker_ml_pieno_net \
    pieno_migrations

echo "migraitons ok"
