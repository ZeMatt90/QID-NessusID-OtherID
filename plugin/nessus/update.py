import pandas as pd
import asyncio
import aiohttp
"""
prima di lanciare questo assicurarsi di aver aggiornato il file cleaned numerbers.csv tramite
curl -S https://www.tenable.com/plugins/feeds?sort=newest | grep -o "<link>https://www.tenable.com/plugins/nessus/[0-9]\+</link>" | sed -n 's/.*\/\([0-9]*\)<\/link>.*/\1/p' > cleaned_numbers.csv
"""
base_url = ""

async def fetch_url(session, url):
    async with session.get(url) as response:
        data = await response.json()
        print(f"\nandato\n{url}\n")
        return data.get("pageProps").get("plugin")
    
async def async_version(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)


async def main():
    file_newid= "plugin/nessus/cleaned_numbers.csv"
    file_full= "plugin/nessus/full_id.csv"
    file_nessus = "data/nessus-kb.csv"

    df_nuovo = pd.read_csv(file_newid, header=None,dtype=int)
    df_full = pd.read_csv(file_full, header=None,dtype=int)
    df_key = pd.read_csv('plugin/nessus/keyforget.csv' , header=None)
    keyforget= df_key.iloc[0, 0]

    numeri_esistenti = df_full.values.flatten().tolist()
    numeri_nuovi = df_nuovo.values.flatten().tolist()

    #carico i nuovi id da scaricare, che non sono presenti in full_id.csv
    IDs = [numero for numero in numeri_nuovi if numero not in numeri_esistenti]
    print("\n nuovi numeri da aggiungere\n\n")
    print(IDs)
    base_url = "https://www.tenable.com/_next/data/"+str(keyforget)+"/en/plugins/nessus/NUMEROID.json?type=nessus&id=NUMEROID"
    json_data_list = []

    try:
        urls = [base_url.replace("NUMEROID", str(ID)) for ID in IDs]
        results = await async_version(urls)
        
        for ID in results:
            if ID is not None:
                json_data_list.append(ID)
                new_id_inserito = pd.DataFrame([ID['cves']], columns=['cves'])
                new_id_inserito['cves'] = new_id_inserito['cves'].astype(int)
                df_full = pd.concat([df_full, new_id_inserito], ignore_index=True)
                print(str(new_id_inserito['cves'].tolist()) + " andato\n")
            else:
                print("plugin data none")
    except Exception as e:
        print(f"Errore: {str(e)}")
        print(f"curl on {str(ID)} ha generato un errore: {str(e)}")
    finally:
        print("Salvataggio degli aggiornamenti effettuati")
        df_full.to_csv(file_full, header=False, index=False)

        df = pd.concat([pd.DataFrame(json_data_list), pd.read_csv(file_nessus)], ignore_index=True, sort=False)
        df.to_csv(file_nessus, index=False)


asyncio.run(main())




"""
[193309, 193308, 193307, 193306, 193305, 193304, 193303, 193302, 193301, 193300, 193299, 193298, 193297, 193296, 193295, 193294, 193293, 193292, 193291, 193290, 193289, 193288, 193287, 193286, 193285, 193284, 193283, 193282, 193281, 193280, 193279, 193278, 193277, 193276, 193275, 193274, 193273, 193272, 193271, 193270, 193269, 193268, 193267, 193266, 193265, 193264, 193263, 193262, 193261, 193260, 193259, 193258, 193257, 193256, 193255, 193254, 193253, 193252, 193251, 193250, 193249, 193248, 193247, 193246, 193245, 193244, 193243, 193242, 193241, 193240, 193239, 193238, 193237, 193236, 193235, 193234, 193233, 193232, 193231, 193230, 193229, 193228, 193227, 193226, 193225, 193224, 193223, 193222, 193221, 193220, 193219, 193218, 193217, 193216, 193215, 193214, 193213, 193212, 193211, 193210, 193209, 193208, 193207, 193206, 193205, 193204, 193203, 193202, 193201, 193200, 193199, 193198, 193197, 193196, 193195, 193194, 193193, 193192, 193191, 193190, 193189, 193188, 193187, 193186, 193185, 193184, 193183, 193182, 193181, 193180, 193179, 193178, 193177, 193176, 193175, 193174, 193173, 193172, 193171, 193170, 193169, 193168, 193167, 193166, 193165, 193164, 193163, 193162, 193161, 193160, 193159, 193158, 193157, 193156, 193155, 193154, 193153, 193152, 193151, 193150, 193149, 193148, 193147, 193146, 193145, 193144, 193143, 193142, 193141, 193140, 193139, 193138, 193137, 193136, 193135, 193134, 193133, 193132, 193131, 193130, 193129, 193128, 193127, 193126, 193125, 193124, 193123, 193122, 193121, 193120, 193119, 193118, 193117, 193116, 193115, 193114, 193113, 193112, 193111, 193110, 193109, 193108, 193107, 193106, 193105, 193104, 193103, 193102, 193101, 193100, 193099, 193098, 193097, 193096, 193095, 193094, 193093, 193092, 193091, 193090, 193089, 193088, 193087, 193086, 193085, 193084, 193083, 193082, 193081, 193080, 193079, 193078, 193077, 193076, 193075, 193074, 193073, 193072, 193071, 193070, 193069, 193068, 193067, 193066, 193065, 193064, 193063, 193062, 193061, 193060, 193059, 193058, 193057, 193056, 193055, 193054, 193053, 193052, 193051, 193050, 193049, 193048, 193047, 193046, 193045, 193044, 193043, 193042, 193041, 193040, 193039, 193038, 193037, 193036, 193035, 193034, 193033, 193032, 193031, 193030, 193029, 193028, 193027, 193026, 193025, 193024, 193023, 193022, 193021, 193020, 193019, 193018, 193017, 193016, 193015, 193014, 193013, 193012, 193011, 193010, 193009, 193008, 193007, 193006, 193005, 193004, 193003, 193002, 193001, 193000, 192999, 192998, 192997, 192996, 192995, 192994, 192993, 192992, 192991, 192990, 192989, 192988, 192987, 192986, 192985, 192984, 192983, 192982, 192981, 192980, 192979, 192978, 192977, 192976, 192975, 192974, 192973, 192972, 192971, 192970, 192969, 192968, 192967, 192966, 192965, 192964, 192963, 192962, 192961, 192960, 192959, 192958, 192957, 192956, 192955, 192954, 192953, 192952, 192951, 192950, 192949, 192948, 192947, 192946, 192945, 192944, 192943, 192942, 192941, 192940, 192939, 192938, 192937, 192936, 192935, 192934, 192933, 192932, 192931, 192930, 192929, 192928, 192927, 192926, 192925, 192924, 192923, 192922, 192921, 192920, 192919, 192918, 192917, 192916, 192915, 192914, 192913, 192912, 192911, 192910, 192909, 192908, 192907, 192906, 192905, 192904, 192903, 192902, 192901, 192900, 192899, 192898, 192897, 192896, 192895, 192894, 192893, 192892, 192891, 192890, 192889, 192888, 192887, 192886, 192885, 192884, 192883, 192882, 192881, 192880, 192879, 192878, 192877, 192876, 192875, 192874, 192873, 192872, 192871, 192870, 192869, 192868, 192867, 192866, 192865, 192864, 192863, 192862, 192861, 192860, 192859, 192858, 192857, 192856, 192855, 192854, 192853, 192852, 192851, 192850, 192849, 192848, 192847, 192846, 192845, 192844, 192843, 192842]
"""