'''
Author: Rainy
Email: rainysteven1@gmail.com
Date: 2022-09-07 21:48:36
FilePath: /DockerAutoBuild/src/docker_volumes.py
Description: docker容器挂载配置
'''

import os
from docker_abstract import DockerAbstract

REDIS_FOLDERS = ['conf', 'data']


class DockerVolumes(DockerAbstract):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def makedirs_redis_cluster(self):

        port = self.redis_cluster_config.get('redis_port')
        requirepass = self.redis_cluster_config.get('password')
        master_number = self.redis_cluster_config.get('master_number')
        slave_number = self.redis_cluster_config.get('slave_number')
        redis_cluster_name = self.volumes_dir_names.get('redis_cluster')
        redis_cluster_dir = os.path.join(self.volumes_dir, redis_cluster_name)

        def add_folder(type_str, type_number):
            node_conf_copy_path = os.path.join(self.resources_dir,
                                               redis_cluster_name, type_str,
                                               'redis.conf')
            for i in range(1, type_number + 1):
                node = '{0}{1}'.format(type_str, i)
                node_dir = os.path.join(redis_cluster_dir, node)
                for folder in REDIS_FOLDERS:
                    os.makedirs(os.path.join(node_dir, folder))
                node_conf_path = os.path.join(node_dir, 'conf', 'redis.conf')
                cmd = 'PORT={0} REQUIREPASS={1} envsubst <{2} >{3}'.format(
                    port, requirepass, node_conf_copy_path, node_conf_path)
                os.system(cmd)

        if not os.path.exists(redis_cluster_dir):
            add_folder('master', master_number)
            add_folder('slave', slave_number)
