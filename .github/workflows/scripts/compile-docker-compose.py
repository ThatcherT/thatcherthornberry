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
os.chdir(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
# print working directory
docker_compose_paths = []
# git log | grep git-subtree-dir | tr -d ' ' | cut -d ":" -f2 | sort | uniq
p1 = subprocess.Popen(shlex.split("git log"), stdout=subprocess.PIPE)
p2 = subprocess.Popen(
    shlex.split("grep git-subtree-dir"), stdin=p1.stdout, stdout=subprocess.PIPE
)
p3 = subprocess.Popen(shlex.split('tr -d " "'), stdin=p2.stdout, stdout=subprocess.PIPE)
p4 = subprocess.Popen(
    shlex.split('cut -d ":" -f2'), stdin=p3.stdout, stdout=subprocess.PIPE
)
p5 = subprocess.Popen(shlex.split("sort"), stdin=p4.stdout, stdout=subprocess.PIPE)
p6 = subprocess.Popen(shlex.split("uniq"), stdin=p5.stdout, stdout=subprocess.PIPE)
p1.stdout.close()
p2.stdout.close()
p3.stdout.close()
p4.stdout.close()
p5.stdout.close()
output = p6.communicate()[0]
for line in output.splitlines():
    docker_compose_paths.append("./" + line.decode("utf-8") + "/docker-compose.yaml")

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
