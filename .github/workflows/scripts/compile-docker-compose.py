# pip install python git without cacheing
# set working directory to ../../../ 3 parents up.. use os.chdir()
# get each gitsubtree
# for each repo, add paths (<repo>/docker-compose.yml) for each docker-compose.yml to a lst named file_paths
# with open ./docker-compose.yml as read
#    read the file and write it to a python object where services are keys and the data contained within each is mapped to a string
#    write the header to a new file docker-compose.prod.yml

# for each file in file_paths:
#     read the file and write it to a python object where services are keys and the data contained within each is mapped to a string
#     for each service in the file:
#      Overwrite the service in the python object with the service from the file
# with open ./docker-compose.prod.yml as write
#    for each key in the python object:
#         append to the file to ./docker-compose.yml based on the key value

import os
import yaml
import subprocess
import shlex
from pprint import pprint

# set working directory to ../../../ 3 parents up.. use os.chdir()
# os.chdir(
#     os.path.dirname(
#         os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     )
# )

docker_compose_paths = []
for folder in os.listdir("projects"):
    docker_compose_paths.append('./projects/{}/docker-compose.yml'.format(folder))

yml = {}
for path in docker_compose_paths:
    # use yaml to open as ymlfile
    with open(path, "r") as ymlfile:
        # read the file and write it to a python object where services are keys and the data contained within each is mapped to a string
        file_yml = yaml.load(ymlfile, Loader=yaml.FullLoader)
        # update the yml object with the file_yml object
        # if volumes exist at the top level, append them
        # if services exist at the top level, append them
        services = yml.get("services")
        if not services:
            yml["services"] = file_yml["services"]
        else:
            yml["services"].update(file_yml["services"])
        volumes = yml.get("volumes")
        if not volumes:
            yml["volumes"] = file_yml["volumes"]
        else:
            yml["volumes"].update(file_yml["volumes"])

with open("./docker-compose.yaml", "r") as yml_main:
    file_yml = yaml.load(yml_main, Loader=yaml.FullLoader)
    yml['services'].update(file_yml['services'])
    yml['volumes'].update(file_yml['volumes'])
# write the header to a new file docker-compose.prod.yml
pprint(yml)
with open("./docker-compose.prod.yaml", "w") as prodfile:
    yaml.dump(yml, prodfile, default_flow_style=False)
    # for each key in the python object:


# TODO: need to modify the yaml load to modify paths for this project.. for instance! build: . should be ./projects/spotifly and env_file: .env should be ./projects/spotifly/.env
