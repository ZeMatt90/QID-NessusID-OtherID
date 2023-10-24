import requests
import json
import pandas as pd
import time
#idnessus di test con cve CVE-2022-3602
IDs=[51192,57582,45411]#173835,173139,173113,167841,167263,167024,166965,166960,166959,166808,166801,166798,166796,166789,166788,166787,166782,166781,166774,166773]

# URL da cui effettuare la richiesta GET
base_url ="https://www.tenable.com/_next/data/yHtLwfa7D2y-FVrK1k9cM/en/plugins/nessus/NUMEROID.json?type=nessus&id=NUMEROID"
#url = "https://www.tenable.com/_next/data/HbLEgcen8J-sBub4SqZDm/en/plugins/nessus/NUMEROID.json?type=nessus"
json_data_list= []

for ID in IDs:
    url =base_url.replace("NUMEROID",str(ID))
    print("invio get "+url)
    time.sleep(1)
    response = requests.get(url)                                    # Esegui la richiesta GET
    if response.status_code == 200:                                 # Verifica se la richiesta ha avuto successo
        json_data_list.append(response.json().get("pageProps").get("plugin"))     # Ottieni il JSON dalla risposta
    else:
        print("La richiesta non è riuscita. Codice di stato:", response.status_code)
#{'plugin': {'cves': [], 'cvss3_base_score': '6.5', 'cvss3_vector': 'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N', 'cvss_base_score': '6.4', 'cvss_vector': 'CVSS2#AV:N/AC:L/Au:N/C:P/I:P/A:N', 'dependencies': ['ssl_certificate_chain.nasl'], 'description': "The server's X.509 certificate cannot be trusted. This situation can occur in three different ways, in which the chain of trust can be broken, as stated below :\n\n  - First, the top of the certificate chain sent by the     server might not be descended from a known public     certificate authority. This can occur either when the     top of the chain is an unrecognized, self-signed     certificate, or when intermediate certificates are     missing that would connect the top of the certificate     chain to a known public certificate authority.\n\n  - Second, the certificate chain may contain a certificate     that is not valid at the time of the scan. This can     occur either when the scan occurs before one of the     certificate's 'notBefore' dates, or after one of the     certificate's 'notAfter' dates.\n\n  - Third, the certificate chain may contain a signature     that either didn't match the certificate's information     or could not be verified. Bad signatures can be fixed by     getting the certificate with the bad signature to be     re-signed by its issuer. Signatures that could not be     verified are the result of the certificate's issuer     using a signing algorithm that Nessus either does not     support or does not recognize.\n\nIf the remote host is a public host in production, any break in the chain makes it more difficult for users to verify the authenticity and identity of the web server. This could make it easier to carry out man-in-the-middle attacks against the remote host.", 'description_i18n': {'ja_JP': 'サーバーの X.509 証明書は信頼できません。以下に説明するように、この状況は3つの異なる経緯で発生する可能性があり、これによって信頼チェーンが破損する可能性があります。\n\n  - まず、サーバーから送信された、証明書チェーンの最上位の証明書が、既知の公共認証期間由来のものではない可能性があります。これは、チェーンの最上位が正当に認められていない自己署名証明書であるか、または証明書チェーンの最上位と既知の公共認証機関とをつなぐ中間の証明書が見つからない場合に起こることがあります。\n\n  - 2 番目に、スキャンする時点で有効でない証明書が証明書チェーンに含まれていることがあります。これは、証明書の「notBefore」（有効期限の開始日時）日付よりも前または「notAfter」（有効期限の終了日時）日付よりも後にスキャンが実行された場合に起こることがあります。\n\n  - 3 番目に、証明書チェーンに、証明書の情報と一致しなかった署名が含まれているか、検証できなかった署名が含まれている可能性があります。署名が不適切な場合、不適切な署名が含まれている証明書に発行者が再度署名することで修正できます。証明書を検証できなかった場合

# Specifica il percorso del file XLSX in cui desideri salvarli
file_path = "./data/nessus-light.xlsx"

# Effettua la concatenazione, notando che un df ha più colonne
df = pd.concat([pd.DataFrame(json_data_list), pd.read_excel(file_path)], ignore_index=True, sort=False)


# Salva il DataFrame nel file XLSX
df.to_excel(file_path, index=False)


