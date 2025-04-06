import logging
import os
import snowflake.connector
from snowflake.connector import SnowflakeConnection
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Snowflake connection parameters – replace these with your credentials.
SNOWFLAKE_USER = "REPORT_USER"
SNOWFLAKE_PASSWORD = "1234"
SNOWFLAKE_ACCOUNT = "BUTEFLJ-DH94720"
SNOWFLAKE_WAREHOUSE = "REPORT_WAREHOUSE"
SNOWFLAKE_DATABASE = "GOLDERN_LAYER"
SNOWFLAKE_SCHEMA = "PUBLIC"


# Define four pre-defined queries with associated report names.
QUERIES = {
    "1": "number_of_open_pending_items_by_product_id",
    "2": "open_orders_by_delivery_date_and_status",
    "3": "top_3_customers_with_pending_orders",
    "4": "top_3_delivery_dates_with_open_orders",
}


def get_user_selection() -> list[str] | None:
    """
    Display available reports and prompt user for selection.
    Returns a list of valid report keys.
    """
    while True:
        logging.info(
            "Please choose the report(s) you want to run by entering their numbers separated by commas:"
        )
        for key, report_name in QUERIES.items():
            logging.info(f"{key}. {report_name}")

        user_input = input(
            f"We have {len(QUERIES)} reports available:\n"
            "Enter report number(s) (e.g., 1,3): "
        )
        selected_numbers = [s.strip() for s in user_input.split(",") if s.strip()]

        if not selected_numbers:
            logging.error("No report number entered. Please try again.")
            continue

        invalid = [s for s in selected_numbers if s not in QUERIES]
        if invalid:
            logging.error(
                f"Invalid report number(s): {', '.join(invalid)}. Please enter valid report numbers."
            )
            continue

        return selected_numbers


def get_save_path() -> str:
    """
    Prompts the user to input a save path for CSV files.
    If no input is provided, defaults to the Desktop.
    Ensures the directory exists or creates it if necessary.
    Returns the final save path.
    """
    user_path = input(
        "Enter the full path where CSV files should be saved (press Enter to use the default Desktop): "
    ).strip()
    if not user_path:
        save_path = os.path.join(os.getenv("DESKTOP_PATH"))
    else:
        save_path = user_path

    # Check if the save_path exists; if not, try to create it.
    if not os.path.exists(save_path):
        logging.info(f"Directory {save_path} does not exist. Attempting to create it.")
        try:
            os.makedirs(save_path)
            logging.info(f"Created directory: {save_path}")
        except Exception as e:
            logging.error(f"Could not create directory {save_path}. Error: {str(e)}")
            exit(1)
    logging.info(f"CSV files will be saved to: {save_path}")
    return save_path


def read_sql_file(file_path: str) -> str:
    """
    Read a SQL file and return its content as a string.
    """
    try:
        with open(file_path, "r") as file:
            sql_query = file.read()
        return sql_query
    except FileNotFoundError:
        logging.error(f"SQL file not found: {file_path}")
        return ""
    except Exception as e:
        logging.error(f"Error reading SQL file: {file_path}\n{str(e)}")
        return ""


def run_query(connection: SnowflakeConnection, query: str) -> pd.DataFrame | None:
    """
    Execute a query using the provided Snowflake connection.
    Returns a Pandas DataFrame if successful.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            df = cursor.fetch_pandas_all()
        return df
    except Exception as e:
        logging.error(f"Error running query: {query}\n{str(e)}")
        return None


def export_to_csv(df: pd.DataFrame, path: str, filename: str) -> bool:
    """
    Export a DataFrame to a CSV file.
    Returns True if successful, False otherwise.
    """
    try:
        csv_filename = f"{path}/{filename}.csv"
        df.to_csv(csv_filename, index=False)
        logging.info(f"Exported DataFrame to {csv_filename}")
        return True
    except Exception as e:
        logging.error(f"Error exporting DataFrame to CSV: {filename}\n{str(e)}")
        return False


def main():
    # Connect to Snowflake
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
        )
        logging.info("Successfully connected to Snowflake.")
    except Exception as e:
        logging.error("Failed to connect to Snowflake.")
        logging.error(str(e))
        exit(1)

    # Get the user's report selections.
    selected_report_numbers = get_user_selection()
    save_path = get_save_path()

    error_reports = []  # Collect error messages
    # Execute each selected query and save the results.
    for report_number in selected_report_numbers:
        report_name = QUERIES[report_number]
        query = read_sql_file(f"sql/{report_name}.sql")
        if query is None:
            error_reports.append(f"Failed to read SQL file for {report_name}.")
            continue
        logging.info(f"Running {report_name} with query: {query}")
        df = run_query(conn, query)
        if df is None:
            error_reports.append(f"Query execution failed for {report_name}.")
            continue
        export_succeed = export_to_csv(df, save_path, report_name)
        if not export_succeed:
            error_reports.append(f"CSV export failed for {report_name}.")

    conn.close()
    logging.info("Snowflake connection closed. Exiting program.")

    # Print error summary if any errors occurred.
    if error_reports:
        logging.info("\nError Summary:")
        for error in error_reports:
            logging.info(error)
    else:
        logging.info(
            f"CSV export for all selected reports: {[QUERIES[report_number] for report_number in selected_report_numbers]}."
        )


if __name__ == "__main__":
    main()
