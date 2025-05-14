from ..formatters import FormatterRepository


class TemplateFormattingService(object):
    def __init__(self, repository=None):
        self.repository = repository or FormatterRepository()

    def call(self, operation, inputs, template):
        formatter = self.repository.get_formatter(operation)(inputs, template)
        return formatter.format()
