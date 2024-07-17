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
EDUCATION_ORDER = ['Pre-primary education', 'Primary education', 'Lower secondary general education',
                   'Upper secondary general education']
EXPERIENCE_ORDER = ['No Experience', '10 years of Experience', '15 years of Experience', 'Maximum Experience']
MEASURE_ORDER = ['Statutory teaching time', 'Statutory working time required at school', 'Total statutory working time']
COLOR_DISCRETE_MAP = {
    'No Experience': '#fdd0a2',
    '10 years of Experience': '#fd8d3c',
    '15 years of Experience': '#d94801',
    'Maximum Experience': '#7f2704'
}


def load_data(file_path):
    return pd.read_csv(file_path, index_col=0)


def prepare_data_for_fig2(df):
    grouped_df = df.groupby(['Country or Area', 'Experience Level', 'Measure'], as_index=False)[
        'Actual Salary per Hour'].mean()
    grouped_df['avg_salary_per_measure'] = grouped_df.groupby(['Country or Area', 'Measure'])[
        'Actual Salary per Hour'].transform('mean')
    sorted_df = grouped_df.sort_values(by=['Measure', 'avg_salary_per_measure', 'Experience Level'],
                                       ascending=[True, False, True])
    return sorted_df


def update_figure(df, country, qualification):
    # Filter data by country and qualification
    filtered_df = df[(df['Country or Area'] == country) & (df['Qualification level'] == qualification)]
    filtered_df['Education level'] = pd.Categorical(filtered_df['Education level'], categories=EDUCATION_ORDER,
                                                    ordered=True)
    filtered_df['Experience Level'] = pd.Categorical(filtered_df['Experience Level'], categories=EXPERIENCE_ORDER,
                                                     ordered=True)
    filtered_df = filtered_df.sort_values(by=['Education level', 'Experience Level'])

    # fig 1
    fig1 = px.line(filtered_df, x='Education level', y='Actual Salary per Hour', color='Experience Level',
                   facet_col='Measure', facet_col_spacing=0.138,
                   width=2000, height=400,
                   category_orders={'Education level': EDUCATION_ORDER, 'Measure': MEASURE_ORDER},
                   color_discrete_map=COLOR_DISCRETE_MAP)
    fig1.update_traces(line=dict(width=3.5))

    # Modifying tick labels to be multi-line
    tickvals = np.arange(len(EDUCATION_ORDER))
    ticktext = [label.replace('education', '<br>education') for label in EDUCATION_ORDER]
    ticktext = [w.replace('general', '') for w in ticktext]

    fig1.update_xaxes(tickmode='array', tickvals=tickvals, ticktext=ticktext,
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

    for annotation in fig1.layout.annotations:
        annotation.text = annotation.text.replace('Measure=', '<b>Measure</b><br>')

    fig1.update_layout(
        title=f'Actual Salary per Hour in {country} (USD)',
        legend=dict(yanchor='bottom', y=-0.02, xanchor='right', x=1.2, traceorder='reversed', ),
        margin=dict(t=100, b=150)  # Adjust the bottom margin to ensure space for the annotation
    )

    # fig 2

    return fig1


def update_international_figure(df, measure):
    df = prepare_data_for_fig2(df)
    filtered_df = df[df['Measure'] == measure]
    # Plotting the histogram with facets - International Comparison
    fig = px.histogram(filtered_df, x='Country or Area', y='Actual Salary per Hour', color='Experience Level',
                       histfunc='avg', barmode='group',
                       category_orders={'Experience Level': EXPERIENCE_ORDER[::-1]},
                       height=600, width=1500,
                       color_discrete_map=COLOR_DISCRETE_MAP)  # Adjusted dimensions for vertical layout

    # Update layout and legend
    fig.update_layout(
        title='International Comparison of Actual Salary per Hour',
        xaxis=dict(title='Country or Area', tickangle=-45),
        legend=dict(
            title='Experience Level',
            orientation="h",
            x=0.5,  # Center position on the x-axis
            xanchor="center",  # Anchor point for centering
            y=-0.4,  # Position on the y-axis just below the plot
            yanchor="top"  # Anchor point at the top of the legend
        ),
        margin=dict(l=90, r=250, t=100, b=150)
    )

    # # Adjusting annotations for facet titles
    # for annotation in fig.layout.annotations:
    #     annotation.update(textangle=0)  # Set text angle to 0 (horizontal)
    #     annotation.font.size = 12
    #     annotation.text = annotation.text.replace('Measure=', '<b>Measure</b><br>')
    #     annotation.xref = 'paper'  # Reference the entire paper for positioning
    #     annotation.align = 'center'  # Center align the text
    #
    # fig.layout.annotations[0].x = 1.09  # Center the annotation horizontally
    # fig.layout.annotations[1].x = 1.04  # Center the annotation horizontally
    # fig.layout.annotations[2].x = 1.09  # Center the annotation horizontally

    # Clear all y-axis titles
    fig.update_yaxes(title_text='', showticklabels=True)

    # Add an annotation for the y-axis title in the middle of the plot
    fig.add_annotation(
        text='Actual Salary per Hour',  # Y-axis Title
        xref='paper', yref='paper',
        x=-0.1, y=0.5,  # Position the annotation in the middle of the plot
        showarrow=False,
        textangle=-90,  # Vertical text
        font=dict(size=12, color='gray')
    )

    # Customize tick labels to bold 'Israel'
    tickvals = df['Country or Area'].unique()
    ticktext = ['<b style="color:black; font-size:16px;">{}</b>'.format(country) if country == 'Israel' else country for
                country in tickvals]

    # Update x-axis tick labels
    fig.update_xaxes(tickmode='array', tickvals=tickvals, ticktext=ticktext)

    return fig


def main():
    st.set_page_config(layout="wide", initial_sidebar_state='collapsed')
    st.title('Teacher Salary Analysis')
    st.header('*Inner look on Israel, and International comparison*')

    # Load data
    teachers_salary_path = 'merged_data.csv'
    teachers_salary_df = load_data(teachers_salary_path)

    # Relevant Columns and indexes
    countries = teachers_salary_df['Country or Area'].unique().tolist()
    israel_index = countries.index('Israel')

    qualification_levels = teachers_salary_df['Qualification level'].unique().tolist()
    minimum_qualification_index = qualification_levels.index('Minimum qualification at this stage of career')

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.horizontal = True

    col1, col2 = st.columns(2)

    # User Interface - Choose Country
    with col1:
        st.write("**:orange-background[Want to see the Actual salary in other countries?]** :earth_americas:")
        country = st.selectbox('', countries, index=israel_index, label_visibility='collapsed')
        # st.markdown(f":orange[**{country}**] selected")

    # User Interface - Choose qualification Level
    with col2:
        st.write("**:orange-background[Which Qualification would you like to see?]** :mortar_board:")
        qualification = st.selectbox('', qualification_levels, minimum_qualification_index,
                                     label_visibility='collapsed')
        # st.markdown(f":orange[**{qualification}**] is selected")

    # Update and present the figure of the selected country
    country_fig = update_figure(teachers_salary_df, country, qualification)
    st.plotly_chart(country_fig)

    # Update and present the international comparison figure
    selected_measure = st.radio('Choose Measure to view comparison:', MEASURE_ORDER, index=0)
    international_fig = update_international_figure(teachers_salary_df, selected_measure)
    st.plotly_chart(international_fig)


if __name__ == "__main__":
    main()
