import logging
import os
import sys

import pandas as pd

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


from dart.api import Dart_main_api
from dart.utils import get_jinja_yaml_conf, create_db_engine, Postgres_connect
from dart.processing import Disc_processor, Report_processor, Finance_processor, Equity_processor, keymatter_processor, Regist_processor

def main():
    os.chdir(os.path.dirname(__file__))
    conf = get_jinja_yaml_conf('./conf/api.yml', './conf/logging.yml')



    # logger 설정
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=eval(conf['logging']['level']),
        format=conf['logging']['format'],
        handlers = [TimedRotatingFileHandler(filename =  conf['logging']['file_name'],
                                    when=conf['logging']['when'],
                                    interval=conf['logging']['interval'],
                                    backupCount=conf['logging']['backupCount']), logging.StreamHandler()]
                    )



    engine = create_db_engine(os.environ)
    postgres_conn = Postgres_connect(engine)


    dart_api = Dart_main_api(auth_key = os.environ['auth_key'])
    
    if sys.argv[1] in conf:
        logger.info(f"Run {sys.argv[1]}!")
    
    else:
        raise Exception(f"You entered not allowed sub name.")
    
    
    if sys.argv[1] == 'disc':
        disc_processor = Disc_processor(db_conn = postgres_conn, api_conn = dart_api, conf = conf)
        disc_processor.upload_corp_code()
        disc_processor.upload_list()
        disc_processor.upload_company()
        disc_processor.upload_docfile(_ts = os.environ['_ts'])

    elif sys.argv[1] == 'br':
        br_processor = Report_processor(db_conn = postgres_conn, api_conn = dart_api, conf = conf)
        for idx, detail in enumerate(conf['br'].keys()):
            logger.info(f"{detail} upload starts! ({idx+1} / {len(conf['br'].keys())})")
            br_processor.func(detail = detail)

    elif sys.argv[1] == 'fn':
        fn_processor = Finance_processor(db_conn = postgres_conn, api_conn = dart_api, conf = conf)
        for detail in ['fnltt_singl_acnt', 'fnltt_multi_acnt']:
            logger.info(f"{detail} upload starts!")
            fn_processor.acc_func(detail = detail)

        for detail in ['fnltt_singl_indx', 'fnltt_cmpny_indx']:
            logger.info(f"{detail} upload starts!")
            fn_processor.idx_func(detail = detail)

        fn_processor.upload_xbrl(_ts = os.environ['_ts'])
        fn_processor.upload_xbrl_taxo()
        fn_processor.upload_sgl_acc_all()


    elif sys.argv[1] == 'eq':
        eq_processor = Equity_processor(db_conn = postgres_conn, api_conn = dart_api, conf = conf)
        for idx, detail in enumerate(conf['eq'].keys()):
            logger.info(f"{detail} upload starts! ({idx+1} / {len(conf['eq'].keys())})")
            eq_processor.func(detail = detail)

    elif sys.argv[1] == 'km':
        km_processor = keymatter_processor(db_conn = postgres_conn, api_conn = dart_api, conf = conf)
        for idx, detail in enumerate(conf['km'].keys()):
            logger.info(f"{detail} upload starts! ({idx+1} / {len(conf['km'].keys())})")
            km_processor.func(detail = detail)

    elif sys.argv[1] == 'rs':
        rs_processor = Regist_processor(db_conn = postgres_conn, api_conn = dart_api, conf = conf)
        for idx, detail in enumerate(conf['rs'].keys()):
            logger.info(f"{detail} upload starts! ({idx+1} / {len(conf['rs'].keys())})")
            rs_processor.func(detail = detail)
        
        
if __name__ == "__main__":
    main()