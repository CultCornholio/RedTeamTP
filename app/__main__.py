"""Main entry point for RedTeam Infrastructure Tool"""

import sys
from .cli import cli
from .configuration import Configuration
from .generation.persistence.yaml_adapter import YamlPersistenceAdapter


def main():
    """Main entry point"""
    sys.exit(cli())


if __name__ == "__main__":
    Configuration.configure(
        generation_persistence_adapter=YamlPersistenceAdapter(
            template_dir="templates/warhorse",
            template_generated_dir="generated",
        )
    )

    main()
