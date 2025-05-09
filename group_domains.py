import json
from collections import defaultdict

def group_subdomains_by_ip(input_file, output_file=None):
    """
    Reads a JSON file of subdomains with IPs and groups the subdomains by IP address.

    :param input_file: Path to the JSON file (list of dicts with 'subdomain' and 'ip').
    :param output_file: Optional path to write grouped results as JSON.
    """
    # Load data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Grouping
    groups = defaultdict(list)
    for entry in data:
        ip = entry.get('ip')
        subdomain = entry.get('subdomain')
        if ip and subdomain:
            # Clean whitespace
            subdomain = subdomain.strip()
            groups[ip].append(subdomain)

    # Optionally write to output file
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(groups, f, indent=4)
        print(f"Grouped data written to {output_file}")

    # Print grouped results
    for ip, subs in groups.items():
        print(f"{ip}:")
        for sub in subs:
            print(f"  - {sub}")
        print()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Group subdomains by IP address from a JSON file."
    )
    parser.add_argument(
        "input",
        help="Path to the JSON input file containing subdomain entries."
    )
    parser.add_argument(
        "--output", "-o",
        help="Optional output file path for grouped JSON results.",
        default=None
    )
    args = parser.parse_args()
    group_subdomains_by_ip(args.input, args.output)