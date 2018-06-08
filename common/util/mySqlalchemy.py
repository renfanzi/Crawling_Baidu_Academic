#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
import pandas as pd
from common.Base import Config

ret = Config().get_content('notdbMysql')

# 指定具体库
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(ret["user"],
#                                                                                ret["password"],
#                                                                                ret["host"],
#                                                                                ret["port"],
#                                                                                ret["db_name"])

# 不指定具体库
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(ret["user"],
                                                                            ret["password"],
                                                                            ret["host"],
                                                                            ret["port"],
                                                                            '')
sqlalchemy_engine = create_engine(SQLALCHEMY_DATABASE_URI,
                                  pool_size=20,
                                  pool_recycle=3600,
                                  max_overflow=10,
                                  encoding='utf-8',
                                  )

"""
    ----------------example:
    
        if CasesCondition:
            ConditionVariable = (CasesCondition["ConditionVariable"]).replace(" ", '')
            Operator = (CasesCondition["Operator"]).replace(" ", '')
            ConditionValue = (CasesCondition["ConditionValue"]).replace(" ", '')
            subSelectCases = ConditionVariable + ' ' + Operator + " '" + ConditionValue + "'"
        else:
            subSelectCases = "1=1"

        sql = "select {},{} from {} where {};".format(DependenVariable,IndependentVariable, TableName, subSelectCases)
        df = pd.read_sql(sql, sqlalchemy_engine)
        df_dropna = df.dropna()

        return df_dropna
"""

if __name__ == '__main__':
    import pandas as pd
    res = pd.read_sql("select * from db_metadata.meta_project;", sqlalchemy_engine)
    print(res)
