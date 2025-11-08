import streamlit as st
from recommender import recommend

st.set_page_config(page_title="SHL Assessment Recommender", page_icon="🧠")
st.title("🧠 SHL Assessment Recommender")

query = st.text_area("Paste Job Description or Query", height=200)
top_k = st.slider("Number of Recommendations", 1, 10, 5)

if st.button("Recommend"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        recs = recommend(query, top_k=top_k)
        st.success(f"Top {top_k} Recommended Assessments:")
        for i, r in enumerate(recs, 1):
            st.markdown(f"**{i}. {r['assessment_name']}**  \n🔗 [Assessment Link]({r['url']})")
