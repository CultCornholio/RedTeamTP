import oyaml as yaml
import os


class YamlPersistenceAdapter(object):
    def __init__(self, template_dir, template_generated_dir):
        self.template_dir = template_dir
        self.template_generated_dir = template_generated_dir

    def find(self, operation):
        with open(os.path.join(self.template_dir, f"{operation}.yml"), "r") as file:
            return yaml.safe_load(file)

    def persist(self, operation, data):
        if not os.path.exists(self.template_generated_dir):
            os.makedirs(self.template_generated_dir)

        with open(
            os.path.join(self.template_generated_dir, f"{operation}.yml"), "w"
        ) as file:
            yaml.safe_dump(data, file)
