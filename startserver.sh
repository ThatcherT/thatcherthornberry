# remove danlging images
sudo docker system prune -f
# start docker containers for me
sudo docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "/home/sa_109683913549673363733/me:/home/sa_109683913549673363733/me" -w="/home/sa_109683913549673363733/me" docker/compose:1.29.2 up --force-recreate --remove-orphans -d --build
# start docker containers for spotifly
sudo docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "/home/sa_109683913549673363733/spotifly:/home/sa_109683913549673363733/spotifly" -w="/home/sa_109683913549673363733/spotifly" docker/compose:1.29.2 up --force-recreate --remove-orphans -d --build