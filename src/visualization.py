"""
Visualization Engine for Lead Conversion Funnel Analysis
Generates modern, interactive Plotly charts adhering to an enterprise design palette.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Enterprise Palette (Tailwind-aligned)
COLOR_PRIMARY = "#4F46E5"    # Indigo 600
COLOR_SECONDARY = "#06B6D4"  # Cyan 500
COLOR_SUCCESS = "#10B981"    # Emerald 500
COLOR_WARNING = "#F59E0B"    # Amber 500
COLOR_DANGER = "#EF4444"     # Rose 500
COLOR_PURPLE = "#8B5CF6"     # Purple 500
COLOR_SLATE = "#64748B"      # Slate 500

CHART_THEME = {
    "font": {"family": "Inter, system-ui, sans-serif", "size": 12, "color": "#1E293B"},
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": {"l": 40, "r": 40, "t": 50, "b": 40},
}

def create_funnel_chart(stages_df: pd.DataFrame) -> go.Figure:
    """Renders a sleek Plotly Funnel Chart with stage retention and drop-off annotations."""
    if len(stages_df) == 0:
        return go.Figure()

    fig = go.Figure(go.Funnel(
        y=stages_df["stage"],
        x=stages_df["lead_count"],
        textinfo="value+percent previous",
        texttemplate="<b>%{value}</b> leads<br>(%{percentPrevious:.1f}%)",
        hoverinfo="x+y+percent initial+percent previous",
        marker={
            "color": [
                "#312E81", # Indigo 900
                "#3730A3", # Indigo 800
                "#4338CA", # Indigo 700
                "#4F46E5", # Indigo 600
                "#6366F1", # Indigo 500
                "#10B981"  # Emerald 500 (Converted)
            ],
            "line": {"width": 1.5, "color": "#FFFFFF"}
        },
        connector={"line": {"color": "#CBD5E1", "width": 1.5, "dash": "dot"}}
    ))

    fig.update_layout(
        title="<b>Sales Funnel Stage Transition & Drop-off Flow</b>",
        title_font={"size": 16, "family": "Inter, sans-serif"},
        **CHART_THEME
    )
    return fig

def create_conversion_trend_chart(monthly_df: pd.DataFrame) -> go.Figure:
    """Renders dual-axis monthly lead volume vs. conversion rate trend."""
    if len(monthly_df) == 0:
        return go.Figure()

    fig = go.Figure()

    # Bar chart for Total Leads
    fig.add_trace(go.Bar(
        x=monthly_df["creation_month"],
        y=monthly_df["total_leads"],
        name="Total Leads",
        marker_color="#CBD5E1",
        hoverinfo="x+y"
    ))

    # Bar chart for Converted Leads
    fig.add_trace(go.Bar(
        x=monthly_df["creation_month"],
        y=monthly_df["converted_leads"],
        name="Converted Leads",
        marker_color=COLOR_PRIMARY,
        hoverinfo="x+y"
    ))

    # Line chart for Conversion Rate % (Secondary Axis)
    fig.add_trace(go.Scatter(
        x=monthly_df["creation_month"],
        y=monthly_df["conversion_rate_pct"],
        name="Conversion Rate (%)",
        yaxis="y2",
        mode="lines+markers+text",
        text=[f"{val}%" for val in monthly_df["conversion_rate_pct"]],
        textposition="top center",
        line={"color": COLOR_SUCCESS, "width": 3},
        marker={"size": 7}
    ))

    fig.update_layout(
        title="<b>Monthly Pipeline Volume & Conversion Rate Trajectory</b>",
        barmode="group",
        yaxis={"title": "Number of Leads", "gridcolor": "#F1F5F9"},
        yaxis2={
            "title": "Conversion Rate (%)",
            "overlaying": "y",
            "side": "right",
            "range": [0, max(monthly_df["conversion_rate_pct"].max() * 1.3, 30)],
            "showgrid": False
        },
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "center", "x": 0.5},
        **CHART_THEME
    )
    return fig

def create_source_performance_chart(source_df: pd.DataFrame) -> go.Figure:
    """Renders ranked horizontal bar chart of lead sources by conversion efficiency."""
    if len(source_df) == 0:
        return go.Figure()

    sorted_df = source_df.sort_values(by="conversion_rate_pct", ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=sorted_df["source_name"],
        x=sorted_df["conversion_rate_pct"],
        orientation="h",
        text=[f"{val}% ({cnt} won)" for val, cnt in zip(sorted_df["conversion_rate_pct"], sorted_df["converted_leads"])],
        textposition="outside",
        marker={"color": sorted_df["conversion_rate_pct"], "colorscale": "Tealgrn", "showscale": False}
    ))

    fig.update_layout(
        title="<b>Lead Source Conversion Rate Ranking (%)</b>",
        xaxis={"title": "Conversion Rate (%)", "gridcolor": "#F1F5F9"},
        yaxis={"title": ""},
        **CHART_THEME
    )
    return fig

def create_campaign_roi_chart(campaign_df: pd.DataFrame) -> go.Figure:
    """Renders campaign expenditure vs. converted revenue bubble/bar comparison."""
    if len(campaign_df) == 0:
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=campaign_df["campaign_name"],
        y=campaign_df["budget_inr"],
        name="Budget Spend (₹)",
        marker_color="#94A3B8"
    ))

    fig.add_trace(go.Bar(
        x=campaign_df["campaign_name"],
        y=campaign_df["revenue_inr"],
        name="Generated Revenue (₹)",
        marker_color=COLOR_SUCCESS
    ))

    fig.update_layout(
        title="<b>Campaign Budget vs. Converted Revenue (INR ₹)</b>",
        barmode="group",
        yaxis={"title": "Amount (INR ₹)", "gridcolor": "#F1F5F9"},
        xaxis={"tickangle": -15},
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.3, "xanchor": "center", "x": 0.5},
        **CHART_THEME
    )
    return fig

def create_sales_rep_chart(rep_df: pd.DataFrame) -> go.Figure:
    """Renders sales rep revenue generation and closure velocity."""
    if len(rep_df) == 0:
        return go.Figure()

    fig = px.bar(
        rep_df,
        x="rep_name",
        y="revenue_inr",
        color="conversion_rate_pct",
        color_continuous_scale="Purples",
        text="revenue_inr",
        labels={"revenue_inr": "Total Revenue (₹)", "rep_name": "Sales Representative", "conversion_rate_pct": "Win Rate %"}
    )
    fig.update_traces(texttemplate="₹%{y:,.0f}", textposition="outside")
    fig.update_layout(
        title="<b>Sales Representative Revenue Realization & Win Rate (%)</b>",
        yaxis={"gridcolor": "#F1F5F9"},
        **CHART_THEME
    )
    return fig

def create_lead_score_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Renders split histogram of lead score distribution for converted vs lost leads."""
    if len(df) == 0:
        return go.Figure()

    df_plot = df.copy()
    df_plot["Outcome"] = df_plot["is_converted"].map({1: "Converted (Won)", 0: "Unconverted (Lost/Pipeline)"})

    fig = px.histogram(
        df_plot,
        x="lead_score",
        color="Outcome",
        barmode="overlay",
        nbins=25,
        opacity=0.75,
        color_discrete_map={"Converted (Won)": COLOR_SUCCESS, "Unconverted (Lost/Pipeline)": "#94A3B8"},
        labels={"lead_score": "Algorithmic Lead Score (1 - 100)"}
    )
    fig.update_layout(
        title="<b>Lead Score Distribution: Converted vs. Unconverted Prospects</b>",
        yaxis={"title": "Count of Leads", "gridcolor": "#F1F5F9"},
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.25, "xanchor": "center", "x": 0.5},
        **CHART_THEME
    )
    return fig

def create_time_to_convert_chart(df: pd.DataFrame) -> go.Figure:
    """Boxplot displaying conversion duration (days) across industries or sources."""
    conv_df = df[(df["is_converted"] == 1) & (df["conversion_time_days"].notnull())]
    if len(conv_df) == 0:
        return go.Figure()

    fig = px.box(
        conv_df,
        x="source_name",
        y="conversion_time_days",
        color="source_name",
        points="all",
        labels={"conversion_time_days": "Days from Creation to Conversion", "source_name": "Lead Source"}
    )
    fig.update_layout(
        title="<b>Sales Cycle Velocity: Days-to-Close by Acquisition Source</b>",
        showlegend=False,
        yaxis={"gridcolor": "#F1F5F9"},
        **CHART_THEME
    )
    return fig

def create_correlation_heatmap(corr_df: pd.DataFrame) -> go.Figure:
    """Annotated correlation matrix heatmap."""
    if len(corr_df) == 0:
        return go.Figure()

    fig = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1.0,
        zmax=1.0,
        labels={"color": "Correlation Coefficient"}
    )
    fig.update_layout(
        title="<b>Feature Correlation Matrix (Pearson r)</b>",
        **CHART_THEME
    )
    return fig
