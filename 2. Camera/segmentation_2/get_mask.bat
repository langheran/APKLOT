@echo off
if [%1]==[] goto :eof
:loop
python get_mask.py -i "%~dpn1%~x1"
shift
if not [%1]==[] goto loop
::pause
