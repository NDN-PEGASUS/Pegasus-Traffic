import os
from collections import defaultdict


def process_ndn_name(ndn_name):
    """
    Process an NDN name by removing segments starting with /KEY/ or /INFO/ and everything after them.

    Args:
    ndn_name (str): The original NDN name.

    Returns:
    str: The processed NDN name.
    """
    # Split the NDN name into segments
    segments = ndn_name.split('/')
    
    # Initialize an empty list to store the processed segments
    processed_segments = []
    
    # Process each segment
    for segment in segments:
        if segment in ["KEY", "INFO"]:
            # Stop processing if we encounter "KEY" or "INFO"
            break
        processed_segments.append(segment)
    
    # Join the processed segments back into a string
    processed_ndn_name = '/'.join(processed_segments)
    
    return processed_ndn_name


def is_valid_ndn_name(ndn_name):
    """
    Check if the given NDN name is valid.
    In this example, we verify that the number of segments in the name does not exceed 4,
    and that the length of each segment does not exceed 15 characters.
    """
    segments = ndn_name.split("/")
    if len(segments) > 4:
        return False
    for segment in segments:
        if len(segment) > 15:
            return False
    return True

def process_txt_file(input_file):
    """
    Process the given text file, count the occurrences of names, 
    and calculate the number of valid names and the total number of names.
    """
    ndn_names = defaultdict(int)
    valid_count = 0
    total_count = 0

    with open(input_file, "r") as input_f:
        for line in input_f:
            ndn_name = line.strip()
            ndn_name = process_ndn_name(ndn_name) # Remove content after KEY and INFO
            ndn_names[ndn_name] += 1
            total_count += 1
            if is_valid_ndn_name(ndn_name):
                valid_count += 1

    return ndn_names, valid_count, total_count

def analyze_ndn_names():
    """
    analyze the NDN names in the current directory.
    It counts the occurrences of names and the number of valid names.
    """
    current_directory = os.getcwd()  # Get the current working directory
    txt_files = [filename for filename in os.listdir(current_directory) if filename.endswith(".txt")]
    total_files = len(txt_files)
    processed_files = 0

    ndn_names_all = defaultdict(int)
    total_valid_count = 0
    total_count = 0

    for filename in txt_files:
        processed_files += 1
        input_file = os.path.join(current_directory, filename)
        ndn_names, valid_count, count = process_txt_file(input_file)

        for name, name_count in ndn_names.items():
            ndn_names_all[name] += name_count

        total_valid_count += valid_count
        total_count += count

        print(f"Processed file {processed_files}/{total_files}")

    return ndn_names_all, total_valid_count, total_count

ndn_names_all, total_valid_count, total_count = analyze_ndn_names()

# count the number of unique names
unique_names_count = len(ndn_names_all)

# sort the names by their occurrence count in descending order
sorted_names = sorted(ndn_names_all.items(), key=lambda x: x[1], reverse=True)

# output the occurrence count of each name to a text file
output_file = "../statistics/name_counts.txt"
with open(output_file, "w") as f:
    f.write("Name\tCount\n")
    f.write("-----------------\n")
    for name, count in sorted_names:
        f.write(f"{name}\t{count}\n")

# count the total occurrences of names that appear at least twice
repeat_count = sum(count for name, count in ndn_names_all.items() if count >= 2)

# calculate the repeat frequency
repeat_frequency = repeat_count / total_count

# output the statistics to a text file
valid_names_percentage = total_valid_count / total_count * 100
output_file = "../statistics/meta4_statistics.txt"
with open(output_file, "w") as f:
    f.write(f"Total unique names: {unique_names_count}\n")
    f.write(f"Valid qurey count: {total_valid_count}\n")
    f.write(f"Invalid qurey count: {total_count - total_valid_count}\n")
    f.write(f"Valid qurey percentage: {valid_names_percentage:.2f}%\n")
    f.write(f"Repeat count: {repeat_count}\n")
    f.write(f"Repeat frequency: {repeat_frequency:.2%}\n")

print("Statistics have been written to ", output_file)