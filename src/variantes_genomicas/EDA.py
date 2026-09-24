import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Configuración visual compartida para los gráficos del proyecto
sns.set_theme(
	style="whitegrid",
	context="notebook",
	font="DejaVu Sans",
	rc={
		"figure.figsize": (10, 6),
		"figure.dpi": 120,
		"axes.titlesize": 16,
		"axes.titleweight": "bold",
		"axes.labelsize": 12,
		"axes.labelcolor": "#243447",
		"xtick.labelsize": 10,
		"ytick.labelsize": 10,
		"text.color": "#243447",
		"axes.edgecolor": "#B8C2CC",
		"grid.color": "#DCE3E8",
		"grid.linewidth": 0.8,
		"legend.frameon": False,
		"savefig.dpi": 300,
		"savefig.bbox": "tight",
	},
)

PALETTE = {
	"EAS_AF": "#007C91",
	"AMR_AF": "#E76F51",
	"AFR_AF": "#2A9D8F",
	"EUR_AF": "#264653",
	"SAS_AF": "#E9C46A",
	"SNP": "#007C91",
	"INDEL": "#E76F51",
    "VT": "#2A9D8F"
}

BASE_PALETTE = {
	"A": "#007C91",
	"C": "#E76F51",
	"G": "#2A9D8F",
	"T": "#E9C46A",
}

#Carga de datos
df_variants = pd.read_csv("C:\\Users\\alexm\\Entornos\\genomic_variants_dashboard\\data\\processed\\final_variants_chr22.csv")

# Cargar el CSV procesado y revisar shape, tipos de datos y nulos
print("Shape:", df_variants.shape)
print("Columns:", df_variants.columns)
print("Data types:", df_variants.dtypes)
print("DF Info:", df_variants.info())
print("DF Describe:", df_variants.describe())

print("Missing count:", df_variants.isna().sum())
print("Percentage:", df_variants.isna().sum() / len(df_variants) * 100)
# Procederemos despues a eliminar las filas que presentan valres nulos, porque suponen un 0.5% aprox

# Vemos un poco cada columna
#CHROM - nos indica el cromosoma donde se encuentra la variante, en este caso es el 22, por lo que no aporta información relevante. Podemos eliminarla.
print(df_variants["CHROM"].sample(5))

# POS - nos indica la posición del cromosoma donde se encuentra la variante
plt.figure(figsize=(11, 6))
sns.histplot(
	data=df_variants,
	x="POS",
	bins=60,
	kde=False,
	color=PALETTE["EUR_AF"],
)
plt.title('Distribution of Variant Positions on Chromosome 22')
plt.xlabel('Chromosomal position')
plt.ylabel('Number of variants')
plt.tight_layout()
plt.savefig("results\\results\\figures\\POS_Distribution.png")
plt.show()

# ID - nos indica el identificador de la variante, si no tiene, es un punto (.) Como hemos visto no tiene ID, por lo que no nos aporta información relevante. Podemos eliminarla.
print(df_variants["ID"].sample(5))

# REF puede ser una base individual o una secuencia de varias bases, por eso mostramos los 15 alelos más frecuentes.
ref_order = df_variants["REF"].value_counts().head(15).index
ref_data = df_variants[df_variants["REF"].isin(ref_order)]
ref_colors = sns.color_palette("crest", n_colors=len(ref_order))

plt.figure(figsize=(11, 6))
sns.countplot(
	data=ref_data,
    x="REF",
	order=ref_order,
	hue="REF",
	palette=ref_colors,
	legend=False,
)
plt.title("Most Frequent Reference Alleles in Variants")
plt.xlabel("Reference allele")
plt.ylabel("Number of variants (log scale)")
plt.yscale("log")
plt.tight_layout()
plt.savefig("results\\results\\figures\\REF_count.png")
plt.show()

# ALT - nos indica los alelos alternativos en esa posicion
print(df_variants["ALT"].sample(5))
#de la misma manera que REF, puede ser una base individual o una secuencia de varias bases, por eso mostramos los 15 alelos más frecuentes.
alt_order = df_variants["ALT"].value_counts().head(15).index
alt_data = df_variants[df_variants["ALT"].isin(alt_order)]
alt_colors = sns.color_palette("mako", n_colors=len(alt_order))

