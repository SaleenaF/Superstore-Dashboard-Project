import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ==============================
# LOAD CLEANED DATA
# ==============================

df = pd.read_csv("data/cleaned_superstore_data.csv")

df['Order Date'] = pd.to_datetime(df['Order Date'])

# ==============================
# CREATE DASH APP
# ==============================

app = Dash(__name__)

# ==============================
# LAYOUT
# ==============================

app.layout = html.Div([

    html.H1("Superstore Sales Dashboard"),

    # FILTER
    html.Label("Select Year:"),

    dcc.Dropdown(
        options=[{'label': 'All Years', 'value': 'ALL'}] +
                [{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
        value='ALL',
        id='year_filter'
    ),

    # BAR CHART
    dcc.Graph(id='bar_chart'),

    # HEATMAP
    dcc.Graph(id='heatmap'),

    # LINE CHART
    dcc.Graph(id='line_chart'),

    # PIE CHART
    dcc.Graph(id='pie_chart'),

    # MAP
    dcc.Graph(id='map_chart'),

    # BOXPLOT
    dcc.Graph(id='box_plot')

])

# ==============================
# CALLBACK
# ==============================

@app.callback(
    [
        Output('bar_chart', 'figure'),
        Output('heatmap', 'figure'),
        Output('line_chart', 'figure'),
        Output('pie_chart', 'figure'),
        Output('map_chart', 'figure'),
        Output('box_plot', 'figure')
    ],
    [Input('year_filter', 'value')]
)

def update_dashboard(selected_year):

    if selected_year == 'ALL':
        filtered_df = df
    else:
        filtered_df = df[df['Year'] == selected_year]

    # ==============================
    # BAR CHART
    # ==============================

    sales_by_category = filtered_df.groupby('Category')['Sales'].sum()

    categories = sales_by_category.index.tolist()
    sales = sales_by_category.values.tolist()

    barChart = px.bar(
        x=categories,
        y=sales,
        labels={'x': 'Category', 'y': 'Sales'},
        title='Sales by Category',
        text=sales
    )

    barChart.update_traces(textposition='outside')

    # ==============================
    # HEATMAP
    # ==============================

    heat = filtered_df.pivot_table(
        values='Profit',
        index='Region',
        columns='Category',
        aggfunc='sum'
    )

    heatMap = px.imshow(
        heat,
        text_auto=True,
        title='Profit by Region and Category'
    )

    # ==============================
    # LINE CHART
    # ==============================

    monthly_sales = filtered_df.groupby(
        pd.Grouper(key='Order Date', freq='ME')
    )['Sales'].sum().reset_index()

    lineChart = px.line(
        monthly_sales,
        x='Order Date',
        y='Sales',
        markers=True,
        title='Monthly Sales Trend'
    )

    # ==============================
    # PIE CHART
    # ==============================

    pieChart = px.pie(
        names=categories,
        values=sales,
        title='Sales Distribution by Category',
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    # ==============================
    # SALES BY STATE MAP
    # ==============================

    state_sales = filtered_df.groupby('State/Province')['Sales'].sum().reset_index()

    mapChart = px.choropleth(
        state_sales,
        locations='State/Province',
        locationmode='USA-states',
        color='Sales',
        scope='usa',
        title='Sales by U.S. State'
    )

    # ==============================
    # BOXPLOT
    # ==============================

    boxPlot = px.box(
        filtered_df,
        y='Sales',
        title='Sales Values'
    )

    return (
        barChart,
        heatMap,
        lineChart,
        pieChart,
        mapChart,
        boxPlot
    )

# ==============================
# RUN DASHBOARD
# ==============================

if __name__ == '__main__':
    app.run(debug=True)