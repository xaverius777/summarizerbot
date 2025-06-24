import hashlib
import os
import glob


def hash_file(filepath):
    hash_obj = hashlib.sha256()
    with open(filepath, 'rb') as f:
        hash_obj.update(f.read())
    return hash_obj.hexdigest()


def get_file_state(source_dir):
    return {
        os.path.basename(fp): hash_file(fp)
        for fp in glob.glob(os.path.join(source_dir, "*"))
        if os.path.isfile(fp)
    }


def detect_changes(old_state, new_state):
    added = [f for f in new_state if f not in old_state]
    removed = [f for f in old_state if f not in new_state]
    modified = [f for f in new_state if f in old_state and new_state[f] != old_state[f]]
    return added, removed, modified

