from collections import defaultdict


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

input_file = "name_counts.txt"
name_counts = read_name_counts(input_file)

format_counts = defaultdict(int)

for name, count in name_counts:
    segments = name.split('/')
    segment_count = len(segments)
    format = ""
    for i in range(segment_count):
        format += str(len(segments[i])) + "/"
    format_counts[format[:-1]] += count


formats = sorted(format_counts.items(), key=lambda x: x[1], reverse=True)
x, y = [], []
for format, cnt in formats:
    x.append(format)
    y.append(cnt)

output_file = "format_counts.txt"
with open(output_file, "w") as f:
    f.write("Format\tCount\n")
    f.write("-----------------\n")
    for format, count in formats:
        f.write(f"{format}\t{count}\n")