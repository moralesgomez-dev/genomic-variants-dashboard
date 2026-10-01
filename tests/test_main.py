import subprocess
import sys
from pathlib import Path

import pandas as pd


def test_process_vcf_writes_expected_csvs(tmp_path):
    vcf_path = tmp_path / "variants.vcf"
    output_dir = tmp_path / "processed"
    vcf_path.write_text(
        "##fileformat=VCFv4.2\n"
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n"
        "22\t100\t.\tA\tG\t100\tPASS\tEAS_AF=0.25;AMR_AF=0.5;AFR_AF=0.1;"
        "EUR_AF=0.2;SAS_AF=0.3;VT=SNP\tGT\n",
        encoding="utf-8",
    )

    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / "src" / "variantes_genomicas" / "explore_vcf.py"
    subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--input-vcf",
            str(vcf_path),
            "--output-dir",
            str(output_dir),
        ],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )

    final_df = pd.read_csv(output_dir / "final_variants_chr22.csv")
    plain_tableau_df = pd.read_csv(output_dir / "tableau_variants_chr22.csv")
    tableau_df = pd.read_csv(output_dir / "tableau_variants_chr22_with_variant_id.csv")

    assert len(final_df) == 1
    assert final_df.loc[0, "EAS_AF"] == 0.25
    assert "VariantID" not in plain_tableau_df.columns
    assert list(tableau_df["population"]) == ["EAS", "AMR", "AFR", "EUR", "SAS"]
    assert tableau_df["VariantID"].tolist() == [0, 0, 0, 0, 0]
