@echo off
setlocal enabledelayedexpansion

set "base_name=write_CMD_date"
set "extension=.txt"

for /l %%i in (1, 1, 12) do (
    set "output_file=!base_name!%%i!extension!"
    copy "!base_name!!extension!" "!output_file!"
    echo Created: !output_file!
)

endlocal