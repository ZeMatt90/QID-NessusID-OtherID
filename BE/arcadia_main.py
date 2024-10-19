from cve_updater import CveUpdater
from plugin.nessus.update import NessusUpdater 
import asyncio
from arcadia_dictionary import ArcadiaDictionary
from data_cleaner import DataCleaner

class Arcadia:

    def main():
        base_url="https://www.tenable.com/_next/data/",
        file_newid="plugin/nessus/cleaned_numbers.csv",
        file_fullidnessus="plugin/nessus/full_id.csv",
        file_nessus="data/nessus-kb.csv",
        file_qualys="data/qualys-kb.csv",
        file_allcve="data/all_cve.csv",
        keyforget_file="plugin/nessus/keyforget.csv"
        file_dictionary="data/dictionary.csv"
        try:
            #=========================================================== 
            # Step 1. Get new Nessus data                              # 
            #===========================================================                    
            print("update Nessus data...")
            log="logs/tenable_scraper.log"
            nessus_updater = NessusUpdater(base_url,file_newid,file_fullidnessus,file_nessus,keyforget_file,log)
            asyncio.run(nessus_updater.process())
            #=========================================================== 
            # Step 2. Update list of cve and status                    # 
            #===========================================================      
            print("Running CveUpdater...")
            processor = CveUpdater(file_nessus, file_qualys, file_allcve)
            processor.process()     
            #=========================================================== 
            # Step 3. Update     the dictionary                        # 
            #===========================================================      
            print("Running ArcadiaDictionary...")
            processor = ArcadiaDictionary(file_nessus, file_qualys, file_allcve, file_dictionary)
            processor.update()
            #=========================================================== 
            # Step 4. Check data, clean ecc                            # 
            #===========================================================      
            print("clean data and immpossible duplicates...")
            cleaner = DataCleaner(
                file_fullidnessus,
                file_allcve,
                file_nessus,
                file_qualys,
                file_dictionary
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
