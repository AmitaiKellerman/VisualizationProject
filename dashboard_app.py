import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# # Constants
# EDUCATION_ORDER = ['Pre-primary education', 'Primary education', 'Lower secondary general education', 'Upper secondary general education']
#
#
# def load_data(file_path):
#     return pd.read_csv(file_path, index_col=0)
#
#
# def update_figure(df, country, qualification):
#     category_order = {
#         'Education level': EDUCATION_ORDER
#     }
#
#     # Filter data by country
#     filtered_df = df[(df['Country or Area'] == country) & (df['Qualification level'] == qualification)]
#
#     fig1 = px.line(filtered_df, x='Education level', y='Actual Salary per Hour', color='Experience Level', facet_col='Measure', category_orders=category_order)
#     fig1.update_layout(title='Actual Salary per Hour in Israel')
#
#     fig2 = px.histogram(df, x='Country or Area', y='Actual Salary per Hour', color='Experience Level', histfunc='avg', barmode='group', facet_row='Measure')
#     fig2.update_layout(title='International Comparison of Actual Salary per Hour', xaxis={'categoryorder':'total descending'})
#
#     return fig1, fig2
#
#
# def main():
#     st.title('Teacher Salary Analysis')
#     st.title('Inner look on Israel, and International comparison')
#
#     # Load data
#     teachers_salary_path = 'C:/Users/amita/PycharmProjects/VisualizationProject/merged_data.csv'
#     teachers_salary_df = load_data(teachers_salary_path)
#
#     # Visualize data
#     view_option = st.selectbox('Select View', teachers_salary_df['Country or Area'].unique())
#     qualification = st.radio('Select Qualification', teachers_salary_df['Qualification level'].unique())
#     country, international = update_figure(teachers_salary_df, view_option, qualification)
#     st.plotly_chart(country)
#     st.plotly_chart(international)
#
#
# if __name__ == "__main__":
#     main()


# Constants
EDUCATION_ORDER = ['Pre-primary education', 'Primary education', 'Lower secondary general education', 'Upper secondary general education']
EXPERIENCE_ORDER = ['No Experience', '10 years of Experience', '15 years of Experience', 'Maximum Experience']
MEASURE_ORDER = ['Statutory teaching time', 'Statutory working time required at school', 'Total statutory working time']


def load_data(file_path):
    return pd.read_csv(file_path, index_col=0)


def update_figure(df, country, qualification):
    # Filter data by country and qualification
    filtered_df = df[(df['Country or Area'] == country) & (df['Qualification level'] == qualification)]
    filtered_df['Education level'] = pd.Categorical(filtered_df['Education level'], categories=EDUCATION_ORDER, ordered=True)
    filtered_df['Experience Level'] = pd.Categorical(filtered_df['Experience Level'], categories=EXPERIENCE_ORDER, ordered=True)
    filtered_df = filtered_df.sort_values(by=['Education level', 'Experience Level'])

    # Plotting
    fig1 = px.line(filtered_df, x='Education level', y='Actual Salary per Hour', color='Experience Level',
                   facet_col='Measure', facet_col_spacing=0.1,
                   width=2000, height=400,
                   category_orders={'Education level': EDUCATION_ORDER, 'Measure': MEASURE_ORDER},
                   color_discrete_map={'No Experience': '#fdbe85',
                                       '10 years of Experience': '#fd8d3c',
                                       '15 years of Experience': '#e6550d',
                                       'Maximum Experience': '#a63603'})
    fig1.update_traces(line=dict(width=3.5))
    fig1.update_xaxes(tickmode='array', tickvals=np.arange(len(EDUCATION_ORDER)), ticktext=EDUCATION_ORDER,
                      ticks="outside", ticklen=10, tickwidth=1, tickcolor='gray', showticklabels=True)

    # Remove all x-axis titles
    n_facets = len(fig1.layout.annotations)
    for i in range(n_facets):
        axis_name = f'xaxis{i + 1}' if i > 0 else 'xaxis'
        fig1.layout[axis_name].title.text = None

    # Adding a centralized x-axis title using annotations
    fig1.add_annotation(
        x=0.5, y=-0.99,  # Adjust this value to lower the annotation just below the x-axis
        xref="paper", yref="paper",
        showarrow=False,
        text="Education level",
        font=dict(size=14),
        align="center"
    )

    fig1.update_layout(
        title=f'Actual Salary per Hour in {country}',
        legend=dict(yanchor='bottom', y=0.01, xanchor='right', x=1.18, traceorder='reversed', ),
        margin=dict(t=100, b=150)  # Adjust the bottom margin to ensure space for the annotation
    )

    for annotation in fig1.layout.annotations:
        annotation.text = annotation.text.replace('Measure=', '<b>Measure</b><br>')

    color_discrete_map = {
        'No Experience': '#fdd0a2',
        '10 years of Experience': '#fd8d3c',
        '15 years of Experience': '#d94801',
        'Maximum Experience': '#7f2704'
    }

    fig2 = px.histogram(df, x='Country or Area', y='Actual Salary per Hour', color='Experience Level',
                        histfunc='avg', barmode='group', facet_row='Measure')
    fig2.update_layout(title='International Comparison of Actual Salary per Hour',
                       xaxis={'categoryorder': 'total descending'})

    return fig1, fig2


def main():
    st.set_page_config(layout="wide", initial_sidebar_state='collapsed')
    st.title('Teacher Salary Analysis')
    st.header('Inner look on Israel, and International comparison')

    # Load data
    teachers_salary_path = 'merged_data.csv'
    teachers_salary_df = load_data(teachers_salary_path)

    countries_list = teachers_salary_df['Country or Area'].unique().tolist()
    israel_index = countries_list.index('Israel')

    # User Interface for selection
    view_option = st.sidebar.selectbox('Want to see inner look on other country but Israel? choose here:',
                                       countries_list,  # List of unique countries
                                       index=israel_index)  # Default selection is Israel
    filters = st.container(border=True)
    qualification = filters.radio('Select Qualification:', teachers_salary_df['Qualification level'].unique())

    country, international = update_figure(teachers_salary_df, view_option, qualification)
    st.plotly_chart(country, config={'displayModeBar': False})
    st.plotly_chart(international)


if __name__ == "__main__":
    main()
