import io
import logging
import os
import re
import time
import zipfile
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class Base_processor:
    def __init__(self, db_conn, api_conn, conf, sub = None):
        self.db_conn = db_conn
        self.conf = conf
        self.api_conn = api_conn
        self.sub = sub

    def processing_cols(self, data, detail_info, inplace = True):
        if 'no_cols' in detail_info:
            self.processing_no_cols(data, detail_info['no_cols'], inplace = inplace)
        if 'fillna_cols' in detail_info:
            self.processing_fillna_cols(data, detail_info['fillna_cols'], inplace = inplace)
        if 'num_cols' in detail_info:
            self.processing_num_cols(data, detail_info['num_cols'], inplace = inplace)
        if 'date_cols' in detail_info:
            self.processing_date_cols(data, detail_info['date_cols'], inplace = inplace)
        if 'dup_cols' in detail_info:
            self.processing_dup_cols(data, detail_info['dup_cols'], inplace = inplace)
        if 'dropna_cols' in detail_info:
            self.processing_dropna_cols(data, detail_info['dropna_cols'], inplace = inplace)
    

    def processing_num_cols(self, data, cols, inplace = True):
        if not inplace:
            data = data.copy()
        # print(data[cols].T)
        data[cols] = data[cols].apply(lambda x: x.str.replace(r'[,#*%"\n]', r'', regex = True).str.strip() if x.dtypes == 'object' else x).replace('.', '').replace('-', '').replace('--', '')
        data[cols] = data[cols].replace('', pd.NA).apply(pd.to_numeric)
        if not inplace:
            return data
        
    def processing_date_cols(self, data, cols, inplace = True):
        pattern = r'(\d{4})[년.-] ?(\d{1,2})[월.-] ?(\d{1,2})[일]?'
        
        if not inplace:
            data = data.copy()
        data[cols] = data[cols].replace('-', pd.NA).map(lambda x: x.replace('.', '-') if isinstance(x, str) else x)
        data[cols] = data[cols].map(lambda x: '-'.join(re.findall(pattern, x)[0]) if isinstance(x, str) and re.match(pattern, x) else x)
        if not inplace:
            return data

    def processing_fillna_cols(self, data, fillna_info, inplace = True):
        if not inplace:
            data = data.copy()
        cols = list(fillna_info.keys())
        data[cols] = data[cols].fillna(fillna_info)
        if not inplace:
            return data

    def processing_no_cols(self, data, no_info, inplace = True):
        if not inplace:
            data = data.copy()
        no_cols = [col for col in no_info if col not in data.columns]
        data[no_cols] = np.nan
        if not inplace:
            return data

    def processing_dup_cols(self, data, dup_info, inplace = True):
        if not inplace:
            data = data.copy()
        dup_cols = data.columns if dup_info == 'all' else dup_info
        data.drop_duplicates(subset = dup_cols,
                                inplace = True)
        if not inplace:
            return data

    def processing_dropna_cols(self, data, dropna_info, inplace = True):
        if not inplace:
            data = data.copy()
        data.dropna(subset = dropna_info, axis = 'row', inplace = True)
        if not inplace:
            return data
        

    def get_upload_target_year(self, detail, corp_code, report_info):

        report_list = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['disc']['list']['table_name'],
                        columns = ['보고서명', '접수일자', '접수번호'],
                        where = [f"고유번호='{corp_code}'", 
                                 f"보고서명 SIMILAR TO '%%{report_info[0]}%%'", 
                                 r"보고서명 LIKE '%%(____.__)'"],
                        )

        report_list['사업연도'] = report_list['보고서명'].map(lambda x: pd.to_datetime(x[-8:-1], format = '%Y.%m').year)
        

        db_history = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['history_table_name'],
                        columns = 'latest_ins_date',
                        where = [f"고유번호='{corp_code}'", 
                                 f"테이블이름='{self.conf[self.sub][detail]['table_name']}'"],
                        )

        db_latest_ins_date = db_history.iloc[0, 0] if db_history.shape[0] > 0 else datetime(self.conf['api_report_start_year'], 1, 1).date()

        

        return report_list.loc[report_list['접수일자'] >= db_latest_ins_date, '사업연도'].sort_values().unique()

    
    def _write_history(self, table_name, corp_code, _ts = datetime.astimezone(datetime.now())):
        
        data = pd.DataFrame([[_ts, table_name, corp_code, _ts.date()]], columns = ['_ts', '테이블이름', '고유번호', 'latest_ins_date'])
        self.db_conn.upsert(data,
                                self.conf['schema_name'], 
                                table_name = self.conf['history_table_name'])

    

    def get_proc_upload(self, detail, params = {}, ins_col_info = {}):
        try:
            data = self.api_conn.get_data(self.conf[self.sub][detail]['detail_url'], 
                        rename = self.conf[self.sub][detail]['rename'],
                        params = params)

        except Exception as e:
            if isinstance(e.args[0], dict) and e.args[0]['status'] == '013':
                logger.warning(f"There is some error in {detail}, params: {params}")
                logger.warning(e)
                return
            raise Exception(e)
    
        for col, val in ins_col_info.items():
            data[col] = data[val]
        
        if 'num_cols' in self.conf[self.sub][detail]:
            self().processing_num_cols(data, self.conf[self.sub][detail]['num_cols'])

        logger.info(f"data shape: {data.shape[0]}")
        self.db_conn.upsert(data,
                            self.conf['schema_name'], 
                            table_name = self.conf[self.sub][detail]['table_name'])

