'''
Author: Rainy
Email: rainysteven1@gmail.com
Date: 2022-09-07 22:16:17
FilePath: /DockerAutoBuild/src/docker_abstract.py
Description: docker抽象类
'''

import os
import re

from src import DOCKER_IMAGE_OPTIONS


def read_docker_images():
    cmd = "docker images"
    pattern = r'(\S*)\s*(\S*)\s*\w{12}.*'
    image_info_list = os.popen(cmd, 'r').read().split('\n')[1:-1]
    image_info_list = [re.findall(pattern, image_info)[0] for image_info in image_info_list]
    image_version_dict = dict()
    for item in image_info_list:
        if item[0] in DOCKER_IMAGE_OPTIONS:
            if item[0] in image_version_dict.keys():
                image_version_dict[item[0]].append(item[1])
                continue
            image_version_dict[item[0]] = list()
            image_version_dict[item[0]].append(item[1])
    return image_version_dict


class DockerAbstract(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.root_dir = os.path.dirname(os.path.dirname(__file__))
        self.resources_dir = os.path.join(self.root_dir, 'resources')
        self.volumes_dir = os.path.join(self.root_dir, 'volumes')
        self.volumes_images = read_docker_images()
