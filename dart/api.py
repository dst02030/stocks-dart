import logging
import json
import requests
import io
import os
import time
import zipfile


import numpy as np
import pandas as pd

from io import BytesIO
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)




class Dart_main_api:
    def __init__(self, auth_key, max_rows = 100, max_date = 90, data_type = "json", max_api_retries = 30):
        logger.info(f"### dart main api is initialized! ###")
        self.title_url = "https://opendart.fss.or.kr/api"
        self.max_rows = max_rows if max_rows else 100
        self.max_date = max_date if max_date else 90
        self.data_type = data_type if data_type else 'json'
        self.params = {
        'crtfc_key': auth_key,
        'page_count': self.max_rows
        }
        self.max_api_retries = max_api_retries
        self.api_call = 0

        # 나중에 제거
        self.auth_list = ['cdf5844c1c5d830d5a8a7742bb42bf85ebb2d743', '80e3f01e10bb3263558e82dc40ff0558e3d22afd',
                    'bc7d6a119b2d5f27127c8146489fed71fdea8254', '44dafac39127a5c0a626c140b5fca7e3e4ad955b',
                    'd3e570d43d8054f8795cfb744f6bf1497336231f', '0591085ea8208d99a64fc63a9d23a8c1a1c7b9a0',
                    'a93018f782c7df2dfb124ebf27a04440cd5ed49e', '500d6451fbdd36bde7b815efb75863acb88fa6bc']

        self.auth_list = [auth for auth in self.auth_list if auth != auth_key]


    def get_data(self, detail_url, params = {}, data_type = None, rename = None, _ts = datetime.astimezone(datetime.now()), is_zip = False, content_key = 'list'):
        logger.debug(f"### {detail_url} data call starts! ###")
        
        
        page, total_page = 0, 1
        data = pd.DataFrame()
        
        while total_page > page:
            page += 1
            params.update({'page_no': page})
    
            for _ in range(self.max_api_retries):
                try:
                    res = self.get_api_data(detail_url, params, data_type)
                    break
                
                except Exception as e:
                    logger.warning(e)
                    logger.warning(f"data re-load would be start... ({_+1}/{self.max_api_retries})")
                    time.sleep(5)
                    
                if _ + 1 == self.max_api_retries:
                    logger.error(e)
                    raise e

            
            if is_zip:
                data = self._read_zipfile(res)
                break
            
            api_results = json.loads(
                res.text
                )

            # 나중에 제거
            while api_results is None or api_results['status'] == '020':
                self.chg_auth_key()
                res = self.get_api_data(detail_url, params, data_type)
                api_results = json.loads(
                res.text
                )
            
            if api_results['status'] != '000':
                logger.error(api_results)
                raise Exception(api_results)

            total_page = api_results['total_page'] if 'total_page' in api_results else 1
                
            this_data = pd.DataFrame(api_results[content_key] if content_key in api_results else [api_results])
            
            data = pd.concat([data, this_data])
            logger.debug(f"data page load finished: ({page}/{total_page}).")
        
        data['_ts'] = _ts

        if rename:
            rename = {key: val for key, val in rename.items() if key in data.columns}
            data.rename(columns = rename, inplace = True)
        
        return data.replace('', pd.NA)
        
    
    def get_api_data(self, detail_url, params = {}, data_type = None, timeout = 3):
        params.update(self.params)
        params = [f"{key}={val}" for key, val in params.items()]
        params_url = "&".join(params)
        data_type = data_type if data_type else self.data_type

        self.api_call += 1
        res = requests.get(f"{self.title_url}/{detail_url}.{data_type}?{params_url}")
        res.raise_for_status()

        if self.api_call % 100 == 0:
            logger.info(f"API call nums: {self.api_call}")
        
        return res
    
    
    
    def _read_zipfile(self, res, to_df = True):
        file = zipfile.ZipFile(
            io.BytesIO(res.content))

        if to_df:
            return pd.read_xml(file.read(file.filelist[0]))
        return file.read(file.filelist[0])

    def chg_auth_key(self): # 나중에 제거
        logger.warning("Available API call num exceeds. Change your auth_key")
        self.params['crtfc_key'] = self.auth_list.pop()
        self.api_call = 0
        logger.warning(f"Remaining auth keys: {len(self.auth_list)}")