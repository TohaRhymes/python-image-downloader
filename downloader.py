import concurrent.futures
import os
import urllib.request
from hashlib import md5
from time import time
from tqdm import tqdm
import argparse

FILE = None
DESTINATION = None
WORKERS = None
VERBOSE = None
POST_PROCESSING = None


def parse_args() -> (str, str, int, bool, bool):
    parser = argparse.ArgumentParser()

    parser.add_argument("-in", "--file", help="File with links to image.", type=str)
    parser.add_argument("-out", "--out_dir", help="Output directory.", type=str)
    parser.add_argument("-wrks", "--workers", help="Amount of python workers (python threads work in parallel).",
                        type=int)
    parser.add_argument("-vb", "--verbose", help="Verbosity of the output.", type=bool,
                        action=argparse.BooleanOptionalAction)
    parser.add_argument("-pp", "--postprocessing", help="Make post-processing?", type=bool,
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    return args.file, args.out_dir, args.workers, args.verbose, args.postprocessing


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        if VERBOSE:
            print(f'Made directory: {directory}')
    else:
        if VERBOSE:
            print(f'Using existing directory: {directory}')


def check(url: str):
    return not url.startswith('//')


def get_urls_from_file(file):
    try:
        with open(file, 'r') as links_f:
            urls = [l for l in links_f.read().split('\n') if check(l)]
        return urls
    except (FileNotFoundError, FileExistsError):
        print('Can\'t find file to parse.')
        return list()


def download_image(url, destination_template, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        data = response.read()
        ext = response.info().get_content_subtype()
        with open(destination_template.format(f'{md5(data).hexdigest()}.{ext}'), "wb") as img_file:
            img_file.write(data)


def download(workers, destination, urls):
    t = time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        # Start the load operations and mark each future with its URL
        dest = os.path.join(destination, '{}')
        future_to_url = {executor.submit(download_image, url, dest, 60): url for url in urls}
        successes = 0
        errors = 0
        for future in tqdm(concurrent.futures.as_completed(future_to_url)):
            url = future_to_url[future]
            try:
                future.result()
                successes += 1
            except Exception as exc:
                errors += 1
                if VERBOSE:
                    print('%r generated an exception: %s' % (url, exc))
    print(f'Download finished (errors: {errors}, successes: {successes}).\nTotal time of downloading: {time() - t}')


def make_post_processing_of_file(file):
    """Count sum of squared bytes in file"""
    counter = 0
    with open(file, 'rb') as f:
        byte = f.read(1)
        while byte != b"":
            counter += int.from_bytes(byte, "big") ** 2
            byte = f.read(1)
    return counter


def make_post_processing(workers, destination):
    t = time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        dest = os.path.join(destination, '{}')
        future_to_url = {executor.submit(make_post_processing_of_file, dest.format(file)): file for file in
                         os.listdir(destination)}
        for future in tqdm(concurrent.futures.as_completed(future_to_url)):
            sum_squared_bytes = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                if VERBOSE:
                    print('%r generated an exception: %s' % (sum_squared_bytes, exc))
    print(f'Post processing finished, total time: {time() - t}')


def main():
    FILE, DESTINATION, WORKERS, VERBOSE, POST_PROCESSING = parse_args()
    urls = get_urls_from_file(FILE)
    t = time()
    if len(urls) < 1:
        print("Can't find any strings in file, try again.")
        return None
    make_dir(DESTINATION)
    download(WORKERS, DESTINATION, urls)
    if POST_PROCESSING:
        make_post_processing(WORKERS, DESTINATION)
    print(f'Program finished, total time: {time() - t}')


if __name__ == '__main__':
    main()
