from openbooru.modules import database, settings
from openbooru.modules.importers import (
    Importer,
    E621Importer,
    E926Importer,
    Rule34Importer,
    SafebooruImporter,
    HydrusImporter,
    FileImporter,
)
from typing import Type
import pytest
import requests


GENERIC_IMPORTERS = (E621Importer, E926Importer, Rule34Importer, SafebooruImporter)


@pytest.mark.parametrize("Importer", GENERIC_IMPORTERS)
@pytest.mark.timeout(10)
async def test_Generic_Importer(Importer: Type[Importer]):
    database.Post.clear()
    importer = Importer()
    await importer.load(100)
    assert database.Post.count() == 100


@pytest.mark.timeout(10)
async def test_Hydrus_Importer():
    try:
        requests.get(settings.IMPORTER_HYDRUS_URL, timeout=2)
    except requests.RequestException:
        pytest.skip("Hydrus Server Doesn't Exist")

    database.Post.clear()
    importer = HydrusImporter()
    await importer.load(5)
    assert database.Post.count() == 5


@pytest.mark.timeout(10)
async def test_Files_Importer():
    database.Post.clear()
    importer = FileImporter("data/images")
    await importer.load(1)
    assert database.Post.count() == 1