plt.figure(figsize=(11, 6))
sns.countplot(
	data=alt_data,
	x="ALT",
	order=alt_order,
	hue="ALT",
	palette=alt_colors,
	legend=False,
)
plt.title("Most Frequent Alternative Alleles in Variants")
plt.xlabel("Alternative allele")
plt.ylabel("Number of variants (log scale)")
plt.yscale("log")
plt.tight_layout()
plt.savefig("results\\results\\figures\\ALT_count.png")
plt.show()

# QUAL - nos indica la calidad de la variante, es un valor numérico que indica la confianza en la llamada de variante. Podemos visualizar su distribución.
print(df_variants["QUAL"].sample(5))
print(df_variants["QUAL"].value_counts())


# La calidad es 100 siempre, por lo que no aporta información relevante. Podemos eliminarla.

# FILTER - es una flag que nos indica si la variante ha pasado los filtros de calidad. Podemos visualizar su distribución.
print(df_variants["FILTER"].sample(5))
print(df_variants["FILTER"].value_counts())

# El valor del flag es siempre PASS, por lo que no aporta información relevante. Podemos eliminarla.

# FORMAT - Nos idnica una descripcion del sample, GT en este caso, que nos indica el genotipo de la variante. Podemos visualizar su distribución.
print(df_variants["FORMAT"].sample(5))
print(df_variants["FORMAT"].value_counts())

# Tenemos varios valores dentro del campo INFO:
# EAS_AF - Frecuencia alelica para cada alelo alternativo en la población East Asian (EAS). Valor numérico entre 0 y 1 que indica la proporción de alelos alternativos en la población EAS.
print(df_variants["EAS_AF"].sample(5))
print(df_variants["EAS_AF"].describe())

plt.figure(figsize=(11, 6))
sns.histplot(
	data=df_variants,
	x="EAS_AF",
	bins=30,
	kde=True,
	color=PALETTE["EAS_AF"],
)
plt.title("Distribution of East Asian Allele Frequencies (EAS_AF)")
plt.yscale("log")
plt.xlabel("EAS_AF")
plt.ylabel("Number of variants (Log scale)")
plt.tight_layout()
plt.savefig("results\\results\\figures\\EAS_Distribution.png")
plt.show()

# AMR_AF - Frecuencia alelica para cada alelo alternativo en la población Admixed American (AMR). Valor numérico entre 0 y 1 que indica la proporción de alelos alternativos en la población AMR.
print(df_variants["AMR_AF"].sample(5))
print(df_variants["AMR_AF"].describe())

plt.figure(figsize=(11, 6))
sns.histplot(
	data=df_variants,
	x="AMR_AF",
	bins=30,
	kde=True,
	color=PALETTE["AMR_AF"],
)
plt.title("Distribution of Admixed American Allele Frequencies (AMR_AF)")
plt.yscale("log")
plt.xlabel("AMR_AF")
plt.ylabel("Number of variants (Log scale)")
plt.tight_layout()
plt.savefig("results\\results\\figures\\AMR_Distribution.png")
plt.show()

# AFR_AF - Frecuencia alelica para cada alelo alternativo en la población Africana (AFR). Valor numérico entre 0 y 1 que indica la proporción de alelos alternativos en la población AFR.
print(df_variants["AFR_AF"].sample(5))
print(df_variants["AFR_AF"].describe())

plt.figure(figsize=(11, 6))
sns.histplot(
	data=df_variants,
	x="AFR_AF",
	bins=30,
	kde=True,
	color=PALETTE["AFR_AF"],
)
plt.title("Distribution of Admixed American Allele Frequencies (AFR_AF)")
plt.yscale("log")
plt.xlabel("AFR_AF")
plt.ylabel("Number of variants (Log scale)")
plt.tight_layout()
plt.savefig("results\\results\\figures\\AFR_Distribution.png")
plt.show()

