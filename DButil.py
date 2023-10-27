import os
import pandas as pd
from sqlalchemy import create_engine

# Connect to DB
engine = create_engine(f"mysql+mysqlconnector://"
                       f"{os.environ['dpmo_db_user']}:{os.environ['dpmo_db_pwd']}@"
                       f"{os.environ['dpmo_db_host']}:{os.environ['dpmo_db_port']}/"
                       f"{os.environ['dpmo_db_name']}?charset=utf8")

cs_table = os.environ['dpmo_cs_table']
hs_table = os.environ['dpmo_hs_table']

cs_tables = {"AP": cs_table + "_AP", "SP": cs_table + "_SP", "EMR_FSP_API": cs_table + "_EMR_FSP_API"}
hs_tables = {"AP": hs_table + "_AP", "SP": hs_table + "_SP", "EMR_FSP_API": hs_table + "_EMR_FSP_API"}

cs_dtype = ['string', 'string', 'string', 'int', 'string', 'string', 'string', 'datetime', 'datetime', 'int', 'int', 'int', 'string', 'string', 'string', 'string', 'string']
hs_dtype = ['string', 'string', 'string', 'int', 'string', 'string', 'string', 'int', 'datetime', 'datetime', 'int', 'int', 'int', 'string', 'string', 'string', 'string', 'string', 'string']


def write_to_db(df, table, method="replace"):
    df.to_sql(table, engine, if_exists=method, index=False)


def get_dataframe(table, bkc_no=None):
    condition = ''
    if bkc_no is not None:
        condition = f"WHERE `Work Week` LIKE 'BKC{bkc_no}%'"
    return pd.read_sql(f"SELECT * from `{table}` {condition}", engine, parse_dates=["Cycling Start Date", "Cycling Stop Date"])


def create_table(name):
    if name in cs_tables.values():
        cmd = f"CREATE TABLE IF NOT EXISTS `{name}`(" \
              "`System` varchar(30) NOT NULL," \
              "`BKC` VARCHAR(100) DEFAULT NULL, " \
              "`IFWI` varchar(100) NOT NULL," \
              "`QDF` char(4) DEFAULT NULL," \
              "`Sockets` tinyint(4) DEFAULT NULL," \
              "`OS` varchar(30) DEFAULT NULL," \
              "`HW CFG Description` varchar(1000) DEFAULT NULL," \
              "`Cycling Type` varchar(10) NOT NULL," \
              "`Cycling Start Date` datetime DEFAULT NULL," \
              "`Cycling Stop Date` datetime DEFAULT NULL," \
              "`Target Cycles` smallint(6) NOT NULL," \
              "`Cycles Run` smallint(6) DEFAULT NULL," \
              "`Nof Failures` smallint(6) DEFAULT NULL," \
              "`Failure Description` varchar(1000) DEFAULT NULL," \
              "`PostCode` varchar(10) DEFAULT NULL," \
              "`Current State` varchar(20) DEFAULT NULL," \
              "`PCIe Info` varchar(1000) DEFAULT NULL," \
              "`Log Path` varchar(1000) DEFAULT NULL," \
              "`Comment` varchar(1000) DEFAULT NULL," \
              "`Family` varchar(1000) DEFAULT NULL," \
              "PRIMARY KEY (`System`)" \
              ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    elif name in hs_tables.values():
        cmd = f"CREATE TABLE IF NOT EXISTS `{name}`(" \
              "System VARCHAR(30) NOT NULL," \
              "BKC VARCHAR(100) DEFAULT NULL, " \
              "WorkWeek VARCHAR(100) DEFAULT NULL, " \
              "Program VARCHAR(100) DEFAULT NULL, " \
              "IFWI VARCHAR(100) NOT NULL, " \
              "QDF CHAR(4)," \
              "Sockets TINYINT, " \
              "OS VARCHAR(30), " \
              "`HW CFG Description` VARCHAR(1000), " \
              "`Cycling Type` VARCHAR(10) NOT NULL, " \
              "`Cycling Start Date` DATETIME, " \
              "`Cycling Stop Date` DATETIME, " \
              "`Target Cycles` SMALLINT NOT NULL, " \
              "`Cycles Run` SMALLINT, " \
              "`Nof Failures` SMALLINT, " \
              "`Failure Description` VARCHAR(1000), " \
              "PostCode VARCHAR(10), " \
              "`Current State` VARCHAR(20), " \
              "`Work Week` CHAR(4), " \
              "`Log Path` VARCHAR(1000), " \
              "`Sighting ID` VARCHAR(100), " \
              "Comment VARCHAR(1000)," \
              "`Family` varchar(1000)" \
              ")ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    else:
        raise RuntimeError
    engine.execute(cmd)
