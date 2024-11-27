from redis_om import Field, HashModel
from time import time
from typing import Optional


class TaskModel(HashModel):
    scan_id: str = Field(index=True)
    asset_value: str
    asset_type: str
    job_id: str
    report_sent: str = 'false'
    started_at: int = int(time() * 1000)