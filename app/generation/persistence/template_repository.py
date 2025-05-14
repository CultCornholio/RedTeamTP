from ...configuration import Configuration


class TemplateRepository(object):
    def __init__(self, adapter=None):
        self.adapter = adapter or Configuration.generation_persistence_adapter

    def find(self, operation):
        return self.adapter.find(operation)

    def persist(self, operation, data):
        return self.adapter.persist(operation, data)
