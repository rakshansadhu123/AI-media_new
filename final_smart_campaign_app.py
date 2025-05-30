
import streamlit as st
import pandas as pd
import io
from campaign_summary import generate_campaign_summary
from ai_comparison import compare_campaigns_with_ai

st.set_page_config(page_title="🧠 Smart Media Comparator", layout="wide")
st.title("🧠 Smart Media Comparator")

# Upload files
benchmark_file = st.file_uploader("📊 Upload Benchmark File", type=["xlsx"], key="benchmark")
current_file = st.file_uploader("📂 Upload Current Campaign File (Excel with sheets)", type=["xlsx"], key="current")
previous_file = st.file_uploader("📁 Upload Previous Campaign File (Excel with sheets)", type=["xlsx"], key="previous")

def extract_sheets(file):
    """Return cleaned, non-empty dataframes from Excel file sheets"""
    try:
        sheets = pd.read_excel(file, sheet_name=None)
        dfs = []
        for name, df in sheets.items():
            df.columns = [c.strip().lower() for c in df.columns if isinstance(c, str)]
            if df.empty: continue
            df = df.copy()
            rename_map = {
                'cost': 'Spend (£)', 'spend': 'Spend (£)',
                'views': 'Impressions', 'impressions': 'Impressions',
                'clicks': 'Clicks', 'conversions': 'Conversions',
                'revenue': 'Revenue (£)'
            }
            df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)
            for col in ['Spend (£)', 'Impressions', 'Clicks', 'Conversions', 'Revenue (£)']:
                if col not in df.columns:
                    df[col] = 0
            df['CPM (£)'] = df['Spend (£)'] / (df['Impressions'] / 1000).replace(0, pd.NA)
            df['CTR (%)'] = (df['Clicks'] / df['Impressions']).replace(0, pd.NA) * 100
            df['CPC (£)'] = df['Spend (£)'] / df['Clicks'].replace(0, pd.NA)
            df['ROAS'] = df['Revenue (£)'] / df['Spend (£)'].replace(0, pd.NA)
            df['Conversion Rate (%)'] = df['Conversions'] / df['Clicks'].replace(0, pd.NA) * 100
            dfs.append(df)
        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    except Exception as e:
        st.error(f"Error processing Excel: {e}")
        return pd.DataFrame()

if benchmark_file and current_file and previous_file:
    try:
        benchmark_df = pd.read_excel(benchmark_file)
        benchmark_df.columns = [c.strip().lower() for c in benchmark_df.columns]
        benchmark_df.rename(columns={
            'channel': 'Channel',
            'benchmark cpm': 'Benchmark CPM',
            'benchmark roas': 'Benchmark ROAS'
        }, inplace=True)

        # Process campaign files
        current_df = extract_sheets(current_file)
        previous_df = extract_sheets(previous_file)

        st.success("✅ All files loaded and processed.")
        st.write("### 📊 Current Campaign Data")
        st.dataframe(current_df.head())
        st.write("### 📁 Previous Campaign Data")
        st.dataframe(previous_df.head())

        # Generate summaries
        current_summary = generate_campaign_summary(current_df, "Current Campaign")
        previous_summary = generate_campaign_summary(previous_df, "Previous Campaign")
        benchmark_summary = benchmark_df.to_string(index=False)

        # Run AI comparison
        with st.spinner("🤖 Generating AI summary..."):
            ai_insight = compare_campaigns_with_ai(current_summary, previous_summary, benchmark_summary)

        st.markdown("## 🧠 AI Campaign Summary + Recommendations")
        st.markdown(ai_insight)

        # Export to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            current_df.to_excel(writer, index=False, sheet_name="Current Campaign")
            previous_df.to_excel(writer, index=False, sheet_name="Previous Campaign")
            benchmark_df.to_excel(writer, index=False, sheet_name="Benchmark")
            pd.DataFrame({"AI Summary": [ai_insight]}).to_excel(writer, index=False, sheet_name="AI Summary")

        st.download_button("📥 Download Excel Report", output.getvalue(), file_name="AI_Campaign_Analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
else:
    st.info("📌 Please upload all three files to begin.")
