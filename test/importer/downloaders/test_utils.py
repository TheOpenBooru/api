from modules.importers import utils
import pytest


# guess_mimetype
@pytest.mark.asyncio
async def test_Bad_File_Raises_ValueError():
    with pytest.raises(ValueError):
        utils.guess_mimetype("/test")
