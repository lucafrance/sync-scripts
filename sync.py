import logging
import os
import shutil


SYNC_FILES_DIR = "../sync-files"

def sync_list():
    with open("sync-files.txt",  "rt") as f:
        return f.read().splitlines()

def sync_file(dir1, dir2, filename):
    """Sync file in dir1 and dir2 by keeping the most recent one"""
    
    dir1 = os.path.expanduser(dir1)
    dir2 = os.path.expanduser(dir2)
    path1 = os.path.join(dir1, filename)
    path2 = os.path.join(dir2, filename)
    
    # -------------------------------------------------------------
    # Begin handling invalid cases
    # -------------------------------------------------------------
    for dir in (dir1, dir2):
        if not os.path.isdir(dir):
            logging.warning("Path \"{}\" is not a directory, \"{}\" not synced.".format(dir, filename))
            return
                
    if not os.path.exists(path1):
        if not os.path.exists(path2):
            logging.warning("Files \"{}\" and \"{}\" do not exist, nothing to sync.".format(path1, path2))
            return
        else:
            sync_file(path2, path1)
    
    if not os.path.isfile(path1):
        logging.warning("\"{}\" is not a file, cannot sync.")
    # -------------------------------------------------------------
    # End of handling invalid cases
    # -------------------------------------------------------------
    
    # If the second file does not (yet) exists, just copy the first one over 
    if not os.path.exists(path2):
        shutil.copy2(path1, dir2)
        logging.info("Copied \"{}\" to \"{}\".".format(path1, dir2))
        return
        
    # If both files exist, keep the most recent one
    if os.path.getmtime(path1) > os.path.getmtime(path2):
        shutil.copy2(path1, path2)
        logging.info("Replaced \"{}\" with more recent \"{}\".".format(path2, path1))
    else:
        shutil.copy2(path2, path1)
        logging.info("Replaced \"{}\" with more recent \"{}\".".format(path1, path2))

def sync_all():
    for path in sync_list():
        if path.startswith("#"):
            continue
        filename = os.path.basename(path)
        sync_file(os.path.dirname(path), SYNC_FILES_DIR, filename)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    sync_all()
