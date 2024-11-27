from celery import shared_task
from flask import current_app
import asyncio

def get_engines_for_asset(asset):
    return current_app.config.get({
        'ip': 'IP_ENGINES',
        'domain': 'DOMAIN_ENGINES',
        'path': 'DOMAIN_ENGINES',
        'fqdn': 'DOMAIN_ENGINES',
        'ip-range': 'IP_RANGE_ENGINES',
        'ip-subnet': 'IP_SUBNET_ENGINES',
        'url': 'URL_ENGINES',
        'keyword': 'OTHER_ENGINES',
        'person': 'OTHER_ENGINES',
        'organisation': 'OTHER_ENGINES',
        'application': 'OTHER_ENGINES'
    }.get(asset['datatype'], []))

async def run_engine(engine, scan_id, asset_value, report_folder):
    await asyncio.to_thread(engine, scan_id, asset_value, report_folder)

@shared_task
def start_scan_job(scan_id, asset, report_folder):
    engines = get_engines_for_asset(asset)
    if not engines:
        return True
    asyncio.run(run_scan_job(engines, scan_id, asset, report_folder))
    return True

async def run_scan_job(engines, scan_id, asset, report_folder):
    tasks = [run_engine(engine, scan_id, asset['value'], report_folder) for engine in engines]
    await asyncio.gather(*tasks)
