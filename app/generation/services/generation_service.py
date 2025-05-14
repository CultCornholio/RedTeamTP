from .contract_processing_service import ContractProcessingService
from .template_formatting_service import TemplateFormattingService
from ..persistence.template_repository import TemplateRepository


class GenerationService(object):
    @classmethod
    def generate_with(cls, operation, inputs):
        cls().generate(operation, inputs)

    def __init__(
        self,
        contract_processing_service=None,
        template_formatting_service=None,
        template_repository=None,
    ):
        self.contract_processing_service = (
            contract_processing_service or ContractProcessingService()
        )
        self.template_formatting_service = (
            template_formatting_service or TemplateFormattingService()
        )
        self.template_repository = template_repository or TemplateRepository()

    def generate(self, operation, inputs):
        sanitized_inputs = self.contract_processing_service.call(operation, inputs)
        template = self.template_repository.find(operation)
        formatted_template = self.template_formatting_service.call(
            operation, sanitized_inputs, template
        )
        self.template_repository.persist(operation, formatted_template)