class Disc_processor(Base_processor):    
    def __init__(self, db_conn, api_conn, conf):
        logger.info('Initialize disclosure data processer!')
        super().__init__(db_conn, api_conn, conf, 'disc')
        
    def upload_corp_code(self):
        logger.info('upload corp code starts!')
        detail = 'corp_code'

        for _ in range(len(self.api_conn.auth_list)):
            try:
                data = self.api_conn.get_data(self.conf[self.sub][detail]['detail_url'], data_type = 'xml', is_zip = True, rename = self.conf[self.sub][detail]['rename'])
                
            except:
                self.api_conn.chg_auth_key()

        
        data[self.conf[self.sub][detail]['date_col']] = data[self.conf[self.sub][detail]['date_col']].map(lambda x: pd.to_datetime(x, format = '%Y%m%d').date())
        data['고유번호'] = data['고유번호'].map(lambda x: str(x).zfill(8))
        data.replace('', pd.NA, inplace = True)
        
        max_db_date = self.db_conn.get_maxmin_col(schema_name = self.conf['schema_name'],
                    table_name = self.conf[self.sub][detail]['table_name'],
                    column = self.conf[self.sub][detail]['date_col'])[0]
        
        
        if max_db_date:
            data = data[data[self.conf[self.sub][detail]['date_col']] >= max_db_date]

        
        if 'dup_cols' in self.conf[self.sub][detail]:
            data =  self.db_conn.ext_notin_db(data, schema_name = self.conf['schema_name'], 
                                    table_name = self.conf[self.sub][detail]['table_name'], 
                                    subset = self.conf[self.sub][detail]['dup_cols'])

        
        self.db_conn.upsert(data, schema_name = self.conf['schema_name'], table_name = self.conf[self.sub][detail]['table_name'])
        
    
    def upload_list(self):
        logger.info('upload list starts!')
        detail = 'list'
        max_db_date = self.db_conn.get_maxmin_col(schema_name = self.conf['schema_name'],
                    table_name = self.conf[self.sub][detail]['table_name'],
                                column = self.conf[self.sub][detail]['date_col'])[0]

        start_date = max_db_date if max_db_date else self.conf['api_start_date']
        end_date = self.conf['api_end_date'] if 'api_end_date' in self.conf else pd.to_datetime(os.environ['_ts']).date() + timedelta(days = 1)
        
        
        data = pd.DataFrame()
        date_list = pd.date_range(start_date, end_date, periods = int((end_date - start_date) / timedelta(days = 80)) + 1).tolist()
        date_list.append(pd.to_datetime(end_date))
        logger.info(f"data load will be start from {date_list[0].date()} to {date_list[-1].date()}.")

        for idx in range(len(date_list) - 1):
            bgn_de, end_de = date_list[idx].strftime('%Y%m%d'), (date_list[idx+1] - timedelta(days = 1)).strftime('%Y%m%d')
            logger.info(f"data load starts from {bgn_de} to {end_de} ({idx+1}/{len(date_list) - 1}).")
            
            data = self.api_conn.get_data(detail_url = self.conf[self.sub][detail]['detail_url'], 
                            params = {'bgn_de': bgn_de,
                                        'end_de': end_de },
                                rename = self.conf[self.sub][detail]['rename']).replace('', pd.NA)
            
            if 'dup_cols' in self.conf[self.sub][detail]:
                dup_cols = data.columns if self.conf[self.sub][detail]['dup_cols'] == 'all' else self.conf[self.sub][detail]['dup_cols']
                data =  self.db_conn.ext_notin_db(data, schema_name = self.conf['schema_name'], 
                                table_name = self.conf[self.sub][detail]['table_name'], 
                                subset = dup_cols)
            
            
            self.db_conn.upsert(data.drop_duplicates(),
                schema_name = self.conf['schema_name'],
                table_name = self.conf[self.sub][detail]['table_name'])

    def upload_docfile(self, _ts = datetime.astimezone(datetime.now())):
        detail = 'document'
        db_list = self.db_conn.get_data(self.conf['schema_name'], self.conf[self.sub][detail]['table_name'], columns = '접수번호', is_distinct = True)
        where = [f"접수번호 > '{db_list.max()}'"] if db_list.shape[0] > 0 else None
        rcept_list = self.db_conn.get_data('dart', 'disc_list', columns = '접수번호', orderby_cols = '접수번호', where = where)['접수번호']

        
        for idx, rcept_no in enumerate(rcept_list):
            logger.info(f"'{rcept_no}' doc upload starts! ({idx+1}/{len(rcept_list)})")
        
            res = None
            while res is None or '사용한도를 초과' in res.text:
                try:
                    res = self.api_conn.get_api_data(self.conf[self.sub][detail]['detail_url'], params = {'rcept_no': rcept_no}, data_type = 'xml')
                    
                    file = zipfile.ZipFile(
                                io.BytesIO(res.content))
            
                except Exception as e:
                    if res is not None and '사용한도를 초과' in res.text:
                        self.api_conn.chg_auth_key()
                    logger.warning(e)

            if '파일이 존재' in res.text:
                logger.warning(f"There doesn't exist rcept_no: {rcept_no}; skip this report.")
                continue
        

            try:
                data = pd.DataFrame([[_ts, rcept_no, file_name, BeautifulSoup(file.read(file_name), features = 'xml').prettify()] for file_name in file.namelist()], columns = ['_ts', '접수번호', '파일이름', '파일내용'])
                
                self.db_conn.insert_df(data,
                                    self.conf['schema_name'],
                                    self.conf[self.sub][detail]['table_name'])

            except Exception as e:
                logger.error(f"error file: {rcept_no}")
                logger.error(f"{e}")

        
    def upload_company(self):
        logger.info('upload corp overview starts!')
        detail = 'company'
        
        corp_list = self.db_conn.get_data(schema_name = self.conf['schema_name'],
                    table_name = self.conf[self.sub]['list']['table_name'],
                                columns = ['고유번호'],
                            is_distinct = True)


        db_list = self.db_conn.get_data(schema_name = self.conf['schema_name'],
                                table_name = self.conf[self.sub][detail]['table_name'],
                                columns = ['고유번호']).to_numpy().ravel()
        
        corp_list = corp_list.loc[~corp_list.isin(db_list).iloc[:, 0]].to_numpy().ravel()
        
        
        for idx, corp in enumerate(corp_list):
            logger.info(f"Check company info '{corp}' ({idx+1}/{len(corp_list)})...")

            db_max_ts = self.db_conn.get_maxmin_col(schema_name = self.conf['schema_name'],
                                table_name = self.conf[self.sub][detail]['table_name'],
                                column = '_ts',
                                where = [f"고유번호 = '{corp}'"])[0]

            db_latest_update = self.db_conn.get_maxmin_col(schema_name = self.conf['schema_name'],
                                table_name = self.conf[self.sub]['corp_code']['table_name'],
                                column = '최종변경일자',
                                where = [f"고유번호 = '{corp}'"])[0]

            if db_max_ts and db_max_ts.date() > db_latest_update:
                logger.info(f"'{corp}' is existing in db. skip api call.")
                continue
            
            data = self.api_conn.get_data(detail_url = self.conf[self.sub][detail]['detail_url'], 
                                    params = {'corp_code': corp},
                                        rename = self.conf[self.sub][detail]['rename']).drop(columns = ['status', 'message'])

            if 'dup_cols' in self.conf[self.sub][detail]:
                data =  self.db_conn.ext_notin_db(data, schema_name = self.conf['schema_name'], 
                                table_name = self.conf[self.sub][detail]['table_name'], 
                                subset = self.conf[self.sub][detail]['dup_cols'])

            self.db_conn.upsert(data,
                schema_name = self.conf['schema_name'],
                table_name = self.conf[self.sub][detail]['table_name'])

    

        
    
    

