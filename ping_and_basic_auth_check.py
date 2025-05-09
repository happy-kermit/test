#!/usr/bin/env python3
"""
Check specific hrz.uni-bielefeld.de subdomains for the presence of /robots.txt,
printing HTTP response codes to the console and collecting domains with Accessible robots.txt.

Usage:
    python check_robots.py subdomains.json -o robots_urls.json

Positional Arguments:
  input       Path to JSON file containing subdomain entries (list of dicts with 'subdomain').

Optional Arguments:
  -o, --output
              Path to output JSON file for URLs where /robots.txt is present (default: robots_urls.json).
  -d, --delay
              Delay in seconds between each HTTP request (default: 1.0).
  -t, --timeout
              Timeout in seconds for each HTTP request (default: 3.0).
"""
import json
import argparse
import time
from urllib.parse import urljoin
from requests import Session, RequestException

SUPPORTED_SUFFIX = 'hrz.uni-bielefeld.de'
PATH_SUFFIX = '/robots.txt'


def main(input_file, output_file, delay, timeout):
    # Load JSON list of subdomain entries
    with open(input_file, 'r', encoding='utf-8') as f:
        entries = json.load(f)

    # Filter and build robots.txt URLs
    urls_to_check = []
    for entry in entries:
        if isinstance(entry, dict) and 'subdomain' in entry:
            domain = entry['subdomain'].strip()
            if domain.endswith(SUPPORTED_SUFFIX):
                base = domain if domain.startswith(('http://', 'https://')) else f'http://{domain}'
                full_url = urljoin(base.rstrip('/') + '/', PATH_SUFFIX.lstrip('/'))
                urls_to_check.append(full_url)

    session = Session()
    robots_urls = []

    # Check each robots.txt URL
    for url in urls_to_check:
        try:
            resp = session.get(url, timeout=timeout, allow_redirects=False)
            code = resp.status_code
            label = 'FOUND' if code == 200 else 'NOT_FOUND'
            print(f"{url}: {code} {label}")
            if code == 200:
                robots_urls.append(url)
        except RequestException as e:
            print(f"{url}: ERROR ({e})")
        time.sleep(delay)

    # Write accessible robots.txt URLs to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'robots_txt_urls': robots_urls}, f, indent=4)

    print(f"\nWritten {len(robots_urls)} URLs with robots.txt to {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Check hrz.uni-bielefeld.de subdomains for /robots.txt presence.',
        epilog='Example: python check_robots.py subdomains.json -o robots_urls.json',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Path to JSON file with subdomain entries (list of dicts with \'subdomain\').'
    )
    parser.add_argument(
        '-o', '--output',
        default='robots_urls.json',
        help='Output JSON file for URLs with robots.txt (JSON).'
    )
    parser.add_argument(
        '-d', '--delay',
        type=float,
        default=1.0,
        help='Delay in seconds between requests (default: 1.0).'
    )
    parser.add_argument(
        '-t', '--timeout',
        type=float,
        default=3.0,
        help='Timeout in seconds for each request (default: 3.0).'
    )
    args = parser.parse_args()
    main(args.input, args.output, args.delay, args.timeout)
    # Example usage:
    # python check_robots.py subdomains.json -o robots_urls.json -d 1.0 -t 3.0
    # python check_robots.py subdomains.json -o robots_urls.json -d 0.5 -t 2.0