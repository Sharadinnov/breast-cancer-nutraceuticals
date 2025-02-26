import streamlit as st
import pandas as pd

# Load Excel file
def load_data():
    file_path = 'C:\\Users\\Admin\\Desktop\\Database for coding.xlsx'
    xl = pd.ExcelFile(file_path)
    mutations_df = xl.parse('Cancer To Gene')  # Load first sheet
    nutraceuticals_df = xl.parse('Gene to Nutraceutical')  # Load second sheet
    return mutations_df, nutraceuticals_df

# Load data
mutations_df, nutraceuticals_df = load_data()

# Streamlit UI
st.title("Breast Cancer Gene-Nutraceutical Mapping")

# Step 1: Select Breast Cancer Type (Added 'All' Option)
cancer_types = ['All'] + list(mutations_df['Breast Cancer Type'].unique())
selected_cancer = st.selectbox("Select Breast Cancer Type", cancer_types)

# Step 2: Show Mutated Genes for Selected Cancer Type
if selected_cancer == 'All':
    filtered_genes = mutations_df['Mutated Gene'].dropna().unique()
else:
    filtered_genes = mutations_df[mutations_df['Breast Cancer Type'] == selected_cancer]['Mutated Gene'].dropna().unique()

selected_genes = st.multiselect("Select Mutated Gene", filtered_genes, default=filtered_genes.tolist())

# Step 3: Show Nutraceuticals Mapping
if selected_genes:
    st.subheader("Selected Cancer Type & Genes")
    st.write(f"**Cancer Type:** {selected_cancer}")
    st.write(f"**Selected Genes:** {', '.join(selected_genes)}")

    # ✅ Correct filtering of nutraceuticals
    filtered_nutraceuticals = nutraceuticals_df[nutraceuticals_df['Top Biomarkers & Mutations'].isin(selected_genes)]

    # ✅ Add fresh numbering
    filtered_nutraceuticals = filtered_nutraceuticals.reset_index(drop=True)
    filtered_nutraceuticals.index += 1  # Start numbering from 1

    # ✅ Ensure all required columns are shown
    st.subheader("Mapped Nutraceuticals")
    st.dataframe(filtered_nutraceuticals[['Top Biomarkers & Mutations', 'Recommended Nutraceutical', 'Main Action', 'Publication Name', 'Summary', 'URL']])

    # ✅ Download option with fresh numbering
    csv = filtered_nutraceuticals.to_csv(index_label="Sr. No", index=True).encode('utf-8')
    st.download_button(label="Download Nutraceutical Data", data=csv, file_name="nutraceuticals_mapping.csv", mime="text/csv")

    ### 📌 NEW REPORT: UNIQUE RECOMMENDED NUTRACEUTICALS ###
    st.subheader("Unique Recommended Nutraceuticals")

    # ✅ Group by Nutraceutical, collect mutated genes
    grouped_nutraceuticals = (
        filtered_nutraceuticals.groupby("Recommended Nutraceutical")["Top Biomarkers & Mutations"]
        .apply(lambda x: ", ".join(sorted(set(x))))  # Unique genes, sorted, comma-separated
        .reset_index()
    )

    # ✅ Sort by the most frequently recommended Nutraceutical
    grouped_nutraceuticals["Count"] = grouped_nutraceuticals["Recommended Nutraceutical"].map(
        filtered_nutraceuticals["Recommended Nutraceutical"].value_counts()
    )
    grouped_nutraceuticals = grouped_nutraceuticals.sort_values(by="Count", ascending=False).drop(columns=["Count"])

    # ✅ Add fresh numbering
    grouped_nutraceuticals.index = range(1, len(grouped_nutraceuticals) + 1)
    grouped_nutraceuticals.index.name = "Sr. No"

    # ✅ Display the new unique report
    st.dataframe(grouped_nutraceuticals)

    # ✅ Download option for unique nutraceuticals report
    csv_nutraceuticals = grouped_nutraceuticals.to_csv().encode('utf-8')
    st.download_button(label="Download Unique Nutraceuticals Report", data=csv_nutraceuticals, file_name="unique_nutraceuticals.csv", mime="text/csv")
