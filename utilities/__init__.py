# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import configparser
import os
import sys
import json

module_path = os.path.abspath(os.path.join('.'))
sys.path.append(module_path)
config = configparser.ConfigParser()
config.read(module_path+'/config/config.ini')

# [CONFIG]
BACKEND_URL = config['CONFIG']['BACKEND_URL']

#[API_AUTH]
ADMIN_API_KEY = config['API_AUTH']['ADMIN_API_KEY']

#[ENDPOINTS]
CHAT_API = config['ENDPOINTS']['CHAT_API']

__all__ = ["BACKEND_URL",
           "ADMIN_API_KEY",
           "CHAT_API",
           "root_dir",
           "save_config"]