import concurrent.futures
import os
import urllib.request
from time import time
from tqdm import tqdm

FILE = 'data/images2.txt'
WORKERS = 50
DESTINATION = 'im'
VERBOSE = 1


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


def download_images(url, i, destination_template, timeout):
    data = urllib.request.urlopen(url, timeout=timeout).read()
    with open(destination_template.format(i), "wb") as img_file:
        img_file.write(data)


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        if VERBOSE:
            print(f'Made directory: {directory}')
    else:
        if VERBOSE:
            print(f'Using existing directory: {directory}')


def download(workers, destination, urls):
    t = time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        # Start the load operations and mark each future with its URL
        dest = os.path.join(destination, '{}')
        future_to_url = {executor.submit(download_images, url, i, dest, 60): url for i, url in enumerate(urls)}
        for future in tqdm(concurrent.futures.as_completed(future_to_url)):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                if VERBOSE:
                    print('%r generated an exception: %s' % (url, exc))
    print(f'Download finished, total time: {time() - t}')


# for file in os.listdir(directory):
def make_post_processing_of_file(file):
    '''Count sum of squared bytes in file'''
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
    urls = get_urls_from_file(FILE)
    t = time()
    if len(urls) < 1:
        print("Can't find any strings in file, try again.")
        return None
    make_dir(DESTINATION)
    download(WORKERS, DESTINATION, urls)
    make_post_processing(WORKERS, DESTINATION)
    print(f'Program finished, total time: {time() - t}')


if __name__ == '__main__':
    main()
