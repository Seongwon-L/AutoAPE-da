# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
from dataanalyzer.analyzer.TableDatasetMeta import TableDatasetMeta
from dataanalyzer.common.Constants import Constants
from dataanalyzer.info.DAJobInfo import DAJobInfo
from dataanalyzer.util.sftp.PySFTPClient import PySFTPClient
from dataanalyzer.analyzer.DatasetMeta import DatasetMeta


class DataLoader(object):
    def __init__(self, job_info: DAJobInfo, sftp_client: PySFTPClient, mrms_sftp_client: PySFTPClient):
        self.job_info: DAJobInfo = job_info
        self.sftp_client: PySFTPClient = sftp_client
        self.mrms_sftp_client: PySFTPClient = mrms_sftp_client
        self.dataset_meta: DatasetMeta = DatasetMeta()
        self.num_worker: int = 1

    def load(self):
        raise NotImplementedError

    def get_num_worker(self) -> int:
        return self.num_worker

    def get_meta(self) -> DatasetMeta:
        return self.dataset_meta

    def global_meta(self):
        raise NotImplementedError
