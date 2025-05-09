#!/usr/bin/env python3
import os
import time
import requests
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Download a sequence of images following a numeric filename scheme"
    )
    parser.add_argument(
        "-b", "--base-url",
        default="https://wwwhomes.uni-bielefeld.de/bildwis/bigImages/",
        help="Base URL for images (must end with a slash)"
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=660,
        help="Total number of images to download"
    )
    parser.add_argument(
        "-o", "--output",
        default="images",
        help="Directory where downloaded images will be saved"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=1.0,
        help="Delay in seconds between each download request"
    )
    # Add optional auth header (Basic)
    parser.add_argument(
        "-a", "--auth",
        default="Basic YmtnOmJrZ3Bhc3N3b3Jk",
        help="Authorization header value (Basic ...)"
    )
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output, exist_ok=True)

    headers = {
        "Authorization": args.auth
    }

    for i in range(445, args.count + 1):
        filename = f"{i:03d}.jpg"
        url = args.base_url + filename
        output_path = os.path.join(args.output, filename)

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        except requests.HTTPError as e:
            print(f"Failed to download {filename}: {e}")

        time.sleep(args.delay)


if __name__ == "__main__":
    main()
