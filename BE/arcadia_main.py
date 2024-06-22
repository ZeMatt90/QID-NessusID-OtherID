from cve_updater import CveUpdater
from plugin.nessus.update import NessusUpdater 
import asyncio
from arcadia_dictionary import ArcadiaDictionary
from data_cleaner import DataCleaner

class Arcadia:

    def main():
        try:
            print("update Nessus data...")
            nessus_updater = NessusUpdater(
                base_url="https://www.tenable.com/_next/data/",
                file_newid="plugin/nessus/cleaned_numbers.csv",
                file_full="plugin/nessus/full_id.csv",
                file_nessus="data/nessus-kb.csv",
                keyforget_file="plugin/nessus/keyforget.csv"
            )
            asyncio.run(nessus_updater.process())

            print("Running CveUpdater...")
            processor = CveUpdater("data/nessus-kb.csv", "data/qualys-kb.csv", "data/all_cve.csv")
            processor.process()     

            print("Running create_dictionary...")
            processor = ArcadiaDictionary("data/nessus-kb.csv", "data/qualys-kb.csv", "data/all_cve.csv", "data/dictionary.csv")
            processor.update()

            print("clean data and immpossible duplicates...")
            cleaner = DataCleaner(
                file_fullidnessus="plugin/nessus/full_id.csv",
                file_allcve="data/all_cve.csv",
                file_nessus="data/nessus-kb.csv",
                file_qualys="data/qualys-kb.csv",
                file_dictionary="data/dictionary.csv"
            )
            cleaner.deduplicate_and_save()

            # plugin/nessus/update.py
            # create_all_cve.py
            # createdictionary.py
            # controller_check_data.py

            print("All tasks completed successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

    if __name__ == "__main__":
        main()
