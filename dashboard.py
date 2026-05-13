import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv("data/cleaned_superstore_data.csv")
df['Order Date'] = pd.to_datetime(df['Order Date'])

# ==============================
# APP
# ==============================

app = Dash(__name__)

# ==============================
# LAYOUT (VERTICAL POWER BI STYLE)
# ==============================

app.layout = html.Div(
    style={
        "fontFamily": "Verdana, sans-serif"
    },
    children=[

    # HEADER
    html.Div([
        html.H1("Superstore Sales Dashboard"),
        html.P("Analytics Report (Python + Plotly Dash)")
    ]),

    # FILTER
    dcc.Dropdown(
        options=[{'label': 'All Years', 'value': 'ALL'}] +
                [{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
        value='ALL',
        id='year_filter',
        clearable=False,
        style={"width": "300px"}
    ),

    # KPI ROW
    html.Div(id='kpi_row'),

    # CHARTS (VERTICAL STACK)
    dcc.Graph(id='bar_chart'),
    dcc.Graph(id='heatmap'),
    dcc.Graph(id='line_chart'),
    dcc.Graph(id='pie_chart'),
    dcc.Graph(id='map_chart'),
    dcc.Graph(id='box_plot'),

])


# ==============================
# CALLBACK
# ==============================

@app.callback(
    [
        Output('kpi_row', 'children'),
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

    # FILTER
    if selected_year == 'ALL':
        filtered_df = df
    else:
        filtered_df = df[df['Year'] == selected_year]

    # KPI METRICS
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = total_profit / total_sales if total_sales != 0 else 0

    # ==============================
    # KPI CARDS (PLASMA STYLE COLORS)
    # ==============================

    kpis = html.Div([

        html.Div([
            html.H3(f"${total_sales:,.0f}"),
            html.P("Total Sales")
        ], style={
            "background": "linear-gradient(135deg, #0d0887, #6a00a8)",
            "color": "white",
            "padding": "15px",
            "borderRadius": "12px",
            "textAlign": "center",
            "width": "30%",
            "boxShadow": "2px 2px 10px rgba(0,0,0,0.15)"
        }),

        html.Div([
            html.H3(f"${total_profit:,.0f}"),
            html.P("Total Profit")
        ], style={
            "background": "linear-gradient(135deg, #b12a90, #e16462)",
            "color": "white",
            "padding": "15px",
            "borderRadius": "12px",
            "textAlign": "center",
            "width": "30%",
            "boxShadow": "2px 2px 10px rgba(0,0,0,0.15)"
        }),

        html.Div([
            html.H3(f"{profit_margin:.2%}"),
            html.P("Profit Margin")
        ], style={
            "background": "linear-gradient(135deg, #f89441, #f0f921)",
            "color": "black",
            "padding": "15px",
            "borderRadius": "12px",
            "textAlign": "center",
            "width": "30%",
            "boxShadow": "2px 2px 10px rgba(0,0,0,0.15)"
        }),

    ], style={
        "display": "flex",
        "justifyContent": "space-between",
        "marginTop": "20px",
        "marginBottom": "20px"
    })

    # ==============================
    # BAR CHART
    # ==============================
    html.Div(id='font_debug', style={
        "marginTop": "10px",
        "fontFamily": "monospace",
        "whiteSpace": "pre-wrap",
        "background": "#f5f5f5",
        "padding": "10px",
        "borderRadius": "8px"
    })
    sales_by_category = filtered_df.groupby('Category')['Sales'].sum().reset_index()

    barChart = px.bar(
        sales_by_category,
        x='Category',
        y='Sales',
        title='Sales by Category',
        text='Sales'
    )
    
    barChart.update_traces(textposition='outside')
    barChart.update_layout(xaxis_title="Category", yaxis_title="Sales")

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

    pie_data = filtered_df.groupby('Category')['Sales'].sum().reset_index()

    pieChart = px.pie(
        pie_data,
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
    # BOXPLOT
    # ==============================

    boxPlot = px.box(
        filtered_df,
        x='Category',
        y='Sales',
        title='Sales Distribution'
    )

    return kpis, barChart, heatMap, lineChart, pieChart, mapChart, boxPlot


# ==============================
# RUN APP
# ==============================

if __name__ == '__main__':
    app.run(debug=True)