# EUR_AF - Frecuencia alelica para cada alelo alternativo en la población Europea (EUR). Valor numérico entre 0 y 1 que indica la proporción de alelos alternativos en la población EUR.
print(df_variants["EUR_AF"].sample(5))
print(df_variants["EUR_AF"].describe())

plt.figure(figsize=(11, 6))
sns.histplot(
	data=df_variants,
	x="EUR_AF",
	bins=30,
	kde=True,
	color=PALETTE["EUR_AF"],
)
plt.title("Distribution of Admixed American Allele Frequencies (EUR_AF)")
plt.yscale("log")
plt.xlabel("EUR_AF")
plt.ylabel("Number of variants (Log scale)")
plt.tight_layout()
plt.savefig("results\\results\\figures\\EUR_Distribution.png")
plt.show()

# SAS_AF - Frecuencia alelica para cada alelo alternativo en la población Sur Asiatica (SAS). Valor numérico entre 0 y 1 que indica la proporción de alelos alternativos en la población SAS.
print(df_variants["SAS_AF"].sample(5))
print(df_variants["SAS_AF"].describe())

plt.figure(figsize=(11, 6))
sns.histplot(
	data=df_variants,
	x="SAS_AF",
	bins=30,
	kde=True,
	color=PALETTE["SAS_AF"],
)
plt.title("Distribution of Admixed American Allele Frequencies (SAS_AF)")
plt.yscale("log")
plt.xlabel("SAS_AF")
plt.ylabel("Number of variants (Log scale)")
plt.tight_layout()
plt.savefig("results\\results\\figures\\SAS_Distribution.png")
plt.show()

# VT - indioca el tipo de variante genomica
print(df_variants["VT"].sample(5))
print(df_variants["VT"].value_counts())

plt.figure(figsize=(11, 6))
sns.countplot(
    data=df_variants,
    x="VT",
    color=PALETTE["VT"],
    hue="VT",
    legend=False
)
plt.title("Frecuency of Variant Type (VT INFO field)")
plt.yscale("log")
plt.xlabel("Genetic Variant Type")
plt.ylabel("Number of variants (log scale)")
plt.tight_layout()
plt.savefig("results\\results\\figures\\VT_frecuency.png")
plt.show()

# BOXPLOT de distribucion de frecuencias alelicas por poblacion
poblaciones = ["EAS_AF", "AFR_AF", "AMR_AF", "SAS_AF", "EUR_AF"]

allele_frequency_df = (
    df_variants[poblaciones]
    .rename(columns={
        "EAS_AF": "EAS",
        "AFR_AF": "AFR",
        "AMR_AF": "AMR",
        "SAS_AF": "SAS",
        "EUR_AF": "EUR",
    })
    .melt(var_name="Population", value_name="Allele frequency")
)

palette_by_population = {
    "EAS": PALETTE["EAS_AF"],
    "AFR": PALETTE["AFR_AF"],
    "AMR": PALETTE["AMR_AF"],
    "SAS": PALETTE["SAS_AF"],
    "EUR": PALETTE["EUR_AF"],
}

plt.figure(figsize=(11, 6))
sns.boxplot(
    data=allele_frequency_df,
    x="Population",
    y="Allele frequency",
    order=["EAS", "AFR", "AMR", "SAS", "EUR"],
    palette=[palette_by_population[p] for p in ["EAS", "AFR", "AMR", "SAS", "EUR"]],
)
plt.title("Distribution of Allele Frequency by Population")
plt.yscale("log")
plt.xlabel("Population")
plt.ylabel("Allele frequency")
plt.tight_layout()
plt.savefig("results\\results\\figures\\boxplot.png")
plt.show()

plt.figure(figsize=(11, 6))
sns.violinplot(
    data=allele_frequency_df,
    x="Population",
    y="Allele frequency",
    order=["EAS", "AFR", "AMR", "SAS", "EUR"],
    palette=[palette_by_population[p] for p in ["EAS", "AFR", "AMR", "SAS", "EUR"]],
)
plt.title("Distribution of Allele Frequency by Population")
plt.yscale("log")
plt.xlabel("Population")
plt.ylabel("Allele frequency")
plt.tight_layout()
plt.savefig("results\\results\\figures\\violinplot.png")
plt.show()


