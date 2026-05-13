import requests
import pandas as pd
from google.colab import files

# 1. Ambil data JSON
url = "https://disbiome.ugent.be:8080/experiment"
data = requests.get(url).json()

# 2. Buat dataframe dan ambil kolom penting
df = pd.DataFrame(data)
microbe_sample = df[['organism_name', 'sample_name']].drop_duplicates()

# 3. Mapping sample_name → body_site
def map_body_site(sample):
    sample_lower = str(sample).lower()  # case-insensitive
    # Tubuh manusia
    if any(x in sample_lower for x in ["faeces", "stool", "rectal swab"]):
        return "gut"
    elif any(x in sample_lower for x in ["saliva", "oral swab", "tongue swab"]):
        return "oral"
    elif "skin" in sample_lower:
        return "skin"
    elif any(x in sample_lower for x in ["urine", "vaginal swab", "cervical swab"]):
        return "genitourinary tract"
    elif any(x in sample_lower for x in ["nasal", "throat swab", "sputum"]):
        return "respiratory tract"
    # Lingkungan spesifik
    elif "water" in sample_lower:
        return "environmental_water"
    elif "gravel" in sample_lower:
        return "environmental_gravel"
    elif "snow" in sample_lower:
        return "environmental_snow"
    else:
        return None  # yang ambiguous

# 4. Terapkan mapping
microbe_sample['body_site'] = microbe_sample['sample_name'].apply(map_body_site)

# 5. Hapus yang tidak ter-mapping
microbe_body_site = microbe_sample.dropna(subset=['body_site'])

# 6. Simpan CSV
microbe_body_site.to_csv("microbe_body_site_mapping.csv", index=False)

# 7. Download CSV
files.download("microbe_body_site_mapping.csv")

# 8. Opsional: lihat ringkasan jumlah per body_site
print(microbe_body_site['body_site'].value_counts())
