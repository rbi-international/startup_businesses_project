# Startup Funding Analysis

## Overview
This project provides an interactive dashboard for analyzing startup funding trends using Streamlit. The application allows users to explore funding data based on various metrics such as total investment, investor activity, and startup-specific insights.

## Features
- **Overall Analysis**: View total investment trends, monthly investment movement, and key statistics.
- **Startup Insights**: Explore startup-specific investment data, including total funding and sector-wise distribution.
- **Investor Analysis**: Analyze investor activity, recent investments, and sector preferences.
- **Error Handling**: The application includes robust error handling to manage missing or inconsistent data gracefully.

## Installation
1. Clone the repository:
   ```bash
      git clone https://github.com/your-repo/startup-funding-analysis.git
      cd startup-funding-analysis
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
Dependencies
- Python 3.x
- Streamlit
- Pandas
- Matplotlib
- NumPy

Known Issues & Future Enhancements

- The dataset needs to be updated periodically for accurate insights.
- Additional visualizations and filters can be introduced.
- The UI can be improved for better user experience.
- Advanced analytics, such as predictive funding trends, can be implemented.

