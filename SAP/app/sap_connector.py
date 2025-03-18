import os
from pyrfc import Connection
from dotenv import load_dotenv

load_dotenv()

class SAPConnector:
    def __init__(self):
        self.conn_params = {
            "ashost": os.getenv("SAP_ASHOST"),
            "sysnr": os.getenv("SAP_SYSNR"),
            "client": os.getenv("SAP_CLIENT"),
            "user": os.getenv("SAP_USER"),
            "passwd": os.getenv("SAP_PASSWD"),
            "lang": os.getenv("SAP_LANG"),
        }
        self.conn = None

    def connect(self):
        try:
            self.conn = Connection(**self.conn_params)
            return True
        except Exception as e:
            print(f"Erreur connexion SAP : {e}")
            return False

    def read_table(self, table_name, fields, options=None, max_rows=100):
        if not self.conn:
            self.connect()
        try:
            result = self.conn.call(
                'RFC_READ_TABLE',
                QUERY_TABLE=table_name,
                DELIMITER=';',
                FIELDS=[{'FIELDNAME': field} for field in fields],
                OPTIONS=[{'TEXT': options}] if options else [],
                ROWCOUNT=max_rows
            )
            columns = [field['FIELDNAME'] for field in result['FIELDS']]
            data = [row['WA'].split(';') for row in result['DATA']]
            return columns, data
        except Exception as e:
            print(f"Erreur lecture table SAP : {e}")
            return [], []

    def close(self):
        if self.conn:
            self.conn.close()
