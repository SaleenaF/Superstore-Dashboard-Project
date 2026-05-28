import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback_context

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("data/cleaned_superstore_data.csv")
df['Order Date'] = pd.to_datetime(df['Order Date'])

# ==============================
# APP Setup
# ==============================
app = Dash(__name__)

# ==============================
# LAYOUT (GRID / SINGLE SCREEN)
# ==============================
app.layout = html.Div(
    style={
        "fontFamily": "Verdana, sans-serif",
        "height": "100vh",
        "maxHeight": "100vh",
        "overflow": "hidden",
        "display": "flex",
        "flexDirection": "column",
        "backgroundColor": "#f8f9fa",
        "padding": "12px",
        "boxSizing": "border-box",
        "position": "relative"
    },
    children=[

        # ZOOM HINT INDICATOR
        html.Div(
            "🔎︎ Click anywhere on a chart container to zoom",
            style={
                "position": "absolute",
                "top": "15px",
                "right": "20px",
                "color": "#a0aec0",
                "fontSize": "11px",
                "fontStyle": "italic",
                "zIndex": "10"
            }
        ),

        # 1. TOP HEADER BAR
        html.Div([
            html.H2("Superstore Sales Dashboard", style={"margin": "0", "fontSize": "22px", "fontWeight": "bold", "color": "#2c3e50"}),
            html.P("Analytics Report (Python + Plotly Dash)", style={"margin": "0 0 0 15px", "color": "#7f8c8d", "fontSize": "13px", "alignSelf": "center"})
        ], style={"display": "flex", "borderBottom": "2px solid #e2e8f0", "paddingBottom": "5px", "marginBottom": "10px", "height": "5%"}),

        # 2. MAIN CONTENT AREA
        html.Div([
            
            # LEFT SIDEBAR: FILTERS & KPIs
            html.Div([
                html.Label("Select Year:", style={"fontWeight": "bold", "fontSize": "11px", "marginBottom": "4px"}),
                dcc.Dropdown(
                    options=[{'label': 'All Years', 'value': 'ALL'}] +
                            [{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
                    value='ALL',
                    id='year_filter',
                    clearable=False,
                    style={"marginBottom": "12px", "fontSize": "12px"}
                ),

                html.Label("Toggle Category:", style={"fontWeight": "bold", "fontSize": "11px", "marginBottom": "4px"}),
                dcc.Dropdown(
                    id='bar_toggle',
                    options=[
                        {'label': 'Category', 'value': 'Category'},
                        {'label': 'Sub-Category', 'value': 'Sub-Category'}
                    ],
                    value='Category',
                    clearable=False,
                    style={"marginBottom": "15px", "fontSize": "12px"}
                ),
                
                # KPI Container
                html.Div(id='kpi_row', style={"display": "flex", "flexDirection": "column", "gap": "10px", "height": "70%"})

            ], style={"width": "18%", "display": "flex", "flexDirection": "column", "paddingRight": "12px", "borderRight": "1px solid #e2e8f0"}),

            # RIGHT MAIN GRID
            html.Div([
                
                # ROW 1: 3 Charts
                html.Div([
                    html.Div(id='box_bar', n_clicks=0, children=[dcc.Graph(id='bar_chart', style={"height": "100%", "width": "100%"}, config={'displayModeBar': False, 'staticPlot': True})], style={"width": "33.3%", "height": "100%", "cursor": "pointer"}),
                    html.Div(id='box_heat', n_clicks=0, children=[dcc.Graph(id='heatmap', style={"height": "100%", "width": "100%"}, config={'displayModeBar': False, 'staticPlot': True})], style={"width": "33.3%", "height": "100%", "cursor": "pointer"}),
                    html.Div(id='box_line', n_clicks=0, children=[dcc.Graph(id='line_chart', style={"height": "100%", "width": "100%"}, config={'displayModeBar': False, 'staticPlot': True})], style={"width": "33.4%", "height": "100%", "cursor": "pointer"}),
                ], style={"display": "flex", "height": "49%", "gap": "8px"}),
                
                # ROW 2: 4 Charts Side-by-Side
                html.Div([
                    html.Div(id='box_pie', n_clicks=0, children=[dcc.Graph(id='pie_chart', style={"height": "100%", "width": "100%"}, config={'displayModeBar': False, 'staticPlot': True})], style={"width": "25%", "height": "100%", "cursor": "pointer"}),
                    html.Div(id='box_sun', n_clicks=0, children=[dcc.Graph(id='sunburst_chart', style={"height": "100%", "width": "100%"}, config={'displayModeBar': False, 'staticPlot': True})], style={"width": "25%", "height": "100%", "cursor": "pointer"}),
                    html.Div(id='box_map', n_clicks=0, children=[dcc.Graph(id='map_chart', style={"height": "100%", "width": "100%"}, config={'displayModeBar': False, 'staticPlot': True})], style={"width": "25%", "height": "100%", "cursor": "pointer"}),
                    html.Div(id='box_box', n_clicks=0, children=[dcc.Graph(id='box_plot', style={"height": "100%", "width": "100%"}, config={'displayModeBar': False, 'staticPlot': True})], style={"width": "25%", "height": "100%", "cursor": "pointer"})
                ], style={"display": "flex", "height": "49%", "gap": "8px", "marginTop": "8px"})

            ], style={"width": "82%", "display": "flex", "flexDirection": "column", "paddingLeft": "12px"}),

        ], style={"display": "flex", "height": "95%"}),

        # 3. INTERACTIVE ZOOM MODAL (With decoupled overlay close action button)
        html.Div(
            id="zoom_modal",
            style={
                "display": "none", 
                "position": "fixed", "top": "0", "left": "0", "width": "100%", "height": "100%",
                "backgroundColor": "rgba(0,0,0,0.7)", "zIndex": "1000", "justifyContent": "center", "alignItems": "center"
            },
            children=[
                html.Div([
                    # Pinned on its own floating overlay coordinate layer so it cannot push the layout box
                    html.Span("✕", id="close_modal", style={
                        "position": "absolute", "top": "15px", "right": "20px",
                        "fontSize": "24px", "color": "#7f8c8d", "cursor": "pointer",
                        "fontWeight": "bold", "zIndex": "1010"
                    }),
                    
                    # Graph layout container occupies 100% of the centered modal view frame area perfectly
                    html.Div([
                        dcc.Graph(id="modal_graph", style={"height": "100%", "width": "100%"})
                    ], style={
                        "height": "84vh", "width": "91vw", 
                        "display": "flex", "alignItems": "center", "justifyContent": "center"
                    })
                ], style={
                    "backgroundColor": "white", "borderRadius": "8px", "position": "relative",
                    "width": "95vw", "height": "92vh", "display": "flex", "alignItems": "center", "justifyContent": "center"
                })
            ]
        )
    ]
)

# ==============================
# MAIN CALLBACK
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

    if selected_year == 'ALL':
        filtered_df = df
    else:
        filtered_df = df[df['Year'] == int(selected_year)]

    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = total_profit / total_sales if total_sales != 0 else 0

    kpi_card_style = {
        "color": "white", "borderRadius": "8px", "boxShadow": "1px 1px 5px rgba(0,0,0,0.1)", "flex": "1",
        "display": "flex", "flexDirection": "column", "justifyContent": "center", "alignItems": "center"
    }

    kpis = [
        html.Div([
            html.H3(f"${total_sales:,.0f}", style={"margin": "0", "fontSize": "20px", "fontWeight": "bold"}),
            html.P("Total Sales", style={"margin": "4px 0 0 0", "fontSize": "11px", "opacity": "0.9"})
        ], style={**kpi_card_style, "background": "linear-gradient(135deg, #0d0887, #6a00a8)"}),

        html.Div([
            html.H3(f"${total_profit:,.0f}", style={"margin": "0", "fontSize": "20px", "fontWeight": "bold"}),
            html.P("Total Profit", style={"margin": "4px 0 0 0", "fontSize": "11px", "opacity": "0.9"})
        ], style={**kpi_card_style, "background": "linear-gradient(135deg, #b12a90, #e16462)"}),

        html.Div([
            html.H3(f"{profit_margin:.2%}", style={"margin": "0", "fontSize": "20px", "fontWeight": "bold"}),
            html.P("Profit Margin", style={"margin": "4px 0 0 0", "fontSize": "11px"})
        ], style={**kpi_card_style, "background": "linear-gradient(135deg, #f89441, #f0f921)", "color": "black"})
    ]

    def apply_screenshot_styling(fig, title_text):
        fig.update_layout(
            title={"text": title_text, "font": {"size": 11, "color": "#2c3e50"}},
            margin={"l": 30, "r": 15, "t": 35, "b": 30},
            font={"size": 9},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(240,242,245,0.5)'
        )
        return fig

    # 1. BAR CHART
    sales_data = filtered_df.groupby(selected_bar)['Sales'].sum().reset_index()
    barChart = px.bar(sales_data, x=selected_bar, y='Sales', text='Sales')
    barChart.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    barChart = apply_screenshot_styling(barChart, f'Sales by {selected_bar}')

    # 2. HEATMAP
    heat = filtered_df.pivot_table(values='Profit', index='Region', columns=selected_bar, aggfunc='sum', fill_value=0)
    heatMap = px.imshow(heat, text_auto='.2s', color_continuous_scale='Plasma')
    heatMap.update_layout(coloraxis_showscale=False)
    heatMap = apply_screenshot_styling(heatMap, f'Profit by Region & {selected_bar}')

    # 3. LINE CHART
    monthly_sales = filtered_df.groupby(pd.Grouper(key='Order Date', freq='ME'))['Sales'].sum().reset_index()
    lineChart = px.line(monthly_sales, x='Order Date', y='Sales', markers=True)
    lineChart = apply_screenshot_styling(lineChart, 'Monthly Sales Trend')

    # 4. PIE CHART
    pie_data = filtered_df.groupby(selected_bar)['Sales'].sum().reset_index()
    my_colors = ["#E56D5C", "#F0FA1F", "#636EFB", "#ffcc00", "#00c2ff", "#9b59b6", "#2ecc71"]
    pieChart = px.pie(pie_data, names=selected_bar, values='Sales', color_discrete_sequence=my_colors)
    pieChart.update_traces(showlegend=False, textinfo='percent+label')
    pieChart = apply_screenshot_styling(pieChart, 'Sales Distribution')

    # 5. SUNBURST CHART
    if 'Region' in filtered_df.columns:
        sunburst_data = filtered_df.groupby(['Region', selected_bar])['Sales'].sum().reset_index()
        sunburstChart = px.sunburst(sunburst_data, path=['Region', selected_bar], values='Sales', color='Sales', color_continuous_scale='Plasma')
    else:
        sunburstChart = px.sunburst(filtered_df, path=[selected_bar], values='Sales', color='Sales', color_continuous_scale='Plasma')
    sunburstChart.update_layout(coloraxis_showscale=False)
    sunburstChart = apply_screenshot_styling(sunburstChart, 'Sales Nesting Structure')

    # 6. MAP
    state_sales = filtered_df.groupby('State/Province')['Sales'].sum().reset_index()
    mapChart = px.choropleth(state_sales, locations='State/Province', locationmode='USA-states', color='Sales', scope='usa', color_continuous_scale='Plasma')
    mapChart.update_layout(coloraxis_showscale=False)
    mapChart.update_geos(bgcolor='rgba(0,0,0,0)', lakecolor='white')
    mapChart = apply_screenshot_styling(mapChart, 'Sales by U.S. State')

    # 7. BOXPLOT
    boxPlot = px.box(filtered_df, x=selected_bar, y='Sales')
    boxPlot = apply_screenshot_styling(boxPlot, 'Sales Range Distribution')

    return kpis, barChart, heatMap, lineChart, pieChart, sunburstChart, mapChart, boxPlot


# ==============================
# BOX CONTAINER MODAL CALLBACK
# ==============================
@app.callback(
    [
        Output("zoom_modal", "style"),
        Output("modal_graph", "figure")
    ],
    [
        Input("box_bar", "n_clicks"),
        Input("box_heat", "n_clicks"),
        Input("box_line", "n_clicks"),
        Input("box_pie", "n_clicks"),
        Input("box_sun", "n_clicks"),
        Input("box_map", "n_clicks"),
        Input("box_box", "n_clicks"),
        Input("close_modal", "n_clicks")
    ],
    [
        State("bar_chart", "figure"),
        State("heatmap", "figure"),
        State("line_chart", "figure"),
        State("pie_chart", "figure"),
        State("sunburst_chart", "figure"),
        State("map_chart", "figure"),
        State("box_plot", "figure")
    ],
    prevent_initial_call=True
)
def manage_zoom(n1, n2, n3, n4, n5, n6, n7, close_clicks, f1, f2, f3, f4, f5, f6, f7):
    ctx = callback_context
    if not ctx.triggered:
        return {"display": "none"}, {}
    
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "close_modal":
        return {"display": "none"}, {}
    
    fig_mapping = {
        "box_bar": f1, "box_heat": f2, "box_line": f3, 
        "box_pie": f4, "box_sun": f5, "box_map": f6, "box_box": f7
    }
    
    selected_fig = fig_mapping.get(trigger_id)
    if selected_fig:
        # Balanced margins ensure identical boundaries on all four sides of the modal grid box
        selected_fig['layout']['title']['font']['size'] = 18
        selected_fig['layout']['font']['size'] = 14
        selected_fig['layout']['margin'] = {"l": 50, "r": 50, "t": 50, "b": 50}
        
        if 'coloraxis' in selected_fig['layout']:
            selected_fig['layout']['coloraxis']['showscale'] = True 
            
        return {
            "display": "flex", 
            "position": "fixed", "top": "0", "left": "0", "width": "100%", "height": "100%", 
            "backgroundColor": "rgba(0,0,0,0.85)", "zIndex": "1000", 
            "justifyContent": "center", "alignItems": "center"
        }, selected_fig

    return {"display": "none"}, {}


if __name__ == '__main__':
    app.run(debug=True)