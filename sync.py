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
    
    If dir1/filename does not exists, nothing happens.  
    If dir1/filename exists and dir2/filename does not, dir1/filename is copied to dir2.
    If both dir1/filename and  dir2/filename, the least recent file is replaced by the most recent one.
    """
    
    dir1 = os.path.expanduser(dir1)
    dir2 = os.path.expanduser(dir2)
    path1 = os.path.join(dir1, filename)
    path2 = os.path.join(dir2, filename)
    
    # -------------------------------------------------------------
    # Begin handling invalid cases
    # -------------------------------------------------------------
    for dir in (dir1, dir2):
        if not os.path.isdir(dir):
            logging.info("Path \"{}\" is not a directory, \"{}\" not synced.".format(dir, filename))
            return
                
    if not os.path.exists(path1):
        logging.info("\"{}\" does not exist, not synced with \"{}\"".format(path1, path2))
        return
    
    if not os.path.isfile(path1):
        logging.warning("\"{}\" is not a file, cannot sync.")
    # -------------------------------------------------------------
    # End of handling invalid cases
    # -------------------------------------------------------------
    
    # If the second file does not (yet) exist, just copy the first one over 
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
