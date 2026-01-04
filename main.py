import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import reliability.Distributions as Distributions
from reliability.Fitters import Fit_Everything
import traceback

df_manual = pd.DataFrame(
    [
        {"failure": 12.5},
        {"failure": 15.2},
        {"failure": 18.9},
        {"failure": 22.1},
    ]
)

st.set_page_config(page_title="Reliability Analysis Tool", layout="wide")

def main():
    st.title("Reliability Analysis Tool")
    st.markdown("### Select an Analysis Module")

    input_type = st.radio(
    "Select Input Type",
    ["CSV File", "Manual Input"],
    index=None,
    )

    st.write("You selected:", input_type)

    if input_type == "CSV File":
        uploaded_file = st.file_uploader("Upload a CSV", type="csv")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("First 5 rows of the uploaded data:")
            st.dataframe(df.head())
            run_file_analysis(df)
        else:
            st.info("Please upload a CSV file.")

    if input_type == "Manual Input":
        edited_df = st.data_editor(df_manual, num_rows="dynamic")
        run_file_analysis(edited_df)


def run_file_analysis(uploaded_file):
    if uploaded_file is not None:
        try:
            columns = uploaded_file.columns.tolist()
            selected_column = st.selectbox("Select the data column", columns)
            
            # --- Analysis Section ---
            st.subheader("Distribution Analysis")
            
            if st.button("Run Fit Everything Analysis", type="primary"):
                data = uploaded_file[selected_column].dropna()
                # Ensure data is numeric
                data = pd.to_numeric(data, errors='coerce').dropna()
                
                if len(data) == 0:
                    st.error("The selected column does not contain valid numeric data.")
                else:
                    failures = data.values
                    st.info("Running Fit Everything... finding the best distribution for your data.")
                    fit_output = Fit_Everything(
                            failures=failures,
                            show_probability_plot=False, 
                            show_PP_plot=False, 
                            show_histogram_plot=False, 
                            show_best_distribution_probability_plot=False,
                            print_results=False
                        )
                    st.session_state['fit_results'] = fit_output

            if 'fit_results' in st.session_state:
                fit_output = st.session_state['fit_results']
                st.success(f"Best fitting distribution: **{fit_output.best_distribution_name}**")
                    
                # Tabs for results
                tab_results, tab_best_dist = st.tabs(["Detailed Plots & Results", "Best Distribution Plot"])
                    
                with tab_results:
                    st.write("Goodness of fit results:")
                    st.dataframe(fit_output.results)
                        
                    st.subheader("Plots")
                        
                    # Histogram
                    try:
                        fig_hist = fit_output._Fit_Everything__histogram_plot()
                        st.write("**Histogram Plot**")
                        st.pyplot(fig_hist)
                        plt.close(fig_hist)
                    except Exception:
                        st.warning(f"Could not generate Histogram: {traceback.format_exc()}")

                    # Probability Plot (All)
                    try:
                        fig_prob = fit_output._Fit_Everything__probability_plot()
                        st.write("**Probability Plot (All Distributions)**")
                        st.pyplot(fig_prob)
                        plt.close(fig_prob)
                    except Exception:
                        st.warning(f"Could not generate Probability Plot: {traceback.format_exc()}")

                    # PP Plot
                    try:
                        fig_pp = fit_output._Fit_Everything__P_P_plot()
                        st.write("**P-P Plot**")
                        st.pyplot(fig_pp)
                        plt.close(fig_pp)
                    except Exception:
                        st.warning(f"Could not generate P-P Plot: {traceback.format_exc()}")

                with tab_best_dist:
                    try:
                        fig_best = fit_output._Fit_Everything__probability_plot(best_only=True)
                        st.write(f"**Best Distribution: {fit_output.best_distribution_name}**")
                        st.pyplot(fig_best)
                        plt.close(fig_best)
                    except Exception:
                        st.warning(f"Could not generate Best Distribution Plot: {traceback.format_exc()}")


        except Exception as e:
            st.error(f"Error reading CSV file or file not found: {e}")
    else:
        st.info("Please upload a CSV file to begin analysis.")



if __name__ == "__main__":
    main()
