import json
import os

from cloudflare_error_page import ErrorPageParams
from flask import request

from . import root_dir


loc_data: dict = None

def read_loc_file(path: str):
    try:
        with open(os.path.join(root_dir, path)) as f:
            return json.load(f)
    except:
        return


def get_cf_location(loc: str):
    global loc_data
    loc = loc.upper()
    if loc_data is None:
        loc_data = read_loc_file('editor/server/cf-colos.json')
    if loc_data is None:
        # From https://github.com/Netrvin/cloudflare-colo-list/blob/main/DC-Colos.json
        loc_data = read_loc_file('editor/server/cf-colos.bundled.json')
    if loc_data is None:
        return
    data: dict = loc_data.get(loc)
    if not data:
        return
    return data.get('city')


def fill_cf_template_params(params: ErrorPageParams):
    # Get the real Ray ID / data center location from Cloudflare header
    ray_id_loc = request.headers.get('Cf-Ray')
    if ray_id_loc:
        params['ray_id'] = ray_id_loc[:16]

        cf_status = params.get('cloudflare_status')
        if cf_status is None:
            cf_status = params['cloudflare_status'] = {}
        if not cf_status.get('location'):
            loc = get_cf_location(ray_id_loc[-3:])
            if loc:
                cf_status['location'] = loc

    # Get the real client ip from remote_addr
    # If this server is behind proxies (e.g CF CDN / Nginx), make sure to set 'BEHIND_PROXY'=True in app config. Then ProxyFix will fix this variable
    # using X-Forwarded-For header from the proxy.
    params['client_ip'] = request.remote_addr


def sanitize_user_link(link: str):
    link = link.strip()
    link_lower = link
    if link_lower.startswith('http://') or link_lower.startswith('https://'):
        return link
    if '.' in link or '/' in link:
        return 'https://' + link
    return '#' + link


def sanitize_page_param_links(param: ErrorPageParams):
    more_info = param.get('more_information')
    if more_info:
        link = more_info.get('link')
        if link:
            more_info['link'] = sanitize_user_link(link)
    perf_sec_by = param.get('perf_sec_by')
    if perf_sec_by:
        link = perf_sec_by.get('link')
        if link:
            perf_sec_by['link'] = sanitize_user_link(link)
