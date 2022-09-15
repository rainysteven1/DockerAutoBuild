'''
Author: Rainy
Email: rainysteven1@gmail.com
Date: 2022-09-07 20:58:49
FilePath: /DockerAutoBuild/src/docker_compose.py
Description: python写入docker-compose.yml
'''
import os
import yaml

from .docker_abstract import DockerAbstract

FILE = 'docker-compose.yml'
DOCKER_IMAGES_DICT = {'redis': 'redis:7.0.4', 'mysql': 'mysql:8.0.30'}


class DockerCompose(DockerAbstract):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.root_dir = os.path.dirname(os.path.dirname(__file__))
        self.yaml_path = os.path.join(self.root_dir, FILE)
        self.yaml_data = {'version': '3.2', 'services': dict()}

    def write_networks(self):
        networks_data_list = dict()
        for selector in self.networks_cluster_config:
            name = selector.pop('name')
            config = [dict([item for item in selector.items()])]
            selector['name'] = name
            networks_data_list[name] = {
                "name": name,
                "driver": "bridge",
                "ipam": {
                    "driver": "default",
                    "config": config
                }
            }
        self.yaml_data['networks'] = networks_data_list

    def write_redis_cluster(self):
        master_number = self.redis_cluster_config.get('master_number')
        slave_number = self.redis_cluster_config.get('slave_number')
        port = self.redis_cluster_config.get('port')
        redis_port = self.redis_cluster_config.get('redis_port')
        ip_number = 2
        ip_prefix = ".".join(
            self.networks_cluster_config[0].get('gateway').split('.')[:-1])
        network = self.networks_cluster_config[0].get('name')
        redis_volumes_dir = os.path.join(
            self.volumes_dir, self.volumes_dir_names.get('redis_cluster'))
        docker_conf_path = self.redis_cluster_config.get('docker_conf_path')
        docker_data_dir = self.redis_cluster_config.get('docker_data_dir')
        cmd = self.redis_cluster_config.get('command')
        structure = self.redis_cluster_config.get('structure')

        def write_reids_node(type_str, type_number):
            nonlocal port
            nonlocal ip_number
            for i in range(1, type_number + 1):
                name = '{0}{1}'.format(type_str, i)
                redis_node_dir = '{0}/{1}'.format(redis_volumes_dir, name)
                redis_node_conf_path = os.path.join(redis_node_dir, 'conf',
                                                    'redis.conf')
                redis_node_data_dir = os.path.join(redis_node_dir, 'data')
                self.yaml_data['services'][name] = {
                    "image":
                        self.redis_cluster_config.get('image'),
                    "container_name":
                        name,
                    "environment": ["TZ=Asia/Shanghai"],
                    "ports": ["{0}:{1}".format(port, redis_port)],
                    "volumes": [
                        "{0}:{1}".format(redis_node_conf_path,
                                         docker_conf_path),
                        "{0}:{1}".format(redis_node_data_dir, docker_data_dir)
                    ],
                    "networks":
                        dict([(network, {
                            'ipv4_address':
                                '{0}.{1}'.format(ip_prefix, ip_number)
                        })]),
                    "privileged":
                        True
                }
                if type_str == 'master':
                    self.yaml_data['services'][name]['command'] = cmd.format(
                        docker_conf_path, '', '', '')
                if type_str == 'slave':
                    master = list(
                        filter(lambda x: name in x[1],
                               structure.items()))[0][0]
                    master_network = self.yaml_data['services'][master][
                        'networks'][network]['ipv4_address']
                    self.yaml_data['services'][name]['depends_on'] = [master]
                    self.yaml_data['services'][name]['command'] = cmd.format(
                        docker_conf_path, '--replicaof', master_network,
                        redis_port)
                port += 1
                ip_number += 1

        write_reids_node("master", master_number)
        write_reids_node("slave", slave_number)

    def write_yml(self):
        self.write_networks()
        self.write_redis_cluster()
        with open(self.yaml_path, 'w+') as f:
            yaml.dump(self.yaml_data, f)
