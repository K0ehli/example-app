# Reliability Analysis Tool

This is a Streamlit-based web application designed to perform reliability analysis on failure data. It utilizes the `reliability` Python library to fit various statistical distributions to your data and identify the best fit.

## Features

-   **Data Input**:
    -   **CSV Upload**: Upload a CSV file containing your failure data.
    -   **Manual Input**: Enter failure data values directly into an interactive table.
-   **Distribution Analysis**:
    -   Fits multiple probability distributions to the data using `Fit_Everything`.
    -   Identifies the best-fitting distribution based on goodness-of-fit metrics.
-   **Visualizations**:
    -   Interactive plots generated using `matplotlib`.
    -   **Detailed Plots**: specific histograms, probability plots (for all distributions), and P-P plots.
    -   **Best Distribution**: A dedicated view for the probability plot of the best-fitting distribution.
-   **Results**:
    -   Displays a table of goodness-of-fit results for detail comparison.

## How to Get Running

This project uses [`uv`](https://docs.astral.sh/uv/) for dependency management.

### Prerequisites

Ensure you have `uv` installed. If not, follow the instructions in the [official documentation](https://docs.astral.sh/uv/getting-started/installation/).

### Installation

1.  Clone this repository (if applicable) or navigate to the project directory.
2.  Install the dependencies using `uv`:

    ```bash
    uv sync
    ```

### Running the App

To start the Streamlit application, run the following command:

```bash
uv run streamlit run main.py
```

This will launch the app in your default web browser (typically at `http://localhost:8501`).
