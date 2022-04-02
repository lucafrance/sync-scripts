Start-Transcript -Path "sync.log" -Append -UseMinimalHeader
Set-Location -Path $PSScriptRoot
python sync.py
git -C ../sync-files add *
git -C ../sync-files commit -m "Update files"
Stop-Transcript
