# from modules.importers import Safebooru
# import pytest
# import time


# @pytest.mark.asyncio
# async def test_safebooru_subscription_since():
#     safebooru = Safebooru()
#     search = "https://safebooru.org/index.php?page=post&s=list&tags=id%3a1"
#     urls = await safebooru.download_subscription(search, time.time())
#     assert urls == []


# @pytest.mark.asyncio
# async def test_safebooru_subscription():
#     safebooru = Safebooru()
#     search = "https://safebooru.org/index.php?page=post&s=list&tags=id%3a1"
#     urls = await safebooru.download_subscription(search)
#     assert urls == ["https://safebooru.org/index.php?page=post&s=view&id=1"]
