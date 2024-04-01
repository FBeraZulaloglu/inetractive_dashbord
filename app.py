# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  

# Function to upload dataset and return a Pandas DataFrame
def upload_dataset():
    uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)  # For CSV files
        except Exception as e:
            df = pd.read_excel(uploaded_file)  # For Excel files
        return df

# Function to generate chart based on user selection
def generate_chart(chart_type, selected_columns, dataset):
    st.subheader(f"{chart_type}")
    fig = None

    if chart_type == "Bar Chart":
        fig = px.bar(dataset, x=selected_columns[0], y=selected_columns[1])
    elif chart_type == "Line Chart":
        fig = px.line(dataset, x=selected_columns[0], y=selected_columns[1])
    elif chart_type == "Scatter Plot":
        fig = px.scatter(dataset, x=selected_columns[0], y=selected_columns[1])
    elif chart_type == "Pie Chart":
        fig = px.pie(dataset, names=selected_columns[0])
    elif chart_type == "Bubble Chart":
        fig = px.scatter(dataset, x=selected_columns[0], y=selected_columns[1], size=selected_columns[2])
    elif chart_type == "Dot Chart":
        fig = px.scatter(dataset, x=selected_columns[0], y=selected_columns[1])
    elif chart_type == "Horizontal Bar Chart":
        fig = px.bar(dataset, x=selected_columns[0], y=selected_columns[1], orientation='h')
    elif chart_type == "Sunburst Chart":
        if not selected_columns or None in selected_columns:
            st.warning("Please select a valid hierarchical column and a value column for the Sunburst Chart.")
            return
        fig = px.sunburst(dataset, path=selected_columns, values=selected_columns[1])  # Use the third column as values
    elif chart_type == "Sankey Diagram":
        if not selected_columns or None in selected_columns:
            st.warning("Please select source, target, and value columns for the Sankey Diagram.")
            return
        # Use selected_columns[0] and selected_columns[1] as source and target
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=list(set(dataset[selected_columns[0]].tolist() + dataset[selected_columns[1]].tolist()))
            ),
            link=dict(
                source=dataset[selected_columns[0]],
                target=dataset[selected_columns[1]],
                value=dataset[selected_columns[2]]
            )
        ))
    elif chart_type == "Table":
        if selected_columns[2] is not None:
            st.write(dataset[selected_columns])
        else:
            st.write(dataset[[selected_columns[0], selected_columns[1]]])  

    if fig is not None:
        st.plotly_chart(fig)

# Main Streamlit app
def main():
    # Page layout and styling
    st.set_page_config(
        page_title="KeenSight - Interactive Data Dashboard",
        page_icon=":chart_with_upwards_trend:",
    )

    st.image("logo_dark.png", width=350)
    # Title with styling
    st.title(":bar_chart: Interactive Data Dashboard")

    dataset = upload_dataset()

    if dataset is not None:

        st.subheader("**Step 1:** Choose Chart Types")
        chart_types = st.multiselect("Select Chart Types", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Bubble Chart", "Dot Chart", "Horizontal Bar Chart", "Sunburst Chart", "Sankey Diagram", "Table"])

        st.subheader("**Step 2:** Choose Columns")

        selected_columns_list = []

        for chart_type in chart_types:
            if chart_type == "Pie Chart":
                selected_columns = [st.selectbox("Select Column", dataset.columns, key=f"{chart_type}_column")]
            elif chart_type == "Sunburst Chart":
                selected_columns = [
                    st.selectbox("Select Hierarchical Column", dataset.columns, key=f"{chart_type}_hierarchical_column"),
                    st.selectbox("Select Values Column", dataset.columns, key=f"{chart_type}_values_column"),
                ]
            elif chart_type == "Sankey Diagram":
                selected_columns = [
                    st.selectbox("Select Source Column", dataset.columns, key=f"{chart_type}_source_column"),
                    st.selectbox("Select Target Column", dataset.columns, key=f"{chart_type}_target_column"),
                    st.selectbox("Select Value Column", dataset.columns, key=f"{chart_type}_sankey_value_column"),
                ]
            else:
                columns = dataset.columns
                x_column = st.selectbox(f"Select X-axis Column ({chart_type})", columns, key=f"{chart_type}_x_column")
                y_column = st.selectbox(f"Select Y-axis Column ({chart_type})", columns, key=f"{chart_type}_y_column")

                # Show the size column selector only for specific chart types
                if chart_type in ["Bubble Chart", "Dot Chart", "Scatter Plot"]:
                    size_column = st.selectbox(f"Select Size Column (optional) ({chart_type})", [None] + list(columns), key=f"{chart_type}_size_column")
                else:
                    size_column = None

                selected_columns = [x_column, y_column, size_column]

            selected_columns_list.append((chart_type, selected_columns))

        st.subheader("**Step 3:** Generate Dashboard")
        if st.button("Generate Dashboard"):
            for chart_type, selected_columns in selected_columns_list:
                generate_chart(chart_type, selected_columns, dataset)


# Run the app
if __name__ == "__main__":
    main()
