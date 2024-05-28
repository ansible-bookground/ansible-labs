#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import time
import requests

DOCUMENTATION = r'''
---
module: url_checker
short_description: Checks the availability of a URL.
version_added: "1.0.0"
description: This module checks if a given URL is available by making HTTP GET requests.
options:
  url:
    description: The URL to check.
    required: true
    type: str
  interval:
    description: The interval between each request in seconds.
    required: true
    type: int
  count:
    description: The number of requests to send.
    required: true
    type: int
author:
  - Tempei ono
'''

EXAMPLES = r'''
# Basic example
- name: Check URL availability
  namespace.web.url_checker:
    url: "http://example.com"
    interval: 10
    count: 3
'''


def main():
    module_args = dict(
        url=dict(type='str', required=True),
        interval=dict(type='int', required=True),
        count=dict(type='int', required=True)
    )

    result = dict(
        changed=False,
        success_count=0,
        failure_count=0
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    url = module.params['url']
    interval = module.params['interval']
    count = module.params['count']

    for _ in range(count):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                result['success_count'] += 1
            else:
                result['failure_count'] += 1
        except requests.RequestException:
            result['failure_count'] += 1

        time.sleep(interval)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
