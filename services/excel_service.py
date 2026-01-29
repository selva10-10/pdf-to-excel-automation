import pandas as pd
import os


def create_excel(key_info, tables, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

        # Sheet 1 — Summary Info
        summary_df = pd.DataFrame([key_info])
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

        # Sheet 2 — Extracted Tables (if any)
        if tables:
            for i, table in enumerate(tables):
                df = pd.DataFrame(table)
                df.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)

        # Sheet 3 — Raw Text
        text_df = pd.DataFrame({"Extracted Text": [key_info["full_text"]]})
        text_df.to_excel(writer, sheet_name="Raw_Text", index=False)

    print("Excel created with structured data.")
