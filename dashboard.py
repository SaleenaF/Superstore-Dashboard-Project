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

    html.Label("Select Year:"),

    dcc.Dropdown(
        options=[{'label': 'All Years', 'value': 'ALL'}] +
                [{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
        value='ALL',
        id='year_filter'
    ),

    dcc.Graph(id='bar_chart'),
    dcc.Graph(id='heatmap'),
    dcc.Graph(id='line_chart'),
    dcc.Graph(id='pie_chart'),
    dcc.Graph(id='map_chart'),
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
    # BAR CHART (FIXED - DATAFRAME METHOD)
    # ==============================

    sales_by_category = filtered_df.groupby('Category')['Sales'].sum().reset_index()

    barChart = px.bar(
        sales_by_category,
        x='Category',
        y='Sales',
        title='Sales by Category',
        text='Sales'
    )

    barChart.update_traces(textposition='outside')

    barChart.update_layout(
        xaxis_title='Category',
        yaxis_title='Sales'
    )

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
        title='Profit by Region and Category',
        labels=dict(x="Category", y="Region", color="Profit")
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

    category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()

    pieChart = px.pie(
        category_sales,
        names='Category',
        values='Sales',
        title='Sales Distribution by Category',
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    # ==============================
    # MAP
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
    # BOXPLOT (FIXED X-AXIS ISSUE)
    # ==============================

    boxPlot = px.box(
        filtered_df,
        x='Category',
        y='Sales',
        title='Sales Values'
    )

    boxPlot.update_layout(
        xaxis_title='Category',
        yaxis_title='Sales'
    )

    return barChart, heatMap, lineChart, pieChart, mapChart, boxPlot


# ==============================
# EXPORT STATIC HTML FOR GITHUB PAGES
# ==============================

def export_static_dashboard():

    filtered_df = df

    # BAR CHART
    sales_by_category = filtered_df.groupby('Category')['Sales'].sum().reset_index()

    barChart = px.bar(
        sales_by_category,
        x='Category',
        y='Sales',
        title='Sales by Category',
        text='Sales'
    )

    barChart.update_traces(textposition='outside')
    barChart.update_layout(xaxis_title='Category', yaxis_title='Sales')

    # HEATMAP
    heat = filtered_df.pivot_table(
        values='Profit',
        index='Region',
        columns='Category',
        aggfunc='sum'
    )

    heatMap = px.imshow(
        heat,
        text_auto=True,
        title='Profit by Region and Category',
        labels=dict(x="Category", y="Region", color="Profit")
    )

    # LINE CHART
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

    # PIE CHART
    category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()

    pieChart = px.pie(
        category_sales,
        names='Category',
        values='Sales',
        title='Sales Distribution by Category',
        color_discrete_sequence=px.colors.sequential.Plasma
    )

    # MAP
    state_sales = filtered_df.groupby('State/Province')['Sales'].sum().reset_index()

    mapChart = px.choropleth(
        state_sales,
        locations='State/Province',
        locationmode='USA-states',
        color='Sales',
        scope='usa',
        title='Sales by U.S. State'
    )

    # BOXPLOT
    boxPlot = px.box(
        filtered_df,
        x='Category',
        y='Sales',
        title='Sales Values'
    )

    boxPlot.update_layout(
        xaxis_title='Category',
        yaxis_title='Sales'
    )

    # EXPORT HTML
    html_content = f"""
    <html>
    <head><title>Superstore Dashboard</title></head>
    <body>
    {barChart.to_html(full_html=False, include_plotlyjs='cdn')}
    {heatMap.to_html(full_html=False, include_plotlyjs=False)}
    {lineChart.to_html(full_html=False, include_plotlyjs=False)}
    {pieChart.to_html(full_html=False, include_plotlyjs=False)}
    {mapChart.to_html(full_html=False, include_plotlyjs=False)}
    {boxPlot.to_html(full_html=False, include_plotlyjs=False)}
    </body>
    </html>
    """

    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("GitHub Pages dashboard saved to docs/index.html")


# ==============================
# RUN APP
# ==============================

if __name__ == '__main__':
    export_static_dashboard()
    app.run(debug=True)