class Report_processor(Base_processor):
    def __init__(self, db_conn, api_conn, conf, sub = 'br'):
        logger.info('Initialize business report data processer!')
        super().__init__(db_conn, api_conn, conf, sub)
        self.report_type = [['분기보고서', 11013],
            ['반기보고서', 11012],
            ['분기보고서', 11014],
            ['사업보고서', 11011]]
        
        self.corp_codes = db_conn.get_data(schema_name = conf['schema_name'], 
                    table_name = conf['disc']['corp_code']['table_name'],
                    columns = ['고유번호'],
                    orderby_cols = ['고유번호']).to_numpy().ravel()

        logger.info(f"There are {len(self.corp_codes)} corp_codes in db.")


    def check_corp_list(self, detail):
        db_history = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['history_table_name'],
                        columns = ['고유번호', 'latest_ins_date'],
                        where = [f"테이블이름='{self.conf[self.sub][detail]['table_name']}'"],
                        )

        report_list = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['disc']['list']['table_name'],
                        columns = ['고유번호', '접수일자'],
                        where = [f"보고서명 SIMILAR TO '{'|'.join([report[0] for report in self.report_type])}%%'", 
                                 r"보고서명 LIKE '%%(____.__)'"],
                        )

        latest_report_date = report_list.groupby('고유번호')['접수일자'].max().reset_index()
        merge_data = latest_report_date.merge(db_history, on = '고유번호', how = 'left')
        corp_idx = merge_data.apply(lambda x: x['접수일자'] >= x['latest_ins_date'] if not pd.isna(x['latest_ins_date']) else True , axis = 1)
        corp_idx &= merge_data['접수일자'] >= datetime(self.conf['api_report_start_year'], 1, 1).date()

        logger.info(f"Run only for corp_code not in DB: (nums: {corp_idx.sum()})")
        return merge_data.loc[corp_idx, '고유번호'].to_numpy().ravel()
    

    def func(self, detail):
        logger.info(f"{'#' * 15} Starts {self.conf[self.sub][detail]['table_name']} upload! {'#' * 15}")
        corp_codes = self.check_corp_list(detail)


        for corp_idx, corp_code in enumerate(corp_codes):
            logger.info(f"data upload starts for '{corp_code}'({corp_idx+1}/{len(corp_codes)})")
            cnt = 0
            corp_data = pd.DataFrame()


            for rep_idx, report_info in enumerate(self.report_type):
                logger.debug(f"Upload report type: '{report_info[1]}' ({rep_idx+1}/{len(self.report_type)}).")
                target_years = super().get_upload_target_year(detail, corp_code, report_info)

                for yr_idx, year in enumerate(target_years):
                    logger.debug(f"Upload {year} starts! ({yr_idx+1}/{len(target_years)})")

                    try:
                        params = {'corp_code': corp_code, 'bsns_year': year, 'reprt_code': report_info[1]}
                        data = self.api_conn.get_data(self.conf[self.sub][detail]['detail_url'], 
                                    rename = self.conf[self.sub][detail]['rename'],
                                    params = params)
            
                    except Exception as e:
                        if isinstance(e.args[0], dict) and e.args[0]['status'] == '013':
                            logger.warning(f"There is some error in {detail}, params: {params}")
                            logger.warning(e)
                            continue
                        raise Exception(e)
                
                    
                    data['사업연도'] = year
                    data['보고서코드'] = report_info[1]

                    self.processing_cols(data, self.conf[self.sub][detail])
                    corp_data = pd.concat([corp_data, data])

            # return corp_data
            if corp_data.shape[0] > 0:
                self.db_conn.upsert(corp_data,
                                    self.conf['schema_name'], 
                                    table_name = self.conf[self.sub][detail]['table_name'])



            super()._write_history(table_name = self.conf[self.sub][detail]['table_name'],
                           corp_code = corp_code)
                

