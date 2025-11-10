import os
import torch
import pandas as pd
import json
from tqdm import tqdm
from lognexus.model import LogNexusModel

REQUIRED_COLUMNS = ['date', 'time', 'message']

def load_and_extract_log(filepath):
    """
    Reads a raw flight log and extracts only necessary columns.
    Matches columns case-insensitively.
    """
    # validate the decrypted flight logs
    try:
        with open(filepath, 'r') as file:
            date = []
            time = []
            message_type = []
            message = []

            file_df = pd.read_csv(os.path.join(filepath), skiprows=1) # since the first row contains sep=,
            timeline_df = file_df[['CUSTOM.date [local]', 'CUSTOM.updateTime [local]', 'APP.tip', 'APP.warning']]
            for i, row in timeline_df.iterrows():
                if not pd.isna(row['APP.tip']):
                    date.append(row['CUSTOM.date [local]'])
                    time.append(row['CUSTOM.updateTime [local]'])
                    message_type.append('tip')
                    message.append(row['APP.tip'])
                if not pd.isna(row['APP.warning']):
                    date.append(row['CUSTOM.date [local]'])
                    time.append(row['CUSTOM.updateTime [local]'])
                    message_type.append('warning')
                    message.append(row['APP.warning'])
            parsed_df = pd.DataFrame({
                'date': date,
                'time': time,
                'message_type': message_type,
                'message': message
            })

            return parsed_df[REQUIRED_COLUMNS].copy()
            
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")


def process_logs(input_dir, output_dir, model_path, output_format='xlsx', use_cuda=False):
    print(f"[-] Loading LogNexus model from: {model_path}")
    try:
        if use_cuda:
            if not torch.cuda.is_available():
                print("[!] CUDA requested but not available. Falling back to CPU.")
                use_cuda = False
        ner_model = LogNexusModel(model_path, use_cuda=use_cuda)
    except Exception as e:
        print(f"[!] Model loading failed: {e}")
        return
    print("[+] Model loaded successfully.")

    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith(('.xlsx', '.xls', '.csv'))]

    if not files:
        print(f"[!] No log files found in {input_dir}")
        return

    print(f"[-] Found {len(files)} log file(s). Start processing...")

    for file in tqdm(files, desc="Processing"):
        input_path = os.path.join(input_dir, file)
        try:
            # 1. Load and extract relevant columns from raw log
            df = load_and_extract_log(input_path)

            # 2. Prepare messages
            messages = df['message'].fillna("").astype(str).tolist()

            # 3. Inference
            df['sentence'] = ner_model.predict_sentences(messages)

            # 4. Save Output
            if output_format == 'json':
                out_file = os.path.splitext(file)[0] + '.json'
                with open(os.path.join(output_dir, out_file), 'w') as f:
                    json.dump(df.to_dict(orient='records'), f, indent=2, default=str)
            else:
                out_file = os.path.splitext(file)[0] + '_processed.xlsx'
                df.explode('sentence').to_excel(os.path.join(output_dir, out_file), index=False)

        except Exception as e:
            print(f"[!] Error processing {file}: {e}")

    print(f"[+] Completed. Results in: {output_dir}")