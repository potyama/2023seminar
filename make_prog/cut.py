import csv
import os
import re
import argparse

text_directory = "/path/to/org"
csv_directory = "/path/to/buf"

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-a", "--dates", nargs="+", help="Dates in the format YYYYMMDD")
group.add_argument("-All", action="store_true", help="Convert all text files to CSV")
args = parser.parse_args()

if args.dates:
    for date in args.dates:
        csv_file = os.path.join(csv_directory, f"{date}.csv")
        if not os.path.exists(csv_file):
            txt_file = os.path.join(text_directory, f"{date}.txt")

            if os.path.exists(txt_file):
                with open(txt_file, "r") as file:
                    lines = file.readlines()

                # CSVファイルのヘッダーを設定
                header = [
                    "Duration", "Service", "Source bytes", "Destination bytes",
                    "Count", "Same_srv_rate", "Serror_rate", "Srv_serror_rate",
                    "Dst_host_count", "Dst_host_srv_count", "Dst_host_same_src_port_rate",
                    "Dst_host_serror_rate", "Dst_host_srv_serror_rate", "Flag",
                    "IDS_detection", "Malware_detection", "Ashula_detection", "Label",
                    "Source_IP_Address", "Source_Port_Number", "Destination_IP_Address",
                    "Destination_Port_Number", "Start_Time", "Protocol"
                ]

                # CSVファイルに書き込むデータを格納するリスト
                data = []

                for line in lines:
                    line = line.strip()
                    cols = line.split("\t")
                    data.append(cols)

                # CSVファイルにデータを書き込む
                with open(csv_file, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(data)

                print(f"変換が完了しました。出力ファイル: {csv_file}")
            else:
                print(f"テキストファイルが見つかりませんでした。ファイル名: {txt_file}")
        else:
            print(f"CSVファイルは既に存在します。スキップします。ファイル名: {csv_file}")
elif args.All:
    # テキストファイルのパスを取得
    text_files = [f for f in os.listdir(text_directory) if f.endswith(".txt")]

    for text_file in text_files:
        # 日付を抽出
        match = re.search(r"(\d{8})", text_file)
        if match:
            date = match.group(1)
            csv_file = os.path.join(csv_directory, f"{date}.csv")
            if not os.path.exists(csv_file):
                txt_file = os.path.join(text_directory, text_file)

                with open(txt_file, "r") as file:
                    lines = file.readlines()

                # CSVファイルのヘッダーを設定
                header = [
                    "Duration", "Service", "Source bytes", "Destination bytes",
                    "Count", "Same_srv_rate", "Serror_rate", "Srv_serror_rate",
                    "Dst_host_count", "Dst_host_srv_count", "Dst_host_same_src_port_rate",
                    "Dst_host_serror_rate", "Dst_host_srv_serror_rate", "Flag",
                    "IDS_detection", "Malware_detection", "Ashula_detection", "Label",
                    "Source_IP_Address", "Source_Port_Number", "Destination_IP_Address",
                    "Destination_Port_Number", "Start_Time", "Protocol"
                ]

                # CSVファイルに書き込むデータを格納するリスト
                data = []

                for line in lines:
                    line = line.strip()
                    cols = line.split("\t")
                    data.append(cols)

                # CSVファイルにデータを書き込む
                with open(csv_file, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerows(data)

                print(f"変換が完了しました。出力ファイル: {csv_file}")
            else:
                print(f"CSVファイルは既に存在します。スキップします。ファイル名: {csv_file}")
        else:
            print(f"日付の抽出に失敗しました。ファイル名: {text_file}")