class Finance_processor(Base_processor):
    def __init__(self, db_conn, api_conn, conf, sub = 'fn'):
        logger.info('Initialize finance report data processer!')
        super().__init__(db_conn, api_conn, conf, sub)
        self.report_type = [['분기보고서', 11013],
            ['반기보고서', 11012],
            ['분기보고서', 11014],
            ['사업보고서', 11011]]
        
        self.corp_codes = db_conn.get_data(schema_name = conf['schema_name'], 
                    table_name = conf['disc']['corp_code']['table_name'],
                    columns = ['고유번호'],
                    orderby_cols = ['고유번호']).to_numpy().ravel()

        logger.info(f"There are {len(self.corp_codes)} corp_codes in db.")


    def check_corp_list(self, detail):
        db_history = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['history_table_name'],
                        columns = ['고유번호', 'latest_ins_date'],
                        where = [f"테이블이름='{self.conf[self.sub][detail]['table_name']}'"],
                        )

        report_list = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['disc']['list']['table_name'],
                        columns = ['고유번호', '접수일자'],
                        where = [f"보고서명 SIMILAR TO '{'|'.join([report[0] for report in self.report_type])}%%'", 
                                 r"보고서명 LIKE '%%(____.__)'"],
                        )

        latest_report_date = report_list.groupby('고유번호')['접수일자'].max().reset_index()
        merge_data = latest_report_date.merge(db_history, on = '고유번호', how = 'left')
        corp_idx = merge_data.apply(lambda x: x['접수일자'] >= x['latest_ins_date'] if not pd.isna(x['latest_ins_date']) else True , axis = 1)
        corp_idx &= merge_data['접수일자'] >= datetime(self.conf['api_report_start_year'], 1, 1).date()

        logger.info(f"Run only for corp_code not in DB: (nums: {corp_idx.sum()})")
        return merge_data.loc[corp_idx, '고유번호'].to_numpy().ravel()
    

    def acc_func(self, detail):
        logger.info(f"{'#' * 15} Starts {self.conf[self.sub][detail]['table_name']} upload! {'#' * 15}")
        corp_codes = self.check_corp_list(detail)


        for corp_idx, corp_code in enumerate(corp_codes):
            logger.info(f"data upload starts for '{corp_code}'({corp_idx+1}/{len(corp_codes)})")
            cnt = 0
            corp_data = pd.DataFrame()


            for rep_idx, report_info in enumerate(self.report_type):
                logger.debug(f"Upload report type: '{report_info[1]}' ({rep_idx+1}/{len(self.report_type)}).")
                target_years = super().get_upload_target_year(detail, corp_code, report_info)

                for yr_idx, year in enumerate(target_years):
                    logger.debug(f"Upload {year} starts! ({yr_idx+1}/{len(target_years)})")

                    try:
                        params = {'corp_code': corp_code, 'bsns_year': year, 'reprt_code': report_info[1]}
                        data = self.api_conn.get_data(self.conf[self.sub][detail]['detail_url'], 
                                    rename = self.conf[self.sub][detail]['rename'],
                                    params = params)
            
                    except Exception as e:
                        if isinstance(e.args[0], dict) and e.args[0]['status'] == '013':
                            logger.warning(f"There is some error in {detail}, params: {params}")
                            logger.warning(e)
                            continue
                        raise Exception(e)
                
                    
                    data['사업연도'] = year
                    data['보고서코드'] = report_info[1]
                    
                    self.processing_cols(data, self.conf[self.sub][detail])
                    corp_data = pd.concat([corp_data, data])

            if corp_data.shape[0] > 0:
                self.db_conn.upsert(corp_data,
                                    self.conf['schema_name'], 
                                    table_name = self.conf[self.sub][detail]['table_name'])



            super()._write_history(table_name = self.conf[self.sub][detail]['table_name'],
                           corp_code = corp_code)

    
    def idx_func(self, detail):
        logger.info(f"{'#' * 15} Starts {self.conf[self.sub][detail]['table_name']} upload! {'#' * 15}")
        corp_codes = self.check_corp_list(detail)


        for corp_idx, corp_code in enumerate(corp_codes):
            logger.info(f"data upload starts for '{corp_code}'({corp_idx+1}/{len(corp_codes)})")
            cnt = 0
            corp_data = pd.DataFrame()


            for rep_idx, report_info in enumerate(self.report_type):
                logger.debug(f"Upload report type: '{report_info[1]}' ({rep_idx+1}/{len(self.report_type)}).")
                target_years = super().get_upload_target_year(detail, corp_code, report_info)
                target_years = [year for year in target_years if year >= 2023]

                for yr_idx, year in enumerate(target_years):
                    logger.debug(f"Upload {year} starts! ({yr_idx+1}/{len(target_years)})")

                    for idx_idx, idx_code in enumerate(['M210000', 'M220000', 'M230000', 'M240000']):

                        try:
                            params = {'corp_code': corp_code, 'bsns_year': year, 'reprt_code': report_info[1], 'idx_cl_code': idx_code}
                            data = self.api_conn.get_data(self.conf[self.sub][detail]['detail_url'], 
                                        rename = self.conf[self.sub][detail]['rename'],
                                        params = params)
                
                        except Exception as e:
                            if isinstance(e.args[0], dict) and e.args[0]['status'] == '013':
                                logger.warning(f"There is some error in {detail}, params: {params}")
                                logger.warning(e)
                                continue
                            raise Exception(e)
                    
                        
                        data['사업연도'] = year
                        data['보고서코드'] = report_info[1]
                        
                        self.processing_cols(data, self.conf[self.sub][detail])         
                        corp_data = pd.concat([corp_data, data])

            if corp_data.shape[0] > 0:
                self.db_conn.upsert(corp_data,
                                    self.conf['schema_name'], 
                                    table_name = self.conf[self.sub][detail]['table_name'])



            super()._write_history(table_name = self.conf[self.sub][detail]['table_name'],
                           corp_code = corp_code)

    def upload_xbrl(self, _ts = datetime.astimezone(datetime.now())):
        detail = 'fnltt_xbrl'
        db_list = self.db_conn.get_data(self.conf['schema_name'], self.conf[self.sub][detail]['table_name'], columns = '접수번호', is_distinct = True)
        where = [f"접수번호 > '{db_list.max()}'"] if db_list.shape[0] > 0 else []
        where.append(f"보고서명 SIMILAR TO '%%사업보고서|분기보고서|반기보고서%%'")
        rcept_list = self.db_conn.get_data('dart', 'disc_list', columns = '접수번호', orderby_cols = '접수번호', where = where)['접수번호']

        
        for idx, rcept_no in enumerate(rcept_list):
            logger.info(f"'{rcept_no}' doc upload starts! ({idx+1}/{len(rcept_list)})")
        
            res = None
            while res is None or '사용한도를 초과' in res.text:
                try:
                    res = self.api_conn.get_api_data(self.conf[self.sub][detail]['detail_url'], params = {'rcept_no': rcept_no}, data_type = 'xml')
                    
                    file = zipfile.ZipFile(
                                io.BytesIO(res.content))
            
                except Exception as e:
                    if res is not None and '사용한도를 초과' in res.text:
                        self.api_conn.chg_auth_key()
                    logger.warning(e)

            if '파일이 존재' in res.text:
                logger.warning(f"There doesn't exist rcept_no: {rcept_no}; skip this report.")
                continue
        
            data = pd.DataFrame([[_ts, rcept_no, file_name, BeautifulSoup(file.read(file_name), features = 'xml').prettify()] for file_name in file.namelist()], columns = ['_ts', '접수번호', '파일이름', '파일내용'])

            try:
                self.db_conn.insert_df(data,
                                    self.conf['schema_name'],
                                    self.conf[self.sub][detail]['table_name'])

            except:
                logger.error(f"error file: {rcept_no}")

    def upload_xbrl_taxo(self):
        fn_types = ['BS1', 'BS2', 'BS3', 'BS4', 
                    'IS1', 'IS2', 'IS3', 'IS4',
                    'CIS1', 'CIS2', 'CIS3', 'CIS4',
                    'DCIS1', 'DCIS2', 'DCIS3', 'DCIS4',
                    'DCIS5', 'DCIS6', 'DCIS7', 'DCIS8',
                    'CF1', 'CF2', 'CF3', 'CF4',
                    'SCE1', 'SCE2']

        for fn_type in fn_types:
            data = self.api_conn.get_data(self.conf[self.sub]['xbrl_taxonomy']['detail_url'],
                             params = {'sj_div': fn_type},
                             rename = self.conf[self.sub]['xbrl_taxonomy']['rename'])
            
            data = self.db_conn.ext_notin_db(data, self.conf['schema_name'], self.conf[self.sub]['xbrl_taxonomy']['table_name'], subset = ['재무제표구분', '계정id'])
            
            self.db_conn.insert_df(data, self.conf['schema_name'], self.conf[self.sub]['xbrl_taxonomy']['table_name'])

    def upload_sgl_acc_all(self):
        detail = 'fnltt_singl_acnt_all'
        logger.info(f"{'#' * 15} Starts {self.conf[self.sub][detail]['table_name']} upload! {'#' * 15}")
        corp_codes = self.check_corp_list(detail)


        for corp_idx, corp_code in enumerate(corp_codes):
            logger.info(f"data upload starts for '{corp_code}'({corp_idx+1}/{len(corp_codes)})")
            cnt = 0
            corp_data = pd.DataFrame()


            for rep_idx, report_info in enumerate(self.report_type):
                logger.debug(f"Upload report type: '{report_info[1]}' ({rep_idx+1}/{len(self.report_type)}).")
                target_years = super().get_upload_target_year(detail, corp_code, report_info)
                target_years = [year for year in target_years if year >= 2015]

                for yr_idx, year in enumerate(target_years):
                    logger.debug(f"Upload {year} starts! ({yr_idx+1}/{len(target_years)})")

                    for idx, fs_div in enumerate(['OFS', 'CFS']):

                        try:
                            params = {'corp_code': corp_code, 'bsns_year': year, 'reprt_code': report_info[1], 'fs_div': fs_div}
                            data = self.api_conn.get_data(self.conf[self.sub][detail]['detail_url'], 
                                        rename = self.conf[self.sub][detail]['rename'],
                                        params = params)
                
                        except Exception as e:
                            if isinstance(e.args[0], dict) and e.args[0]['status'] == '013':
                                logger.warning(f"There is some error in {detail}, params: {params}")
                                logger.warning(e)
                                continue
                            raise Exception(e)
                    
                        
                        data['사업연도'] = year
                        data['보고서코드'] = report_info[1]
                        data['개별연결구분'] = fs_div
                        
                        self.processing_cols(data, self.conf[self.sub][detail])
                        corp_data = pd.concat([corp_data, data])

            if corp_data.shape[0] > 0:
                self.db_conn.upsert(corp_data,
                                    self.conf['schema_name'], 
                                    table_name = self.conf[self.sub][detail]['table_name'])



            super()._write_history(table_name = self.conf[self.sub][detail]['table_name'],
                           corp_code = corp_code)


