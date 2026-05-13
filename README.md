# 🦠 Microbe Body Site Origin Mapping

A two-part pipeline to classify microbial species detected in **cfRNA data** by their body site of origin, using the **Disbiome database**, and visualize their distribution across longitudinal timepoints.

---

## Overview

This pipeline implements the body site classification approach described in Tan et al. (2023, *Nature Microbiology*), adapted for cfRNA-derived microbial profiles from Kraken2. The workflow consists of two parts:

- **Part 1 (Python):** Retrieve experiment data from the Disbiome API and map each microbial species to a standardized body site category
- **Part 2 (R):** Merge body site mappings with RUV-normalized Kraken2 species counts, and visualize mean species count per body site across timepoints

```
Disbiome API
     │
     ▼
[Python] microbe → sample type → body site mapping
     │
     ▼
microbe_body_sites_mapping.csv
     │
     ▼
[R] Merge with RUV-normalized Kraken2 counts + metadata
     │
     ▼
Line plot: mean species count per body site across timepoints (T1–T10)
```

---

## Part 1: Body Site Mapping (Python)

### Requirements

```bash
pip install requests pandas
```

> If running in **Google Colab**, both libraries are pre-installed and `google.colab.files` is available for file download.

### Usage

```bash
python microbe_body_site_mapping.py
```

### How It Works

1. Fetches all microbiome experiment data from the Disbiome API
2. Extracts unique organism–sample type pairs
3. Maps each sample type to a standardized body site via keyword matching
4. Removes unmapped (ambiguous) entries
5. Saves the result as `microbe_body_site_mapping.csv`

### Body Site Mapping Rules

Sample names are matched **case-insensitively**:

| Body Site | Sample Keywords |
|-----------|-----------------|
| `gut` | faeces, stool, rectal swab |
| `oral` | saliva, oral swab, tongue swab |
| `skin` | skin |
| `genitourinary tract` | urine, vaginal swab, cervical swab |
| `respiratory tract` | nasal, throat swab, sputum |
| `environmental_water` | water |
| `environmental_gravel` | gravel |
| `environmental_snow` | snow |
| *(unmapped)* | anything not matching → excluded |

### Output

| File | Description |
|------|-------------|
| `microbe_body_site_mapping.csv` | Organism–sample–body site mappings |

---

## Part 2: Visualization (R)

### Requirements

```r
install.packages(c("dplyr", "tidyr", "ggplot2", "readr", "tibble"))
```

### Input Files

| File | Description |
|------|-------------|
| `RUV_normalized_counts_species_global.csv` | RUV-normalized species count matrix from Kraken2 (rows = species, columns = samples) |
| `microbe_body_sites_mapping.csv` | Output from Part 1 |
| `metadatamcfrna.txt` | Sample metadata with `cfRNA_Label` and `timepoint` columns |

### How It Works

1. **Load and clean** the RUV-normalized species count matrix
2. **Extract genus** from species names — used only as a join key to match species against the body site mapping file
3. **Merge** species counts with body site mappings via genus-level join
4. **Flag multi-site genera** — species whose genus maps to more than one body site are assigned to a separate `"multiple"` category to avoid misclassification
5. **Pivot to long format** and filter for non-zero counts
6. **Join metadata** to attach timepoint labels (T1–T10) to each sample
7. **Summarize** mean number of species per body site per timepoint
8. **Plot** a line plot (log10 y-axis) of mean species count per body site across timepoints

> **Note:** The unit of analysis throughout is **species**. Genus is used solely as a join key because exact species name matching is not always consistent between the count matrix and the Disbiome mapping file.

### Output

A line plot showing the mean number of detected microbial species per body site origin across longitudinal timepoints (T1–T10), with body sites color-coded and a `"multiple"` category for species whose genus is associated with more than one body site.

---

## Notes

- Species whose maps to multiple body sites are grouped into a `"multiple"` category rather than being discarded, to preserve their signal
- The Disbiome API was originally accessed on 26 April 2022 in the reference paper; results may differ slightly with later access dates as the database is updated

---

## References

- **Method source**: Tan et al. (2023). *No evidence for a common blood microbiome based on a population study of 9,770 healthy humans.* Nature Microbiology, 8, 973–985. https://doi.org/10.1038/s41564-023-01350-w
- **Disbiome database**: Janssen et al. (2018). *Disbiome database: linking the microbiome to disease.* BMC Microbiology. https://doi.org/10.1186/s12866-018-1197-5
- **API endpoint**: https://disbiome.ugent.be:8080/experiment

---

## License

MIT License. See `LICENSE` for details.
