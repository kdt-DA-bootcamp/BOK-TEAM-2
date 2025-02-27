import pandas as pd
from tqdm import tqdm
from pykospacing import Spacing

tqdm.pandas()
spacing = Spacing()

def restore_spacing_only(text):
    if pd.isna(text):
        return ""
    if not isinstance(text, str):
        text = str(text)
    return spacing(text)

def process_csv_file(input_file: str, output_file: str):
    df = pd.read_csv(input_file)

    df['contents'] = df['contents'].progress_apply(restore_spacing_only)
    
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_csv = "filtered_bond_results.csv"
    output_csv = "preprocessed_bond_results.csv"

    process_csv_file(input_csv, output_csv)