import pytest
from pathlib import Path
import shutil

from app.generation.persistence.yaml_adapter import YamlPersistenceAdapter
from app.configuration import Configuration


@pytest.fixture
def tmp_dir():
    return "tests/tmp"


@pytest.fixture(autouse=True)
def around_tests(tmp_dir):
    _ensure_tmp_dir(tmp_dir)

    Configuration.configure(
        generation_persistence_adapter=YamlPersistenceAdapter(
            template_dir="templates/warhorse",
            template_generated_dir=tmp_dir,
        )
    )

    yield

    _clean_tmp_dir(tmp_dir)


def _ensure_tmp_dir(tmp_dir):
    Path(tmp_dir).mkdir(parents=True, exist_ok=True)


def _clean_tmp_dir(tmp_dir):
    shutil.rmtree(tmp_dir)
