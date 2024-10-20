import logging
import json
import csv #Comma Separated Values

logger = logging.getLogger()
logger.setLevel('INFO')

def read_json(setting_file: str) -> dict:
    settings = None
    with open(setting_file) as f:
        settings = json.load(f)
    return settings

def write_card(card: str, filename: str) -> None:
    with open(filename, "w") as f:
        json.dump({"card_number": card}, f)

def load_statistics(filename: str) -> dict:
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        stats = list(reader)
    result = dict()
    for i in stats:
        processes, time = i
        result[int(processes)] = float(time)
    return result

def write_statistics(processes, time, filename) -> None:
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([processes, time])
    logging.info(f"Statistics written to a file {filename}")