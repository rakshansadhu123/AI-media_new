
import pandas as pd

def generate_campaign_summary(df: pd.DataFrame, campaign_name: str = "Campaign") -> str:
    """
    Generate a structured summary string from a media campaign DataFrame
    """
    summary = []

    # Basic stats
    total_spend = df['Spend (£)'].sum()
    total_impressions = df['Impressions'].sum()
    avg_roas = df['ROAS'].mean()
    avg_cpm = df['CPM (£)'].mean()
    avg_ctr = df['CTR (%)'].mean()
    avg_conversion_rate = df['Conversion Rate (%)'].mean()

    summary.append(f"📊 **{campaign_name} Summary**")
    summary.append(f"- Total Spend: £{total_spend:,.2f}")
    summary.append(f"- Total Impressions: {total_impressions:,.0f}")
    summary.append(f"- Average ROAS: {avg_roas:.2f}")
    summary.append(f"- Average CPM: £{avg_cpm:.2f}")
    summary.append(f"- Average CTR: {avg_ctr:.2f}%")
    summary.append(f"- Average Conversion Rate: {avg_conversion_rate:.2f}%")

    if 'Channel' in df.columns:
        channels = df['Channel'].unique()
        summary.append(f"- Channels: {', '.join(map(str, channels))}")

    if 'CPM Status' in df.columns:
        below_benchmark = df[df['CPM Status'] == 'Below Benchmark']
        summary.append(f"- Below Benchmark (CPM): {len(below_benchmark)} entries")

    if 'ROAS Status' in df.columns:
        below_roas = df[df['ROAS Status'] == 'Below Benchmark']
        summary.append(f"- Below Benchmark (ROAS): {len(below_roas)} entries")

    return "\n".join(summary)
