import pandas as pd
import sqlalchemy
import env_config
import config

if __name__ == '__main__':
    df = pd.read_excel('C:\\Users\\xbli06\\Downloads\\综合外教成本趋势.xlsx', sheet_name='Sheet1', skiprows=2)
    #df = pd.read_excel('C:/Users/xbli06/Downloads/综合外教成本趋势.xlsx', sheet_name='Sheet1', skiprows=2)
    print(df)
    engine = sqlalchemy.create_engine(env_config.mssql_url + 'AcadsocAMB', echo=True)
    df.to_sql(name=config.tbl_prefix + 'teacher_cost_trend', con=engine, chunksize=1000, if_exists='replace',
              index=None)
