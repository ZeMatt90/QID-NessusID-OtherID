import requests
import logging
import re
import os

class TenableScraper:
    def __init__(self):
        self.logger = logging.getLogger('TenableScraper')
        handler = logging.FileHandler('../../logs/tenable_scraper.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        pass

    def fetch_and_process_build_manifest(self, url, output_file):
        self.logger.info('Starting fetch_and_process_build_manifest')
        try:
            response = requests.get(url)
            response.raise_for_status()
            matches = re.findall(r'/_next/static/[^/]+/_buildManifest.js', response.text)
            if matches:
                cleaned_string = re.sub(r'/(_next/static/|_buildManifest.js)', '', matches[0])
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, 'w') as file:
                    file.write(cleaned_string + '\n')
                self.logger.info(f"Data written to {output_file}")
            else:
                self.logger.info("No matches found.")
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch URL: {url}, Error: {e}")
        self.logger.info('Finished fetch_and_process_build_manifest')

    def fetch_and_process_plugin_numbers(self, url, output_file):
        self.logger.info('Starting fetch_and_process_plugin_numbers')
        try:
            response = requests.get(url)
            response.raise_for_status()
            matches = re.findall(r'<link>https://www.tenable.com/plugins/nessus/[0-9]+</link>', response.text)
            cleaned_numbers = [re.sub(r'.*/([0-9]+)</link>.*', r'\1', match) for match in matches]
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as file:
                for number in cleaned_numbers:
                    file.write(number + '\n')
            self.logger.info(f"Data written to {output_file}")
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch URL: {url}, Error: {e}")
        self.logger.info('Finished fetch_and_process_plugin_numbers')

if __name__ == '__main__':
    # Esempio di utilizzo
    scraper = TenableScraper()
    scraper.fetch_and_process_build_manifest(
        'https://www.tenable.com/plugins/nessus/186284',
        'keyforget.csv'
    )
    scraper.fetch_and_process_plugin_numbers(
        'https://www.tenable.com/plugins/feeds?sort=newest',
        'cleaned_numbers.csv'
    )
