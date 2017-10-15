import logging
import logging.config


def configure_logging(level, filename):
    logging.config.dictConfig(
        {
            'version' : 1,
            'handlers' : {
                'console' : {
                    'class' : 'logging.StreamHandler',
                    'formatter' : 'default',
                    'level' : level,
                    'stream' : 'ext://sys.stdout'
                },
                'file' : {
                    'class' : 'logging.handlers.RotatingFileHandler',
                    'formatter': 'default',
                    'level' : level,
                    'filename' : filename,
                    'maxBytes' : 4096,
                    'backupCount' : 3
                }
            },
            'formatters' : {
                'default' : {
                    'format' : '%(asctime)s | %(levelname)s | %(message)s'
                }
            },
            'loggers' : {
                __name__ : {
                    'handlers' : ['console', 'file']
                }
            }
        }
    )


configure_logging(logging.DEBUG, '/home/kmcvay/tmp/symlink_manager.log')
logger = logging.getLogger(__name__)

