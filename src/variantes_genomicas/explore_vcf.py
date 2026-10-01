import argparse
import gzip
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_VCF_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz"
)
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
VARIANT_COLUMNS = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT"]
AF_COLUMNS = ["EAS_AF", "AMR_AF", "AFR_AF", "EUR_AF", "SAS_AF"]
INFO_COLUMNS = [*AF_COLUMNS, "VT"]


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process the chromosome 22 VCF for EDA and Tableau."
    )
    parser.add_argument("--input-vcf", type=Path, default=DEFAULT_VCF_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    output_path = args.output_dir
    output_path.mkdir(parents=True, exist_ok=True)

    variants = read_vcf(args.input_vcf).loc[:, VARIANT_COLUMNS]
    variants.to_csv(output_path / "variants_chr22.csv", index=False)

    info_rows = []
    for info in variants["INFO"]:
        info_row = {}
        for item in str(info).split(";"):
            if "=" in item:
                key, value = item.split("=", 1)
                info_row[key] = value
        info_rows.append(info_row)

    info_df = pd.DataFrame(info_rows).reindex(columns=INFO_COLUMNS)
    for column in AF_COLUMNS:
        info_df[column] = pd.to_numeric(info_df[column], errors="coerce")
    info_df.to_csv(output_path / "info_chr22.csv", index=False)

    final_df = pd.concat([variants.drop(columns="INFO"), info_df], axis=1)
    final_df.to_csv(output_path / "final_variants_chr22.csv", index=False)

    tableau_variants = final_df.melt(
        id_vars=[column for column in final_df.columns if column not in AF_COLUMNS],
        value_vars=AF_COLUMNS,
        var_name="population",
        value_name="Allele Frequency",
    )
    tableau_variants["population"] = tableau_variants["population"].str.removesuffix("_AF")
    tableau_variants.to_csv(output_path / "tableau_variants_chr22.csv", index=False)

    variant_count = len(final_df)
    expected_rows = variant_count * len(AF_COLUMNS)
    if len(tableau_variants) != expected_rows:
        raise ValueError("The long-form CSV must contain five rows per original variant.")

    tableau_variants["VariantID"] = np.tile(
        np.arange(variant_count, dtype="int64"),
        len(AF_COLUMNS),
    )
    variant_ids = tableau_variants["VariantID"].to_numpy().reshape(len(AF_COLUMNS), variant_count)
    expected_ids = np.broadcast_to(np.arange(variant_count), variant_ids.shape)
    if not np.array_equal(variant_ids, expected_ids):
        raise ValueError("Each original variant must have the same VariantID in all populations.")

    tableau_variants.to_csv(
        output_path / "tableau_variants_chr22_with_variant_id.csv",
        index=False,
    )
    print(f"Processed VCF outputs written to {args.output_dir.resolve()}")
