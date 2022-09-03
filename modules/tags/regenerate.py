import logging
from . import regen_namespaces
from modules import database


def user_cancelable_event(function, message):
    try:
        function()
    except KeyboardInterrupt:
        logging.info(message)

def regenerate():
    user_cancelable_event(database.Tag.regenerateCount, "Skipping Database Tag Regeneration")
    
    logging.info("Started Namespace Regeneration")
    user_cancelable_event(regen_namespaces, "Skipping Namespace Regeneration")
