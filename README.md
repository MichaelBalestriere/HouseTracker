# Insider Trading Viewer

## Table of Contents
1. [Introduction and Overview](#introduction-and-overview)
2. [System Architecture](#system-architecture)
3. [Data Design](#data-design)
4. [Interface Design](#interface-design)
5. [Component Design](#component-design)
6. [User Interface Design](#user-interface-design)
7. [Assumptions and Dependencies](#assumptions-and-dependencies)
8. [Glossary of Terms](#glossary-of-terms)

---

## 1. Introduction and Overview

Insider Trading Viewer is a GUI-based Python application that allows users to retrieve and view recent insider trading transactions using the Financial Modeling Prep API. It enables users to input a specific date, fetch relevant insider trading data, view the details in a readable format, and export important transactions to a CSV file.

---

## 2. System Architecture

The system is a single-tier client-side application structured into the following layers:

- **GUI Layer (Presentation):** Built using `tkinter`, it provides input and output interfaces for the user.
- **Logic Layer:** Handles API communication, filters data based on user input, and calculates total transaction cost.
- **Data Layer:** Retrieves data via REST API and organizes it into dictionaries for display/export.
- **Export Layer:** Converts filtered results into a downloadable CSV file using Python’s built-in `csv` module.

There is no server, database, or background thread—this is a fully synchronous, event-driven local application.

---

## 3. Data Design

### External Data Source:
- **API Endpoint:** `https://financialmodelingprep.com/stable/insider-trading/latest`
- **Required Parameter:** `apikey` and `date`

### Important Fields:
| Field Name            | Description                                  |
|-----------------------|----------------------------------------------|
| `reportingName`       | Insider's name who reported the trade        |
| `transactionDate`     | The date of the transaction (YYYY-MM-DD)     |
| `transactionType`     | Type of transaction (e.g., P-Purchase)       |
| `securitiesTransacted`| Number of shares bought or sold              |
| `price`               | Price per share during the transaction       |
| `typeOfOwner`         | Insider's relationship to the company        |

### Derived Fields:
- **Total Cost =** `securitiesTransacted * price`, formatted to two decimal places.

Filtered data is stored in a list of dictionaries (`exportable_trades`) for viewing and exporting.

---

## 4. Interface Design

### API Interface:
- Uses `requests.get()` to call the Financial Modeling Prep API.
- API call includes date and API key in the query string.
- On success (`status_code == 200`), returns JSON with an array of insider trade dictionaries.
- Errors are caught and reported via pop-up alerts.

### File Interface:
- Uses `filedialog.asksaveasfilename()` to prompt for CSV export path.
- Uses `csv.DictWriter` to write field-matched data to CSV.

---

## 5. Component Design

| Function/Component    | Description |
|------------------------|-------------|
| `fetch_trades()`       | Main logic: retrieves API data, filters it, formats output, and populates export list |
| `export_to_csv()`      | Saves current filtered trade data to a user-specified CSV file |
| `date_entry`           | GUI input field for date (YYYY-MM-DD) |
| `output_text`          | Text widget that displays formatted trade info |
| `fetch_button`         | Triggers data fetch on click |
| `export_button`        | Triggers CSV export on click |
| Hover events           | Enhances interactivity by changing button color on hover |

Each function has a clear, single responsibility and is event-driven via user interaction.

---

## 6. User Interface Design

- **Window Size:** 800x600, resizable GUI with a modern flat design.
- **Title Label:** “Insider Trading Viewer” in large bold font.
- **Date Input Section:** Labeled entry box for selecting a date in `YYYY-MM-DD` format.
- **Buttons:**
  - `Fetch Trades`: Initiates API call and filters/outputs data.
  - `Export to CSV`: Allows exporting currently displayed trades.
- **Output Display:**
  - Scrollable `Text` widget using a monospaced font.
  - Outputs formatted data blocks for each valid trade.
- **Feedback Mechanisms:**
  - Messageboxes indicate success, failure, or no data returned.

UI uses consistent font and color schemes for readability and user experience.

---

## 7. Assumptions and Dependencies

### Assumptions:
- User will enter a valid date in the format `YYYY-MM-DD`.
- Internet connection is available during runtime.
- Financial Modeling Prep API is up and responsive.
- Only `P-Purchase` and `S-Sale` transactions are relevant for export.

### Dependencies:
- Python 3.12.2
- `requests` for API communication
- `tkinter` for GUI rendering (standard library)
- `csv` for writing exported data (standard library)
- A valid API key from Financial Modeling Prep

---

## 8. Glossary of Terms

| Term                  | Description                                  |
|-----------------------|----------------------------------------------|
| **API**               | Application Programming Interface; a set of protocols for building software applications. |
| **GUI**               | Graphical User Interface; a user interface that allows interaction through graphical icons and visual indicators. |
| **Insider Trading**   | The buying or selling of a company’s stock by someone who has non-public, material information about the company. |
| **CSV**               | Comma-Separated Values; a simple file format used for storing tabular data. |
| **P-Purchase**        | A type of insider trading transaction where an insider buys shares of the company. |
| **S-Sale**            | A type of insider trading transaction where an insider sells shares of the company. |

---


