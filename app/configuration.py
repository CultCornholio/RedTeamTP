class Configuration:
    REQUIRED_ATTRIBUTES = ["generation_persistence_adapter"]

    @classmethod
    def configure(cls, **options):
        for key, value in options.items():
            setattr(cls, key, value)

    @classmethod
    def validate(cls):
        for attribute in cls.REQUIRED_ATTRIBUTES:
            if not hasattr(cls, attribute):
                raise Exception(f"Invalid Configuration: {attribute} is not set")
