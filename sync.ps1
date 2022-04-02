Set-Location -Path $PSScriptRoot
Start-Transcript -Path "sync.log" -Append
python sync.py
git -C ../sync-files add *
git -C ../sync-files commit -m "Update files"
Stop-Transcript
