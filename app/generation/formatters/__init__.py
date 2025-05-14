from .cobalt import CobaltFormatter
from .phish import PhishFormatter

formatters = {
    "cobalt": CobaltFormatter,
    "phish": PhishFormatter,
}


class FormatterRepository(object):
    def __init__(self, registry=formatters):
        self.registry = registry

    def get_formatter(self, key):
        updater_class = self.registry.get(key)
        if not updater_class:
            raise ValueError(f"Formatter for: {key} is not registered")

        return updater_class
