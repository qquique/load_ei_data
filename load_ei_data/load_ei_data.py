import dbf
import os
import zipfile
import tempfile
import signal
import schedule
import logging
import sys
import time
from pathlib import Path
from db import *
from models import FormatA, FormatB
from datetime import date


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

# code pages:
# 437 US MS-DOS
# 850 International MS-DOS
# 1252 Windows ANSI
codepage = 'cp437'
ext = '.DBF'
prefix = 'lsd_'
datadir = os.path.join(os.getenv('DATADIR'), str(date.today().year))  
fieldcount_formata = 30
fieldcount_formatb = 33


def signal_handler(_sig, _frame):
    print('\n Ctrl + C pressed')
    sys.exit()

def create_tables():
    if not FormatA.table_exists():
        FormatA.create_table()
    if not FormatB.table_exists():
        FormatB.create_table()


def get_mapped_rows(table, request_id):
    for record in table:
        record_mapped = {k.lower(): record[k] for k in table.field_names}
        record_mapped['request_id'] = request_id
        yield record_mapped


def exist_request_id(request_id):
    if FormatA.get_or_none(FormatA.request_id == request_id):
        return True
    if FormatB.get_or_none(FormatB.request_id == request_id):
        return True


def process():
    for file in os.listdir(datadir)[:1]:
        request_id = Path(file).stem
        if not exist_request_id(request_id):
            logger.info(f'Processing {file}')
            archive = zipfile.ZipFile(os.path.join(datadir, file), 'r')
            dbfcontent = archive.read(request_id + ext.upper())

            with tempfile.NamedTemporaryFile(suffix=ext.lower(), prefix=prefix) as tf:
                tf.write(dbfcontent)
                tf.flush()
                with dbf.Table(filename=tf.name, codepage=codepage) as table:
                    table.open(dbf.READ_ONLY)
                    records_inserted = 0
                    file_format = ''
                    with db.atomic():
                        if table.field_count == fieldcount_formata:
                            file_format = 'A'
                            records_inserted = FormatA.insert_many(get_mapped_rows(table, request_id)).returning().execute()
                        elif table.field_count == fieldcount_formatb:
                            file_format = 'B'
                            records_inserted = FormatB.insert_many(get_mapped_rows(table, request_id)).returning().execute()
                        logger.info(f"File {file}, format {file_format}, records inserted: {records_inserted}")

                table.close()
        else:
            logger.info(f'{file} already processed')


def main():
    db.connect()
    create_tables()
    schedule.every(1).minutes.do(process)
    while True:
        schedule.run_pending()
        time.sleep(1)
    db.close()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    logger.info('starting...')
    main()
