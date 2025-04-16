#!/usr/bin/env python3

import subprocess
import glob
import os
import re
import shutil

def run_command(command):
    return subprocess.check_output(command, shell=True).decode()

def organize_files():
    print("Organizing files...")
    trace_dir = '/raid/tracedata'
    # Find all .zst files
    zst_files = glob.glob(os.path.join(trace_dir, '*.zst'))

    for file_path in zst_files:
        file_name = os.path.basename(file_path)
        date = re.findall(r'\d{4}-\d{2}-\d{2}', file_name)[0]
        main_dir_path = os.path.join(trace_dir, date)
        os.makedirs(main_dir_path, exist_ok=True)
        old_file_path = os.path.join(trace_dir, file_name)
        new_file_path = os.path.join(main_dir_path, file_name)
        shutil.move(old_file_path, new_file_path)

def push_changes():
    print("Pushing changes...")
    run_command("git add /raid/tracedata")
    date = run_command("date")
    run_command(f"git commit -m 'Auto-commit traces [{date}]'")
    run_command("git push")


def main():
    organize_files()
    push_changes()

if __name__ == "__main__":
    main()
