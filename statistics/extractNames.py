input_file = "name_counts.txt"
output_file = "names.txt"

with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
    for line in f_in:
        # skip first two lines
        if line.strip() == "" or line.startswith("Name") or set(line.strip()) == {"-"}:
            continue
        # extract names
        name = line.strip().split()[0]
        f_out.write(name + "\n")

    unparsableName = "/ndn/edu/pcl/video/live/202310072129"
    parsableName = "/ndn/edu/pcl/video/live"
    f_out.write(unparsableName + "\n")
    f_out.write(parsableName + "\n")