import json

# بارگذاری فایل پیکربندی
try:
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        HF_TOKEN = config_data['HF_TOKEN']
except FileNotFoundError:
    print("File config.json not found.")
    exit(1)  # خاتمه دادن به برنامه در صورت عدم وجود فایل
except json.JSONDecodeError:
    print("Error decoding JSON from config.json.")
    exit(1)
