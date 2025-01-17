# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
from typing import Dict, List

from dataanalyzer.core.analyzer.DatasetMetaAbstract import DatasetMetaAbstract
from dataanalyzer.core.analyzer.table.numeric.LocalStatistics import LocalStatistics
from dataanalyzer.common.Constants import Constants
from dataanalyzer.info.DAJobInfo import DAJobInfo


class TableDatasetMetaWorker(DatasetMetaAbstract):
    COMMON_KEYS = ["unique"]
    LOCAL_KEYS = ["local"]

    def __init__(self):
        DatasetMetaAbstract.__init__(self)
        self.meta_func_list: List[Dict] = list()

    def initialize(self, job_info: DAJobInfo, meta_json: Dict = None):
        self.meta_list: List[Dict] = meta_json.get("meta", list())

        for idx, _ in enumerate(self.meta_list):
            self.meta_func_list.append(self._initialize_meta_functions(job_info, _))
            _["statistics"] = dict()

    def _initialize_meta_functions(self, job_info: DAJobInfo, meta) -> Dict:
        field_type = meta.get("field_type")
        if field_type == Constants.FIELD_TYPE_INT or field_type == Constants.FIELD_TYPE_FLOAT:
            local_statistic = LocalStatistics()
            local_statistic.initialize(
                job_info.get_instances(), float(meta.get("statistics").get("basic").get("mean")))
            return {
                "local": local_statistic,
            }
        else:
            return {}

    def apply(self, data):
        for idx, fd in enumerate(self.meta_list):
            result, f_type = DatasetMetaAbstract.field_type(data.get(fd.get("field_nm")))

            # numeric
            if fd.get("field_type") == Constants.FIELD_TYPE_INT or fd.get("field_type") == Constants.FIELD_TYPE_FLOAT:
                if f_type is Constants.FIELD_TYPE_INT or f_type is Constants.FIELD_TYPE_FLOAT:
                    for _key in self.LOCAL_KEYS:
                        self.meta_func_list[idx].get(_key).apply(result)

    def calculate(self):
        for idx, meta in enumerate(self.meta_list):
            if meta.get("field_type") == Constants.FIELD_TYPE_INT or \
                    meta.get("field_type") == Constants.FIELD_TYPE_FLOAT:
                for _key in self.LOCAL_KEYS:
                    self.meta_func_list[idx].get(_key).calculate()

    def get_meta_list(self) -> List[dict]:
        return self.get_meta_list_for_worker()
