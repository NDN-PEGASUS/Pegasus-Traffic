def is_valid_ndn_name(ndn_name):
    """
    check if the name is valid
    """
    segments = ndn_name.split("/")
    # 15x4 (Meta4)
    if len(segments) > 4:
        return False
    for segment in segments:
        if len(segment) > 15:
            return False
        
    return True

def read_name_counts(input_file):
    """
    read NDN names and their occurrences count
    """
    name_counts = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    name, count = line.split("\t")
                    name_counts.append((name, int(count)))
                except:
                    continue
    return name_counts

def calculate_percentage(total_query_count, name_counts, min_thresholds):
    """
    calculate the percentage of name counts in different request counts
    """
    # total_valid_count = 0
    # total_name_count = 0
    result = []
    process = 0 # progress bar
    for n in min_thresholds:
        name_count_threshold = 0
        valid_name_count_threshold = 0

        name_cnt = 0
        valid_cnt = 0

        for name, count in name_counts:
            if count < n:
                break

            name_count_threshold += count
            name_cnt += 1
            # total_name_count += count

            if is_valid_ndn_name(name):
                valid_name_count_threshold += count
                valid_cnt += 1
                # total_valid_count += count

        name_percentage = name_cnt / len(name_counts)
        query_percentage = name_count_threshold / total_query_count
        valid_name_percentage = valid_cnt / name_cnt
        valid_percentage = valid_name_count_threshold / name_count_threshold

        result.append((n, name_cnt, name_percentage, name_count_threshold, query_percentage, \
                       valid_cnt, valid_name_percentage, valid_name_count_threshold, valid_percentage))

        # show progress
        process += 1
        print(f"Processed {process}/{len(min_thresholds)}")

    return result


input_file = "name_counts.txt"
# The list of minimum request counts for counting the number of names
min_thresholds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 100, 500, 1000]

name_counts = read_name_counts(input_file)
total_count = sum(count for name, count in name_counts)

# plot_statiscs(name_counts)

result = calculate_percentage(total_count, name_counts, min_thresholds)

# Output the results to a txt file
output_file = "statistics_meta4.txt"
with open(output_file, "w") as f:
    f.write(f"Total Name Count: \t{len(name_counts)}\n")
    f.write(f"Total Query Count: \t{total_count}\n")
    f.write("-----------------------------------------------------------------------------------------------------------------------\n")
    f.write("N\t\tName_Cnt\tName_Pct\tQuery_Cnt\tQuery_Pct\tValid_Cnt\tValid_Pct\tValid_Query_Cnt\t\tValid_Query_Pct\n")
    f.write("-----------------------------------------------------------------------------------------------------------------------\n")
    for threshold, name_cnt, name_pencentage, name_count_threshold, percentage, valid_cnt, valid_name_percentage, valid_name_count_threshold, valid_percentage in result:
        if threshold < 30:
            f.write(f"{threshold}\t\t{name_cnt}\t\t{name_pencentage:.2%}\t\t{name_count_threshold}\t\t{percentage:.2%}\t\t{valid_cnt}\t\t\t{valid_name_percentage:.2%}\t\t{valid_name_count_threshold}\t\t\t\t{valid_percentage:.2%}\n")
        elif 30 <= threshold < 1000:
            f.write(f"{threshold}\t\t{name_cnt}\t\t\t{name_pencentage:.2%}\t\t{name_count_threshold}\t\t{percentage:.2%}\t\t{valid_cnt}\t\t\t{valid_name_percentage:.2%}\t\t{valid_name_count_threshold}\t\t\t\t{valid_percentage:.2%}\n")
        else:
            f.write(f"{threshold}\t{name_cnt}\t\t\t{name_pencentage:.2%}\t\t{name_count_threshold}\t\t{percentage:.2%}\t\t{valid_cnt}\t\t\t{valid_name_percentage:.2%}\t\t{valid_name_count_threshold}\t\t\t\t{valid_percentage:.2%}\n")
    f.write("-----------------------------------------------------------------------------------------------------------------------\n")

print("Statistics have been written to ", output_file)