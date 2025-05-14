from ..contracts import ContractRepository


class ContractProcessingService(object):
    def __init__(self, contract_repository=None):
        self.contract_repository = contract_repository or ContractRepository()

    def call(self, operation, inputs):
        contract = self.contract_repository.get_contract(operation)

        return contract.validate(inputs)
