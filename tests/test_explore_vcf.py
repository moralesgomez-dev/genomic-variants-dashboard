import gzip

from variantes_genomicas.explore_vcf import read_vcf


def test_read_vcf_uses_chrom_header_as_column_names(tmp_path):
    vcf_path = tmp_path / "variants.vcf.gz"
    with gzip.open(vcf_path, "wt", encoding="utf-8") as file:
        file.write("##fileformat=VCFv4.2\n")
        file.write("#CHROM\tPOS\tID\tREF\tALT\n")
        file.write("22\t100\t.\tA\tG\n")

    result = read_vcf(vcf_path)

    assert list(result.columns) == ["CHROM", "POS", "ID", "REF", "ALT"]
    assert result.iloc[0]["CHROM"] == 22