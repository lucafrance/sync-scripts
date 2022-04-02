# Sync Scripts

Keep your configuration files like `.gitconfig` up to date across multiple machines by synching them regularly in your OneDrive (or any other cloud service) folder.

## Directory structure

```
~/OneDrive
|- ...
|  |- config-files
|  |  |- sync-scripts  <- this repository 
|  |  |  |- sync.csv
|  |  |  |- sync.py
|  |  |  |- sync.ps1
|  |  |  |- sync.log
|  |  |- sync-files    <- synched files
|  |  |  |- home
|  |  |  |  |- .atom
|  |  |  |  |  |- config.json
|  |  |  |  |- [...]
|  |  |  |  |- .gitignore
|  |  |  |  |- [...]
```

## Setup

1. Create a folder `config-files` within your cloud folder.
1. Create a `sync-scripts` folder in `config-files`.
1. Clone this repository to `sync-scripts`.
1. Create a `sync-files` folder in `config-files`.
1. Initialize a git repository in `sync-files`.
1. Define in `sync-scripts/sync.csv` which files should be synched to which folder within `sync-files`.

Each row of `sync-scripts/sync.csv` consists of two columns `<path1>,<path2>`.
- `<path1>` is an absolute path to a file to synch.
- `<path2>` is a relative path to a folder within `sync-files`.
- If `<path1>` is not a file, nothing happens.
  - E.g. the configuration file is for a program not installed on the machine.
- If `sync-files/<path2>` does not exist, nothing happens.
- If `<path1>` and `sync-files/<path2>` are valid, the most recent version of the file is kept and the other one gets replaced.

## Usage

Run `sync-scripts/sync.ps1` to:
- Synch all files to and from `sync-files`.
- Commit any changes in `sync-files`.
- Log the output to `sync-scripts/sync.log`

## Configuring Windows Task Scheduler

To automate the execution add a task running the command `powershell -file <path to sync.ps1>`.
Pick the option *Run whether user is logged on or not* to prevent the PowerShell window from being shown during the automatic execution ([source](https://stackoverflow.com/a/50630717)).

## Requirements
- Python 3.10
- git 2.33
