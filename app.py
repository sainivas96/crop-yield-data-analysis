import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Crop Yield Analytics", page_icon="🌾", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/crop_yield_data.csv")

df=load_data()

st.title("🌾 Crop Yield Data Analysis")
st.caption("Analytics dashboard for exploring agricultural and weather parameters that influence crop yield.")

with st.sidebar:
    st.header("Filters")
    crops=st.multiselect("Crop", sorted(df["Crop"].unique()), default=sorted(df["Crop"].unique()))
    regions=st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))

f=df[df["Crop"].isin(crops) & df["Region"].isin(regions)].copy()

c1,c2,c3,c4=st.columns(4)
c1.metric("Records", f"{len(f):,}")
c2.metric("Avg Yield", f"{f['Yield_t_ha'].mean():.2f} t/ha")
c3.metric("Avg Rainfall", f"{f['Rainfall_mm'].mean():.0f} mm")
c4.metric("Avg Temperature", f"{f['Temperature_C'].mean():.1f} °C")

st.divider()

left,right=st.columns(2)
with left:
    st.subheader("Average Yield by Crop")
    crop_avg=f.groupby("Crop",as_index=False)["Yield_t_ha"].mean().sort_values("Yield_t_ha",ascending=False)
    fig=px.bar(crop_avg,x="Crop",y="Yield_t_ha",text_auto=".2f",labels={"Yield_t_ha":"Yield (t/ha)"})
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.subheader("Rainfall vs Yield")
    fig=px.scatter(f,x="Rainfall_mm",y="Yield_t_ha",color="Crop",
                   hover_data=["Region","Temperature_C","Humidity_pct"],
                   labels={"Rainfall_mm":"Rainfall (mm)","Yield_t_ha":"Yield (t/ha)"})
    st.plotly_chart(fig,use_container_width=True)

left,right=st.columns(2)
with left:
    st.subheader("Yield by Region")
    reg=f.groupby("Region",as_index=False)["Yield_t_ha"].mean().sort_values("Yield_t_ha",ascending=False)
    fig=px.bar(reg,x="Region",y="Yield_t_ha",text_auto=".2f",labels={"Yield_t_ha":"Yield (t/ha)"})
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.subheader("Fertilizer vs Yield")
    fig=px.scatter(f,x="Fertilizer_kg_ha",y="Yield_t_ha",color="Crop",
                   labels={"Fertilizer_kg_ha":"Fertilizer (kg/ha)","Yield_t_ha":"Yield (t/ha)"})
    st.plotly_chart(fig,use_container_width=True)

st.subheader("Key Correlations with Yield")
corr=f.select_dtypes("number").corr()["Yield_t_ha"].drop("Yield_t_ha").sort_values()
st.dataframe(corr.rename("Correlation").to_frame().style.format("{:.3f}"),use_container_width=True)

st.subheader("Cleaned Dataset Preview")
st.dataframe(f.head(20),use_container_width=True)

st.download_button("Download CSV", f.to_csv(index=False), "crop_yield_filtered.csv", "text/csv")

st.info("Note: The included dataset is an illustrative portfolio dataset created for demonstrating data cleaning, exploratory analysis and visualization. Replace it with a verified public agricultural dataset if you want to publish research claims.")
