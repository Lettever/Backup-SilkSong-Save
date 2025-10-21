import os
import shutil
import time
from datetime import datetime

err = "\033[91m✗\033[0m"
success = "\033[92m✓\033[0m"
path = "/home/lettever/.config/unity3d/Team Cherry/Hollow Knight Silksong/1047710596"
if not os.path.exists(path):
    print(f"{err}: {path=} does not exist")
    exit()
file_number = 3
running = True
save_file = os.path.join(path, f"user{file_number}.dat")
if not os.path.exists(save_file):
    print(f"{err}: {save_file=} does not exist")
    exit()
backup_dir = os.path.join(path, "backup")
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def backup():
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(backup_dir, f"user{file_number}_{current_time}.dat")
    try:
        shutil.copy2(save_file, backup_file)
        print(f"{success}: Backup created: {backup_file}")
    except Exception as e:
        print(f"{err}: Error creating backup: {e}")

def restore():
    most_recent_file = None
    
    for file in os.listdir(backup_dir):
        if file.startswith(f"user{file_number}_") and file.endswith(".dat"):
            if most_recent_file is None or file > most_recent_file:
                most_recent_file = file
    
    if most_recent_file is None:
        print(f"{err}: No backup files found for user{file_number}.dat")
        return
    
    backup_file = os.path.join(backup_dir, most_recent_file)
    
    try:
        shutil.copy2(backup_file, save_file)
        print(f"{success}: Restored from: {backup_file}")
        print(f"{success}: To: {save_file}")
    except Exception as e:
        print(f"{err}: {e}")

def leave():
    global running
    print("Leaving")
    running = False

def list_backups():
    backups = []
    for file in os.listdir(backup_dir):
        if file.startswith(f"user{file_number}_") and file.endswith(".dat"):
            backups.append(file)
        
    backups.sort(reverse=True)
    for file in backups:
        print(f"    {file}")
    print(f"    Total: {len(backups)} backups")

def print_help():
    print("    b > creates a backup")
    print("    r > restores the most recent backup")
    print("    l > leaves the repl")
    print("    L > list all backup")
    print("    h > prints this menu")
    print()
    print(f"    {path=}")
    print(f"    {file_number=}")
    print(f"    {save_file=}")
    print(f"    {backup_dir=}")
    

m = {
    "b": backup,
    "r": restore,
    "l": leave,
    "L": list_backups,
    "h": print_help
}

def get_option():
    while True:
        op = input("[brlLh] > ")
        if (op in m):
            return op
        print(f"{err}: {op} in not a valid option")

if __name__ == "__main__":
    print("Press 'h' to print the help menu")
    
    while running:
        op = get_option()
        m[op]()

"""
Maybe todo:
    - add backup pruning, where you get to keep at least n backup
    prune_backups(keep=3)
"""