class Equity_processor(Base_processor):
    def __init__(self, db_conn, api_conn, conf, sub = 'eq'):
        logger.info('Initialize business report data processer!')
        super().__init__(db_conn, api_conn, conf, sub)
        
        self.corp_codes = db_conn.get_data(schema_name = conf['schema_name'], 
                    table_name = conf['disc']['corp_code']['table_name'],
                    columns = ['고유번호'],
                    orderby_cols = '고유번호').to_numpy().ravel()

        logger.info(f"There are {len(self.corp_codes)} corp_codes in db.")


    def check_corp_list(self, detail):
        db_history = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['history_table_name'],
                        columns = ['고유번호', 'latest_ins_date'],
                        where = [f"테이블이름='{self.conf[self.sub][detail]['table_name']}'"],
                        )

        report_list = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['disc']['list']['table_name'],
                        columns = ['고유번호', '접수일자'],
                        where = [f"보고서명 LIKE '%%{self.conf[self.sub][detail]['report_name']}%%'"],
                        )

        latest_report_date = report_list.groupby('고유번호')['접수일자'].max().reset_index()
        merge_data = latest_report_date.merge(db_history, on = '고유번호', how = 'left')
        corp_idx = merge_data.apply(lambda x: x['접수일자'] >= x['latest_ins_date'] if not pd.isna(x['latest_ins_date']) else True , axis = 1)
        corp_idx &= merge_data['접수일자'] >= datetime(self.conf['api_report_start_year'], 1, 1).date()

        logger.info(f"Run only for corp_code not in DB: (nums: {corp_idx.sum()})")
        return merge_data.loc[corp_idx, '고유번호'].to_numpy().ravel()

    def func(self, detail):
        logger.info(f"{'#' * 15} Starts {self.conf[self.sub][detail]['table_name']} upload! {'#' * 15}")
        corp_codes = self.check_corp_list(detail)


        for corp_idx, corp_code in enumerate(corp_codes):
            logger.info(f"data upload starts for '{corp_code}'({corp_idx+1}/{len(corp_codes)})")


            try:
                params = {'corp_code': corp_code}
                data = self.api_conn.get_data(self.conf[self.sub][detail]['detail_url'], 
                            rename = self.conf[self.sub][detail]['rename'],
                            params = params)
    
            except Exception as e:
                if isinstance(e.args[0], dict) and e.args[0]['status'] == '013':
                    logger.warning(f"There is some error in {detail}, params: {params}")
                    logger.warning(e)
                    super()._write_history(table_name = self.conf[self.sub][detail]['table_name'],
                           corp_code = corp_code)
                    continue
                
                else:
                    raise Exception(e)
                    
            self.processing_cols(data, self.conf[self.sub][detail])
    
            if data.shape[0] > 0:
                self.db_conn.upsert(data,
                                    self.conf['schema_name'], 
                                    table_name = self.conf[self.sub][detail]['table_name'])



            super()._write_history(table_name = self.conf[self.sub][detail]['table_name'],
                           corp_code = corp_code)



