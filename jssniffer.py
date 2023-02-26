# jssniffer 1.0 2023
# Author : Alessio M
# https://github.com/CptAlessio/jssniffer

import os
import requests
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# print list of javascript files the website is using
outputfoundfiles = True


# function to get all JavaScript files on a page
def get_js_files(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        js_files = set()

        # find all script tags
        for script in soup.find_all("script"):
            src = script.get("src")
            if src and src.endswith(".js"):
                js_files.add(src)

        return js_files

    except Exception as e:
        print(f"Error getting JS files for {url}: {str(e)}")
        return set()


# function to crawl a website
def crawl_website(websiteurl):
    visited = set()
    js_files = set()
    queue = [websiteurl]

    while queue:
        # get next page to visit from queue
        websiteurl = queue.pop(0)

        # check if page has already been visited
        if websiteurl in visited:
            continue

        try:
            domain = urlparse(websiteurl).netloc
            page_js_files = get_js_files(websiteurl)

            js_files.update(page_js_files)
            visited.add(websiteurl)
            print(".", end="", flush=True)

            # find all links on the page
            response = requests.get(websiteurl)
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all("a")

            # add links to queue
            for link in links:
                href = link.get("href")
                if href:
                    # resolve relative URLs
                    href = urljoin(websiteurl, href)

                    # check if link is on the same domain and hasn't been visited
                    if urlparse(href).netloc == domain and href not in visited:
                        queue.append(href)

        except Exception as e:
            print(f"\nError crawling website {websiteurl}: {str(e)}")

    # print the list of JavaScript files found
    print(f"\n\nFound {len(js_files)} unique JavaScript files on {domain}:")
    if outputfoundfiles:
        for js_file in js_files:
            print(f" - {js_file}")

    # create a directory for the JavaScript files
    js_dir = os.path.join(os.getcwd(), "js_files")
    if not os.path.exists(js_dir):
        os.mkdir(js_dir)

    # download and search for keywords in each JavaScript file
    keywords = ["token"]
    # create list of files with keywords
    fileswithkeyword = []

    for js_file in js_files:
        file_url = urljoin(websiteurl, js_file)
        file_name = os.path.basename(js_file)
        file_path = os.path.join(js_dir, file_name)

        if not os.path.exists(file_path):
            response = requests.get(file_url)
            with open(file_path, "wb") as f:
                f.write(response.content)

        js_dir = os.path.join(os.getcwd(), "js_files")

        for file_name in os.listdir(js_dir):
            file_path = os.path.join(js_dir, file_name)

            with open(file_path, "rb") as f:
                try:
                    contents = f.read().decode()
                    for keyword in keywords:
                        if keyword.lower() in contents.lower():
                            # print(f"File {file_name} contains keyword '{keyword}'")
                            fileswithkeyword.append(file_name)
                except UnicodeDecodeError:
                    os.remove(file_path)
                    print(f"Error decoding {file_path}, skipping and removing file...")
                    continue

    # remove duplicates
    unique_list = list(set(fileswithkeyword))

    # print unique files
    for file in unique_list:
        print(f"File {file} contains one or more keywords")

    # delete all javascript files if no keyword found
    if os.path.exists(js_dir):
        confirm = input(f"Are you sure you want to delete {js_dir}? (y/n): ")
        if confirm.lower() == "y":
            shutil.rmtree(js_dir)
            print(f"Deleted {js_dir}")
        else:
            print(f"{js_dir} was not deleted.")


# clear console
os.system('cls' if os.name == 'nt' else 'clear')
# run the script
url = input("Enter a URL to crawl: ")
crawl_website(url)