import csv
import filecmp
import logging
import os
import shutil


SYNC_FILES_DIR = "../sync-files"

def sync_list():
    with open("sync.csv",  "rt") as f:
        for row in csv.reader(f):
            filename = os.path.basename(row[0])
            dir1 = os.path.dirname(row[0])
            dir1 = os.path.expanduser(dir1)
            dir1 = os.path.abspath(dir1)
            dir2 = os.path.join(SYNC_FILES_DIR, row[1])
            dir2 = os.path.abspath(dir2)
            yield dir1, dir2, filename

def sync_file(dir1, dir2, filename):
    """Sync file in dir1 and dir2 by keeping the most recent one
    
    If dir1 or dir2 do not exist, nothing happens.
    If dir1/filename and dir2/filename do not exist, nothing happens 
    If just one of dir1/filename or dir2/filename exists, the existing file is copied over.
    If both dir1/filename and dir2/filename exist, the least recent file is replaced by the most recent one.
    """
    
    dir1 = os.path.expanduser(dir1)
    dir2 = os.path.expanduser(dir2)
    path1 = os.path.join(dir1, filename)
    path2 = os.path.join(dir2, filename)
    
    # If a directory on each side does not exist, do nothing
    for dir in (dir1, dir2):
        if not os.path.isdir(dir):
            logging.info("Path \"{}\" is not a directory, \"{}\" not synced.".format(dir, filename))
            return
    
    # If both files do not exist, do nothing            
    if not (os.path.exists(path1) or os.path.exists(path2)) :
        logging.warning("Both \"{}\" and \"{}\" do not exist, not synched.".format(path1, path2))
        return
    
    # If one file does not exist, copy over the existing one 
    if not os.path.exists(path1):
        shutil.copy2(path2, dir1)
        logging.info("Copied \"{}\" to \"{}\".".format(path2, dir1))
        return
    if not os.path.exists(path2):
        shutil.copy2(path1, dir2)
        logging.info("Copied \"{}\" to \"{}\".".format(path1, dir2))
        return
    
    # If both files exist and are the same, do nothing
    if filecmp.cmp(path1, path2):
        logging.debug("\"{}\" appears to be the same as \"{}\", ignored.".format(path1, path2))
        return
    
    # If both files exist and are different, keep the most recent one
    if os.path.getmtime(path1) > os.path.getmtime(path2):
        shutil.copy2(path1, path2)
        logging.info("Replaced \"{}\" with more recent \"{}\".".format(path2, path1))
    else:
        shutil.copy2(path2, path1)
        logging.info("Replaced \"{}\" with more recent \"{}\".".format(path1, path2))

def sync_all():
    for dir1, dir2, filename in sync_list():
        try:
            sync_file(dir1, dir2, filename)
        except Exception as e:
            logging.error(e)
            logging.error("Unexpected error shen syncing \"{}\", \"{}\", \"{}\"".format(dir1, dir2, filename))

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )
    sync_all()