class keymatter_processor(Base_processor):
    def __init__(self, db_conn, api_conn, conf, sub = 'km'):
        logger.info('Initialize key matter report data processer!')
        super().__init__(db_conn, api_conn, conf, sub)
        
        self.corp_codes = db_conn.get_data(schema_name = conf['schema_name'], 
                    table_name = conf['disc']['corp_code']['table_name'],
                    columns = ['고유번호'],
                    orderby_cols = '고유번호').to_numpy().ravel()

        logger.info(f"There are {len(self.corp_codes)} corp_codes in db.")


    def check_corp_list(self, detail):
        report_names = self.conf[self.sub][detail]['report_name']
        report_names = [report_names] if isinstance(report_names, str) else report_names
        db_history = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['history_table_name'],
                        columns = ['고유번호', 'latest_ins_date'],
                        where = [f"테이블이름='{self.conf[self.sub][detail]['table_name']}'"],
                        )

        report_list = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['disc']['list']['table_name'],
                        columns = ['고유번호', '접수일자'],
                        where = [f"보고서명 LIKE '%%{report_name}%%'" for report_name in report_names],
                        where_operator = 'OR',
                    is_distinct = True, orderby_cols = ['고유번호']
                        )
        


        merge_data = report_list.merge(db_history, on = '고유번호', how = 'left')
        corp_idx = merge_data.apply(lambda x: x['접수일자'] >= x['latest_ins_date'] if not pd.isna(x['latest_ins_date']) else True , axis = 1)
        corp_idx &= merge_data['접수일자'] >= datetime(self.conf['api_report_start_year'], 1, 1).date()
        final_data = merge_data.loc[corp_idx, ['고유번호', '접수일자']].reset_index(drop = True)
        logger.info(f"Run only for corp_code not in DB: (nums: {final_data.shape[0]})")
        return final_data

    def func(self, detail):
        logger.info(f"{'#' * 15} Starts {self.conf[self.sub][detail]['table_name']} upload! {'#' * 15}")
        report_list = self.check_corp_list(detail)
        corp_list = report_list.loc[:, '고유번호'].to_numpy().ravel()


        for report_idx, report_info in report_list.iterrows():
            corp_code, date = report_info
            logger.info(f"data upload starts for '{corp_code}'({report_idx+1}/{report_list.shape[0]})")


            try:
                params = {'corp_code': corp_code,
                         'bgn_de': date,
                         'end_de': date}
                
                data = self.api_conn.get_data(self.conf[self.sub][detail]['detail_url'],
                                              rename = self.conf[self.sub][detail]['rename'],
                                              params = params)
    
            except Exception as e:
                if isinstance(e.args[0], dict) and e.args[0]['status'] == '013':
                    logger.warning(f"There is some error in {detail}, params: {params}")
                    logger.warning(e)
                    if corp_code not in corp_list[report_idx+1:]:
                        super()._write_history(table_name = self.conf[self.sub][detail]['table_name'],
                           corp_code = corp_code)
                    continue
                
                else:
                    raise Exception(e)
            # return data
            self.processing_cols(data, self.conf[self.sub][detail])
            # return data

            if data.shape[0] > 0:
                self.db_conn.upsert(data,
                                    self.conf['schema_name'], 
                                    table_name = self.conf[self.sub][detail]['table_name'])

            if corp_code not in corp_list[report_idx+1:]:
                super()._write_history(table_name = self.conf[self.sub][detail]['table_name'],
                           corp_code = corp_code)


