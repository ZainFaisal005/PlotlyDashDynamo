import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px

# Load Dataset
data = pd.read_csv('ds_salaries.csv')

# Initialize Dash App with a modern Bootstrap theme
app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])
app.title = "Data Science Jobs Analysis Dashboard"

# Graph Generators
def generate_barplot(data):
    fig = px.bar(data, x="experience_level", y="salary_in_usd", color="experience_level",
                title="Salary Distribution by Experience Level", color_discrete_sequence=px.colors.qualitative.Set2)
    return fig

def generate_histogram(data):
    fig = px.histogram(data, x="job_title", y="salary_in_usd", color="job_title",
                    title="Histogram of Salary by Job Title", color_discrete_sequence=px.colors.qualitative.Pastel)
    return fig

def generate_pie_chart(data):
    fig = px.pie(data, names="remote_ratio", title="Remote Ratio Distribution",
                color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

def generate_line_chart(data):
    yearly_avg = data.groupby("work_year")["salary_in_usd"].mean().reset_index()
    fig = px.line(yearly_avg, x="work_year", y="salary_in_usd", title="Average Salary Over Years",
                markers=True, color_discrete_sequence=["#F4D03F"])
    return fig

def generate_parallel_coordinates(data):
    sampled_data = data.sample(50)  # Reduce size for readability
    fig = px.parallel_coordinates(
        sampled_data,
        dimensions=["salary_in_usd", "remote_ratio", "work_year"],
        color="salary_in_usd",
        color_continuous_scale=px.colors.sequential.Inferno,
        title="Parallel Coordinates for Salary and Features"
    )
    return fig

def generate_heatmap(data):
    pivot_table = data.pivot_table(index="experience_level", columns="company_size", values="salary_in_usd", aggfunc="mean")
    fig = px.imshow(pivot_table, text_auto=True, title="Average Salary Heatmap",
                    color_continuous_scale="Blues")
    return fig

def generate_scatter_plot(data):
    fig = px.scatter(data, x="remote_ratio", y="salary_in_usd", color="job_title",
                    size="salary_in_usd", title="Scatter Plot: Remote Ratio vs Salary",
                    color_discrete_sequence=px.colors.qualitative.T10)
    return fig

def generate_salary_histogram(data):
    fig = px.histogram(data, x="salary_in_usd", nbins=20, color="experience_level",
                    title="Histogram of Salaries", color_discrete_sequence=px.colors.sequential.Viridis)
    return fig

# Layout with Navbar, Cards, and Footer
app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="Data Science Jobs Analysis Dashboard",
        color="primary",
        dark=True,
        className="mb-4"
    ),
    dbc.Row(
        dbc.Col(dbc.Card([
            dbc.CardHeader("Salary Distribution by Experience Level"),
            dbc.CardBody(dcc.Graph(figure=generate_barplot(data)))
        ], className="mb-4"))
    ),
    dbc.Row(
        dbc.Col(dbc.Card([
            dbc.CardHeader("Histogram of Salary by Job Title"),
            dbc.CardBody(dcc.Graph(figure=generate_histogram(data)))
        ], className="mb-4"))
    ),
    dbc.Row(
        dbc.Col(dbc.Card([
            dbc.CardHeader("Remote Ratio Distribution"),
            dbc.CardBody(dcc.Graph(figure=generate_pie_chart(data)))
        ], className="mb-4"))
    ),
    dbc.Row(
        dbc.Col(dbc.Card([
            dbc.CardHeader("Average Salary Over Years"),
            dbc.CardBody(dcc.Graph(figure=generate_line_chart(data)))
        ], className="mb-4"))
    ),
    dbc.Row(
        dbc.Col(dbc.Card([
            dbc.CardHeader("Parallel Coordinates for Salary and Features"),
            dbc.CardBody(dcc.Graph(figure=generate_parallel_coordinates(data)))
        ], className="mb-4"))
    ),
    dbc.Row(
        dbc.Col(dbc.Card([
            dbc.CardHeader("Average Salary Heatmap"),
            dbc.CardBody(dcc.Graph(figure=generate_heatmap(data)))
        ], className="mb-4"))
    ),
    dbc.Row(
        dbc.Col(dbc.Card([
            dbc.CardHeader("Scatter Plot: Remote Ratio vs Salary"),
            dbc.CardBody(dcc.Graph(figure=generate_scatter_plot(data)))
        ], className="mb-4"))
    ),
    dbc.Row(
        dbc.Col(dbc.Card([
            dbc.CardHeader("Histogram of Salaries"),
            dbc.CardBody(dcc.Graph(figure=generate_salary_histogram(data)))
        ], className="mb-4"))
    ),
    html.Footer(
        dbc.Container(
            html.P("Data Science Jobs Analysis Dashboard © 2024", className="text-center text-light"),
            fluid=True,
            className="bg-primary py-3 mt-4"
        )
    )
], fluid=True)

# Run the App
if __name__ == "__main__":
    app.run_server(debug=True)
