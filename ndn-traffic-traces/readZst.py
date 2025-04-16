import os
import shutil
import zstandard as zstd
from scapy.all import rdpcap, RawPcapNgReader, Ether

root_directory = '.'  # Root path

# Get all date directories
date_paths = [directory for directory in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, directory))]

total_dates = len(date_paths)
processed_dates = 0


def parse_ndn_name(content, name_l):
    name = ""
    index = 0
    comp_cnt = 0
    types = [0x08, 0x01, 0x02, 0x20, 0x32, 0x34, 0x36, 0x38, 0x3a]
    while name_l > 0 and content[index] in types:
        index += 1
        name_l -= 1
        comp_cnt += 1
        comp_l = content[index]
        if comp_l == 0xFD:
            a = [content[index + 1], content[index + 2]]
            comp_l = int(''.join(format(x, '02x') for x in a), 16)
            index += 3
            name_l -= 3
        else:
            index += 1
            name_l -= 1
        tmp = content[index:index+comp_l]
        # print(tmp)
        try:
            tmp = tmp.decode('utf-8')
            name += tmp + "/"
        except:
            # name += tmp.decode('latin-1') + "/"
            break
        index += comp_l
        name_l -= comp_l

    return name[:-1]


def process_ndn_packets(packets, file):
    cnt = 0
    for packet in packets:
        # print('\n')
        if 'UDP' in packet:
            cnt += 1
            payload = packet['UDP'].payload     # Type：scapy.packet.Raw
            payload_bytes = payload.build()     # converse to bytes
            # start to parse NDN
            index = 0
            # LpPacket
            try:
                first_t = payload_bytes[index]
            except:
                continue
            # print("first_t: " + hex(first_t))
            if first_t != 0x64:
                continue
            index += 1
            try:
                first_l = payload_bytes[index]
            except:
                continue
            # print("first_l: " + hex(first_l))
            if first_l == 0xFD:
                index += 3
            else:
                index += 1
            # skip Sequence
            try:
                first_l = payload_bytes[index]
            except:
                continue
            if first_l == 0x51:
                index += 1
                try:
                    length = payload_bytes[index]
                    index += 1
                except:
                    continue
                index += length
            # skip Ack and TxSequence
            try:
                first_l = payload_bytes[index]
            except:
                continue
            while first_l == 0xFD:
                a = [payload_bytes[index+1], payload_bytes[index+2]]
                temp_l = (a[0] << 8) | a[1]
                if temp_l == 0x0348 or temp_l == 0x0344:
                    index += 3
                    length = payload_bytes[index]
                    index += 1 + length
                    try:
                        first_l = payload_bytes[index]
                    except:
                        break
                else:
                    break # NACK
            index += 12
            # Fragment
            try:
                frag_t = payload_bytes[index]
            except:
                continue
            # print("frag_t: " + hex(frag_t))
            if frag_t != 0x50:
                continue
            index += 1
            frag_l = payload_bytes[index]
            if frag_l == 0xFD:
                index += 3
            else:
                index += 1
            # Interest
            inte_t = payload_bytes[index]
            # print("inte_t: " + hex(inte_t))
            if inte_t != 0x05:
                continue
            index += 1
            inte_l = payload_bytes[index]
            if inte_l == 0xFD:
                index += 3
            else:
                index += 1
            # Name
            name_t = payload_bytes[index]
            # print("name_t: " + hex(name_t))
            if name_t != 0x07:
                continue
            index += 1
            name_l = payload_bytes[index]
            if name_l == 0xFD:
                a = [payload_bytes[index+1], payload_bytes[index+2]]
                name_l = int(''.join(format(x, '02x') for x in a), 16)
                index += 3
            else:
                index += 1
            # print("name_l: " + str(name_l))

            name = parse_ndn_name(payload_bytes[index:], name_l)
            name = name.replace('\n', 'n')  # delete line feed
            name = name.replace('\r', 'r')  # delete carriage return
            # print(name)
            file.write(name + "\n")

            # if cnt > 20:
            #     return


for date_path in date_paths:
    date_directory = os.path.join(root_directory, date_path)
    zst_files = [file for file in os.listdir(date_directory) if file.endswith('.pcapng.zst')]

    if not zst_files:
        continue

    print(f"Processing {date_path} ({processed_dates + 1}/{total_dates})")

    # create txt files
    output_file = os.path.join("../ndn_names/" + date_path + '_ndn_names.txt')
    with open(output_file, "w", encoding="utf-8") as file:

        total_files = len(zst_files)
        processed_files = 0

        for zst_file in zst_files:
            # unzip .zst files to .pcapng files
            zst_file_path = os.path.join(date_directory, zst_file)
            pcapng_file = os.path.splitext(zst_file)[0]  # delete ".zst"
            pcapng_file_path = os.path.join(date_directory, pcapng_file)

            with open(zst_file_path, 'rb') as zst_file_handle:
                dctx = zstd.ZstdDecompressor()
                with open(pcapng_file_path, 'wb') as pcapng_file_handle:
                    shutil.copyfileobj(dctx.stream_reader(zst_file_handle), pcapng_file_handle)

            # read .pcapng files and extract NDN names (may cause memory overflow)
            # packets = rdpcap(pcapng_file_path)
            # process_ndn_packets(packets, file)
            
            # use PcapNgReader to read .pcapng files per NDN names (to avoid memory overflow)
            pcap_reader = RawPcapNgReader(pcapng_file_path)
            for pkt_data, pkt_metadata in pcap_reader:
                try:
                    packet = Ether(pkt_data)
                    process_ndn_packets(packet, file)
                except Exception:
                    continue

            # delete .pcapng files
            os.remove(pcapng_file_path)

            processed_files += 1
            print(f"Processed {processed_files}/{total_files} files")

        processed_dates += 1
        print(f"Finished processing {date_path}\n")

print("NDN Names extracted and written to ndn_names.txt in each directory.")