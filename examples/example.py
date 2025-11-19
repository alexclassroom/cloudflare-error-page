#!/usr/bin/env python3

import os
import sys
import webbrowser

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cloudflare_error_page import render as render_cf_error_page

error_page = render_cf_error_page({
    'browser_status': {
        "status": 'ok',
    },
    'cloudflare_status': {
        "status": 'error',
        "status_text": 'Not Working',
    },
    'host_status': {
        "status": 'ok',
        "location": 'example.com',
    },
    'error_source': 'cloudflare',  # 'browser', 'cloudflare', or 'host'

    'what_happened': '<p>There is an internal server error on Cloudflare\'s network.</p>',
    'what_can_i_do': '<p>Please try again in a few minutes.</p>',
})

with open('error.html', 'w') as f:
    f.write(error_page)

webbrowser.open('error.html')