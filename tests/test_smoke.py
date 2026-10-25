from pipeline.models import IngestionRecord
from pipeline.exceptions import IngestionError


def test_package_imports() -> None:
    assert IngestionRecord is not None
    assert issubclass(IngestionError, Exception)
