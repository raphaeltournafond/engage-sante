sh stop.sh
docker volume rm engage_sante_postgres_data
sh build.sh
sh run.sh
sh migrate.sh