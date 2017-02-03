import logging
import xmlrpclib
from server.configuration.configuration import Configuration

__author__ = 'Infectiou'

logger = logging.getLogger(__name__)

class ItemListEntryLoggerClient(object):

    def __init__(self):
        config = Configuration()
        host, port = config.get_configuration()["ItemListEntryLoggerXMLRPC"]
        self.item_list_entry_logger = xmlrpclib.ServerProxy('http://%s:%s' % (str(host), str(port)), allow_none=True)

    def log_crafting_result(self, player_id, item_type, text):
        try:
            self.item_list_entry_logger.log_crafting_result(player_id, item_type, text)
        except Exception as e:
            logger.error("The ItemListEntryLogger could not be reached: %s Data was (%s, %s, %s)"
                         % (str(e), str(player_id), str(item_type), str(text)))

    def log_list_entry_for_player(self, player_id, pos, word):
        self.item_list_entry_logger.log_list_entry_for_player(player_id, pos, word)