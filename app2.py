import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns


web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions", "Correlation Analysis"))

st.sidebar.write(web_apps)

if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")

    if show_df:
      st.write(df)
    
    # displaying relevant statistics about dataset
    st.header('Simple Statistics')
    col1, col2, col3 = st.columns(3) 
    col4, col5, = st.columns(2)
    col1.metric("Number of Rows", df.shape[0])
    col2.metric("Number of Columns", df.shape[1])
    col3.metric("Number of Categorical Variables", len(df.select_dtypes(include = 'object').columns))
    col4.metric("Number of Numerical Variables", len(df.select_dtypes(include = ['int', 'float']).columns))
    col5.metric("Number of Boolean Variables", len(df.select_dtypes(include = bool).columns))
    
    df.dropna(inplace = True) # removing "none" from dataframe
    
    # displaying a selected column
    number = st.sidebar.number_input('Select the index of which column you would like to view', min_value = 1, max_value = df.shape[1], step = 1)
    selected_column = df.iloc[:, number - 1]
    st.sidebar.write(selected_column)
    
    # when the selected column is numerical
    if selected_column.dtype in [int, float]: 
      minimum = np.min(selected_column)
      first_quart = np.percentile(selected_column, 25)
      median = np.median(selected_column)
      third_quart = np.percentile(selected_column, 75)
      maximum = np.max(selected_column)
      st.header('Five Number Summary')
      stat1, stat2, stat3, stat4, stat5 = st.columns(5)
      stat1.metric("Minimum:", minimum)
      stat2.metric("First Quartile:", first_quart)
      stat3.metric("Median:", median)
      stat4.metric("Third Quartile:", third_quart)
      stat5.metric("Maximum", maximum)
      
      
      # histogram
      choose_color = st.color_picker('Pick a Color', "#225692")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value = 1.0)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      column_titles = df.columns.tolist()
      hist_xtitle = st.text_input('Set x-axis Title', column_titles[number - 1])

      fig, ax = plt.subplots()
      ax.hist(selected_column, bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "numerical_plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("numerical_plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="numerical_plot.png",
            mime="image/png"
        )
    
    
    # when the selected column is categorical
    # proportions of each category level and customized barplot    
    if selected_column.dtype in ['category', 'object', 'string']:
      choose_color = st.color_picker('Pick a Color', "#225692")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value = 1.0)
      cat_hist_bins = selected_column.nunique() # number of variables
      cat_hist_title = st.text_input('Set Title', 'Histogram')
      column_titles = df.columns.tolist()
      cat_hist_xtitle = st.text_input('Set x-axis Title', column_titles[number - 1])
      fig2, ax2 = plt.subplots()
      ax2.hist(selected_column, bins = cat_hist_bins,
               edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax2.set_title(cat_hist_title)
      ax2.set_xlabel(cat_hist_xtitle)
      ax2.set_ylabel('Count')
      
      st.pyplot(fig2)
      filename = 'categorical_plot.png'
      fig2.savefig(filename, dpi = 300)
      
      # Display the download button
      with open("categorical_plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="categorical_plot.png",
            mime="image/png"
        )