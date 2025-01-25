import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

st.set_page_config(layout="wide",
                   page_title="Cairo count",
                   menu_items={
                       'Report a bug': "https://github.com/jonathanbouchet",
                       'Get help':"https://github.com/jonathanbouchet",
                       'About': "cairo count"
    })

st.title("CAIRO count DEV")

# st.sidebar.image("cover.png", use_container_width=True)
with st.sidebar:
  st.image("cover.png", width=200, use_container_width=True)
st.sidebar.divider()
st.sidebar.markdown("Antique Hunter's Guide *CAIRO* count")
st.sidebar.divider()
st.sidebar.markdown("x axis: number of pages of the chapter")
st.sidebar.markdown("y axis: number of occurances of the *CAIRO* word")

@st.cache_data
def make_random_data():
    x = np.random.randn(1000)
    y = np.random.randn(1000)
    return pd.DataFrame.from_dict({"x": x, "y": y})

@st.cache_data
def read_data():
    data = pd.read_csv("data.csv", sep=",")
    data["chapter_id"] = data.index
    # data["count"] = len(data) * [1]
    return data

if "data" not in st.session_state:
    st.session_state.data = read_data()

if "random_data" not in st.session_state:
    st.session_state.random_data = make_random_data()

col1, col2 = st.columns([0.4, 0.6])
with col1:
    st.dataframe(st.session_state.data)

with col2:
    if st.session_state.random_data is not None:
        df = st.session_state.data

        fig = px.scatter(df, 
                         x="num_pages", 
                         y="num_cairo", 
                        #  size="count",
                         hover_data=["num_pages", "num_cairo", "chapter_id"],
                         marginal_x="histogram", 
                         marginal_y="histogram", 
                         range_x=[-0.5,10.5], 
                         range_y=[-0.5,10.5])#, marginal_nbinsx=10, marginal_nbinsy=10)
        fig.update_layout(
            title="Number of pages v. Cairo occurances",
            xaxis_title="number of pages",
            yaxis_title="number of Cairo")
        st.plotly_chart(fig, use_container_width=True, key="scatter_plot", on_select="rerun")

        df2 = st.session_state.data[["chapter_id", "num_pages"]]
        df3 = st.session_state.data[["chapter_id", "num_cairo"]]

        trace1 = go.Scatter(x=df2["chapter_id"], y=df2["num_pages"], mode='lines', name='number of pages', line=dict(color='blue'))
        trace2 = go.Scatter(x=df3["chapter_id"], y=df3["num_cairo"], mode='lines', name='number of Cairo', line=dict(color='red'))

        data = [trace1, trace2]

        layout = go.Layout(title='Number of pages and Cairo occurances per chapter',
                        xaxis=dict(title='chapter #'),
                        yaxis=dict(title='Count'),
                        hovermode='closest')
        
        fig = go.Figure(data=data, layout=layout)
        st.plotly_chart(fig, use_container_width=True, key="line_plot", on_select="rerun")


        # fig = px.line(df2, 
        #                  x="chapter_id", 
        #                  y="num_pages", 
        #                  hover_data=["num_pages", "chapter_id"], markers=True)
        # fig.add_scatter(x=df3['chapter_id'], y=df3['num_cairo'], mode='lines', name='# of Cairo', line=dict(color='#4CC005'))
        # st.plotly_chart(fig, use_container_width=True, key="line_plot", on_select="rerun")