from http import client
import json
from optparse import Values
import os

INTERFACE_PATH = "config/interface.json"
CONFIG_PATH = "config/config.json"
RESOURCE_PATH = "assets/resource/mix/pipeline/Event.json"

def load_json(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"配置文件未找到: {json_path}")
    with open(json_path, "r", encoding='utf-8') as f:
        return json.load(f)

class config_client():
    def __init__(self, interface_path=INTERFACE_PATH, config_path=CONFIG_PATH) -> None:
        self.interface_path = interface_path
        self.load_interface(self.load_interface)

        self.config_path = config_path
        self.load_config(self.config_path)

    def load_interface(self, interface_path):
        self.data = load_json(self.interface_path)['client']
        self.client_name = []
        self.client_path = []
        self.indexes = []
        for index, client in enumerate(self.data, start=1):
            self.client_name.append(client['name'])
            self.client_path.append(client['path'])
            self.indexes.append(index)

    def load_config(self, config_path):
        self.config = load_json(self.config_path)

    def get_clients_info(self):
        return self.client_name, self.client_path, self.indexes

    def get_client_names(self):
        return self.client_name

    def get_client_paths(self):
        return self.client_path

    def get_client_info(self, index):
        try:
            index = index - 1
            return self.client_name[index], self.client_path[index]
        except:
            return "index out of range"

    def get_client_name(self, index):
        try:
            index = index - 1
            return self.client_name[index]
        except:
            return "index out of range"

    def get_client_path(self, index):
        try:
            index = index - 1
            return self.client_path[index]
        except:
            return "index out of range"

    def get_active_client_info(self):
        active_name = self.config['client']
        active_path = self.config['resource_path']
        return active_name, active_path

    def set_active_client(self, index):
        try:
            name = self.get_client_name(index)
            path = self.get_client_path(index)
            self.config['client'] = name
            self.config['resource_path'] = path
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            return f"Client setted to {self.get_active_client_info()}"
        except:
            return "index out of range"

class config_task():
    def __init__(self, interface_path=INTERFACE_PATH, config_path=CONFIG_PATH) -> None:
        self.interface_path = interface_path
        self.load_interface(self.load_interface)

        self.config_path = config_path
        self.load_config(self.config_path)

    def load_interface(self, interface_path):
        self.data = load_json(self.interface_path)['task']
        self.task_name = []
        self.task_entry = []
        self.indexes = []
        for index, task in enumerate(self.data, start=1):
            self.task_name.append(task['name'])
            self.task_entry.append(task['entry'])
            self.indexes.append(index)

    def load_config(self, config_path):
        self.active_task = []
        self.active_indexes = []
        self.config = load_json(self.config_path)
        for index, task in enumerate(self.config['task'], start=1):
            self.active_task.append(self.config['task'][task])
            self.active_indexes.append(index)

    def get_task_list(self):
        return self.task_name, self.task_entry, self.indexes

    def get_task_names(self):
        return self.task_name

    def get_task_entries(self):
        return self.task_entry

    def get_task(self, index):
        try:
            index = index - 1
            return self.task_name[index], self.task_entry[index]
        except:
            return "index out of range"

    def get_task_name(self, index):
        try:
            index = index - 1
            return self.task_name[index]
        except:
            return "index out of range"

    def get_task_entry(self, index):
        try:
            index = index - 1
            return self.task_entry[index]
        except:
            return "index out of range"

    def get_active_task_list(self):
        return self.active_task, self.active_indexes

    def get_active_task_name(self):
        name = []
        for task in self.active_task:
            name.append(task['name'])
        return name

    def get_active_task_entry(self):
        entry = []
        for task in self.active_task:
            entry.append(task['entry'])
        return entry

    def add_task(self, index):
        index = index - 1
        task_to_add = self.data[index]
        self.active_task.append(task_to_add)
        self.set_active_task()
        return f"{task_to_add['name']} is added"

    def remove_task(self, index):
        try:
            index = index - 1
            task_to_remove = self.active_task.pop(index)
            self.set_active_task()
            return f"{task_to_remove['name']} is removed"
        except:
            return f"out of index"

    def move_task(self, index, pos):
        index = int(index) - 1
        pos = int(pos) - 1
        task_to_move = self.active_task.pop(index)
        self.active_task.insert(pos, task_to_move)
        self.set_active_task()
        return f"{task_to_move['name']} is moved to {pos+1}"

    def set_active_task(self):
        new_active_task = {str(self.active_indexes + 1): task for self.active_indexes, task in enumerate(self.active_task)}
        self.config['task'] = new_active_task
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
        return True

class config_event():
    def __init__(self, config_path=CONFIG_PATH, resource_path=RESOURCE_PATH) -> None:
        self.config_path = config_path
        self.load_config(self.config_path)

        self.resource_path = resource_path
        self.load_resource(self.resource_path)

    def load_config(self, config_path):
        self.config = load_json(self.config_path)
        self.event_name = self.config['event']['name']
        self.event_time = self.config['event']['time']

    def load_resource(self, resource_path):
        self.resource = load_json(self.resource_path)
        self.find_event = self.resource['FindEvent_inverse']
        self.enter_event = self.resource['EnterEvent']

    def get_event(self):
        return self.event_name, self.event_time

    def get_event_name(self):
        return self.event_name

    def get_event_time(self):
        return self.event_time

    def get_event_name_resource(self):
        return self.enter_event['expected'][0]

    def config_event(self, name, time=3):
        self.config['event']['name'] = name
        self.config['event']['time'] = time
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
        return True

    def config_event_name(self, name) -> bool:
        self.config['event']['name'] = name
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
        return True

    def config_event_time(self, time=3) -> bool:
        self.config['event']['time'] = time
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)
        return True

    def set_event(self, name):
        self.find_event['expected'] = [name]
        self.enter_event['expected'] = [name]
        self.resource['FindEvent_inverse'] = self.find_event
        self.resource['EnterEvent'] = self.enter_event
        with open(self.resource_path, 'w', encoding='utf-8') as f:
            json.dump(self.resource, f, ensure_ascii=False, indent=4)
        return True
