import gzip
from pathlib import Path

import pandas as pd


def read_vcf(vcf_file: str | Path) -> pd.DataFrame:
    """Read a VCF file using the columns declared in its #CHROM header."""
    vcf_path = Path(vcf_file)
    opener = gzip.open if vcf_path.suffix == ".gz" else open

    with opener(vcf_path, "rt", encoding="utf-8") as file:
        for line in file:
            if line.startswith("#CHROM"):
                columns = line.rstrip("\r\n").split("\t")
                columns[0] = columns[0].removeprefix("#")
                break
        else:
            raise ValueError("The VCF file does not contain a #CHROM header.")

    return pd.read_csv(
        vcf_path,
        sep="\t",
        comment="#",
        header=None,
        names=columns,
        compression="infer",
    )

vcf_file = "C:\\Users\\alexm\\Entornos\\genomic_variants_dashboard\\data\\raw\\ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz"

df_variants = read_vcf(vcf_file)

print(df_variants.head())
print(df_variants.columns)
print(df_variants.shape)

# Nos quedamos solo con las columnas que nos interesan
df_variants = df_variants[['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT']]
print(df_variants.head())
print(df_variants.columns)
print(df_variants.shape)

df_variants.to_csv("C:\\Users\\alexm\\Entornos\\genomic_variants_dashboard\\data\\processed\\variants_chr22.csv", index=False)
df_variants_processed = pd.read_csv("C:\\Users\\alexm\\Entornos\\genomic_variants_dashboard\\data\\processed\\variants_chr22.csv")

info_rows = []

for info in df_variants_processed["INFO"]:
    row = {}
    for item in str(info).split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            row[key] = value
    info_rows.append(row)

info_df = pd.DataFrame(info_rows)
print(info_df.head())
print(info_df.shape)
print(info_df.columns)

wanted = ["EAS_AF", "AMR_AF", "AFR_AF", "EUR_AF", "SAS_AF", "VT"]
info_df = info_df[wanted]

numeric_columns = ["EAS_AF", "AMR_AF", "AFR_AF", "EUR_AF", "SAS_AF"]
for col in numeric_columns:
    info_df[col] = pd.to_numeric(info_df[col], errors="coerce")

print(info_df.head())

info_df.to_csv("C:\\Users\\alexm\\Entornos\\genomic_variants_dashboard\\data\\processed\\info_chr22.csv", index=False)

#Juntando los dos dataframes
df_variants_processed.drop(columns=["INFO"], inplace=True)
final_df = pd.concat([df_variants_processed, info_df], axis=1)
print(final_df.head())
final_df.to_csv("C:\\Users\\alexm\\Entornos\\genomic_variants_dashboard\\data\\processed\\final_variants_chr22.csv", index=False)