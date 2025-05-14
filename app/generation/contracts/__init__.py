from . import cobalt
from . import phish

contracts = {"cobalt": cobalt.contract, "phish": phish.contract}


class ContractRepository(object):
    def __init__(self, registry=contracts):
        self.registry = registry

    def get_contract(self, key):
        contract = self.registry.get(key)
        if not contract:
            raise ValueError(f"Contract for: {key} is not registered")

        return contract
