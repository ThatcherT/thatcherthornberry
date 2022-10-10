# remove danlging images
sudo docker system prune -f
# start docker containers
sudo docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "/home/sa_109683913549673363733/thatcherthornberry:/home/sa_109683913549673363733/thatcherthornberry" -w="/home/sa_109683913549673363733/thatcherthornberry" docker/compose:1.29.2 -f docker-compose.prod.yaml up --force-recreate --remove-orphans -d --build