class Regist_processor(Base_processor):
    def __init__(self, db_conn, api_conn, conf, sub = 'rs'):
        logger.info('Initialize registration report data processer!')
        super().__init__(db_conn, api_conn, conf, sub)
        
        self.corp_codes = db_conn.get_data(schema_name = conf['schema_name'], 
                    table_name = conf['disc']['corp_code']['table_name'],
                    columns = ['고유번호'],
                    orderby_cols = '고유번호').to_numpy().ravel()

        logger.info(f"There are {len(self.corp_codes)} corp_codes in db.")


    def check_corp_list(self, detail):
        db_history = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['history_table_name'],
                        columns = ['고유번호', 'latest_ins_date'],
                        where = [f"테이블이름='{self.conf[self.sub][detail]['table_name']}'"],
                        )

        report_list = self.db_conn.get_data(self.conf['schema_name'], 
                    table_name = self.conf['disc']['list']['table_name'],
                        columns = ['고유번호', '접수일자'],
                        where = [f"보고서명 LIKE '%%{self.conf[self.sub][detail]['report_name']}%%'"],
                    is_distinct = True, orderby_cols = ['고유번호']
                        )
        


        merge_data = report_list.merge(db_history, on = '고유번호', how = 'left')
        corp_idx = merge_data.apply(lambda x: x['접수일자'] >= x['latest_ins_date'] if not pd.isna(x['latest_ins_date']) else True , axis = 1)
        corp_idx &= merge_data['접수일자'] >= datetime(self.conf['api_report_start_year'], 1, 1).date()
        final_data = merge_data.loc[corp_idx, ['고유번호', '접수일자']].reset_index(drop = True)
        logger.info(f"Run only for corp_code not in DB: (nums: {final_data.shape[0]})")
        return final_data

    def func(self, detail):
        logger.info(f"{'#' * 15} Starts {self.conf[self.sub][detail]['table_name']} upload! {'#' * 15}")
        report_list = self.check_corp_list(detail)
        corp_list = report_list.loc[:, '고유번호'].to_numpy().ravel()


        for report_idx, report_info in report_list.iterrows():
            corp_code, date = report_info
            logger.info(f"data upload starts for '{corp_code}'({report_idx+1}/{report_list.shape[0]})")


            try:
                params = {'corp_code': corp_code,
                         'bgn_de': date,
                         'end_de': date}
                
                data = self.api_conn.get_data(self.conf[self.sub][detail]['detail_url'],
                                              content_key = 'group',
                            params = params).T
    
            except Exception as e:
                if isinstance(e.args[0], dict) and e.args[0]['status'] == '013':
                    logger.warning(f"There is some error in {detail}, params: {params}")
                    logger.warning(e)
                    if corp_code not in corp_list[report_idx+1:]:
                        super()._write_history(table_name = self.conf[self.sub][detail]['table_name'],
                           corp_code = corp_code)
                    continue
                
                else:
                    raise Exception(e)

            data.columns = data.loc['title', :]

            data['_ts'] = data.loc['_ts', :].iloc[0]
            data['고유번호'] = corp_code
            data['접수일자'] = date

            data = data.loc['list']

            
            for group in self.conf[self.sub][detail]['group']:
                content = pd.DataFrame(data[group]).rename(columns = self.conf[self.sub][detail]['rename'][group])
                
                this_conf = {key: self.conf[self.sub][detail][key][group] 
                             for key in self.conf[self.sub][detail].keys() 
                             if isinstance(self.conf[self.sub][detail][key], dict) and group in self.conf[self.sub][detail][key]}
                
                self.processing_cols(content, this_conf)

                data[group] = content.to_json(orient = 'records', force_ascii = False)

            data = pd.DataFrame(data).T

            if data.shape[0] > 0:
                self.db_conn.upsert(data,
                                    self.conf['schema_name'], 
                                    table_name = self.conf[self.sub][detail]['table_name'])

            if corp_code not in corp_list[report_idx+1:]:
                super()._write_history(table_name = self.conf[self.sub][detail]['table_name'],
                           corp_code = corp_code)