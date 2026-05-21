import os
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

    # BAR / CATEGORY TOGGLE
    dcc.Dropdown(
        id='bar_toggle',
        options=[
            {'label': 'Category', 'value': 'Category'},
            {'label': 'Sub-Category', 'value': 'Sub-Category'}
        ],
        value='Category',
        clearable=False,
        style={"width": "300px", "marginTop": "10px"}
    ),

    # CHARTS (STACKED LAYOUT)
    dcc.Graph(id='bar_chart'),
    dcc.Graph(id='heatmap'),
    dcc.Graph(id='line_chart'),
    
    # SIDE-BY-SIDE CONTAINER FOR PIE AND SUNBURST
    html.Div([
        dcc.Graph(id='pie_chart', style={"width": "49%"}),
        dcc.Graph(id='sunburst_chart', style={"width": "49%"})
    ], style={"display": "flex", "justifyContent": "space-between", "marginTop": "10px", "marginBottom": "10px"}),
    
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
        Output('sunburst_chart', 'figure'),
        Output('map_chart', 'figure'),
        Output('box_plot', 'figure')
    ],
    [
        Input('year_filter', 'value'),
        Input('bar_toggle', 'value')
    ]
)
def update_dashboard(selected_year, selected_bar):

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

    sales_data = filtered_df.groupby(selected_bar)['Sales'].sum().reset_index()

    barChart = px.bar(
        sales_data,
        x=selected_bar,
        y='Sales',
        title=f'Sales by {selected_bar}',
        text='Sales'
    )

    barChart.update_traces(textposition='outside')

    barChart.update_layout(
        xaxis_title=selected_bar,
        yaxis_title="Sales"
    )

    # ==============================
    # HEATMAP
    # ==============================

    heat = filtered_df.pivot_table(
        values='Profit',
        index='Region',
        columns=selected_bar,
        aggfunc='sum'
    )

    heatMap = px.imshow(
        heat,
        text_auto=True,
        title=f'Profit by Region and {selected_bar}'
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
    # PIE CHART (ORIGINAL)
    # ==============================

    pie_data = filtered_df.groupby(selected_bar)['Sales'].sum().reset_index()

    my_colors = [
        "#efff43", "#495eff", "#e74c3c", "#ffcc00", "#00c2ff", 
        "#9b59b6", "#2ecc71", "#ff7f50", "#1abc9c", "#f39c12", 
        "#d63384", "#34495e", "#7f8c8d", "#8e44ad", "#27ae60", 
        "#c0392b", "#2980b9", "#16a085", "#f1c40f", "#e67e22"
    ]

    pieChart = px.pie(
        pie_data,
        names=selected_bar,
        values='Sales',
        title=f'Sales Distribution by {selected_bar}',
        color_discrete_sequence=my_colors
    )

    # ==============================
    # SUNBURST CHART (NEW)
    # ==============================

    if 'Region' in filtered_df.columns:
        sunburst_data = filtered_df.groupby(['Region', selected_bar])['Sales'].sum().reset_index()
        
        sunburstChart = px.sunburst(
            sunburst_data, 
            path=['Region', selected_bar], 
            values='Sales',
            title=f'Sales by Region and {selected_bar}',
            color='Sales',
            color_continuous_scale='Plasma'
        )
    else:
        sunburstChart = px.sunburst(
            filtered_df, 
            path=[selected_bar], 
            values='Sales',
            title=f'Sales by {selected_bar}',
            color='Sales',
            color_continuous_scale='Plasma'
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
        x=selected_bar,
        y='Sales',
        title=f'Sales Distribution by {selected_bar}'
    )

    return kpis, barChart, heatMap, lineChart, pieChart, sunburstChart, mapChart, boxPlot


# ==============================
# RUN APP & EXPORT
# ==============================

if __name__ == '__main__':
    # Ensure folder exists
    os.makedirs('docs', exist_ok=True)

    # 1. Get the figures (Ignoring KPIs with the _)
    _, *charts = update_dashboard('ALL', 'Category')

    # 2. One-liner to save everything to docs/index.html
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write("".join([c.to_html(full_html=False, include_plotlyjs='cdn') for c in charts]))

    print("Dashboard saved to docs/index.html")
    app.run(debug=True)