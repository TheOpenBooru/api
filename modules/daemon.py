from modules import importers, settings, tags
import asyncio
import logging
from threading import Thread
import time

def run_daemon():
    async def background_thread():
        await importers.import_all()
        if settings.TAGS_REGENERATE_ON_BOOT:
            try:
                tags.regenerate()
            except KeyboardInterrupt:
                print("Manually Skippped Tag Regenerated")


    def thread_target():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(background_thread())
        loop.close()


    logging.info("Starting Daemon Thread")
    Thread(target=thread_target, daemon=True).start()
