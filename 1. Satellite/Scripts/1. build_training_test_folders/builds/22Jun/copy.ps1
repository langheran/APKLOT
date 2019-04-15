$destination_path="C:\Users\langh\Dropbox\MCC-I Masters\Thesis\A17\1. Training 400\database\training"

$path_90="F:\Dataset ITESM\MCC-I Masters\Thesis\A6\dataset\images"
Get-Content 90.txt|Foreach-Object{copy-item -path "$path_90\$_" -destination "$destination_path"}

$path_310="F:\Dataset ITESM\MCC-I Masters\Thesis\A15\1. Quantitative Assessment\training\images"
Get-Content 310.txt|Foreach-Object{copy-item -path "$path_310\$_" -destination "$destination_path"}