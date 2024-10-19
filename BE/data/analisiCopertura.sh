#!/bin/bash

# File di input
file1="cveNessus2023"
file2="cveQualys2023"

# File di output
righe_in_comune="righe_in_comune.txt"
righe_solo_file1="righe_solo_cveNessus2023"
righe_solo_file2="righe_solo_cveQualys2023"

# Trovare righe comuni
grep -Fxf "$file1" "$file2" > "$righe_in_comune"

# Trovare righe solo nel primo file
grep -Fv -x -f "$file2" "$file1" > "$righe_solo_file1"

# Trovare righe solo nel secondo file
grep -Fv -x -f "$file1" "$file2" > "$righe_solo_file2"

# Contare CVE del 2023
cve2023_file1=$(grep -c "CVE-2023-" "$file1")
cve2023_file2=$(grep -c "CVE-2023-" "$file2")
cve2023_comuni=$(grep -c "CVE-2023-" "$righe_in_comune")

# Risultati
echo "Risultati dell'analisi:"
echo "--------------------------------"
echo "Righe comuni: $(wc -l < "$righe_in_comune")"
echo "Righe solo nel file Nessus: $(wc -l < "$righe_solo_file1")"
echo "Righe solo nel file Qualys: $(wc -l < "$righe_solo_file2")"
echo "CVE del 2023 in file Nessus: $cve2023_file1"
echo "CVE del 2023 in file Qualys: $cve2023_file2"
echo "CVE del 2023 in comune: $cve2023_comuni"

# Calcolare CVE non censiti
cve2023_non_censiti_file1=$((cve2023_file2 - cve2023_comuni))
cve2023_non_censiti_file2=$((cve2023_file1 - cve2023_comuni))

echo "CVE 2023 non censiti nel file Nessus: $cve2023_non_censiti_file1"
echo "CVE 2023 non censiti nel file Qualys: $cve2023_non_censiti_file2"

