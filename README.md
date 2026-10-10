# ATM Finder Botswana 🇧🇼

An open-source, verified database and 3D interactive web application designed to help users locate ATMs across Botswana, filter by bank, town, or service, and view exact map directions or geolocated distance rankings.

---

## Repository Structure

```text
botswana-atm-finder/
├── README.md               # Project documentation & guidelines
├── index.html              # Frontend web application (3D Globe UI, search filters & geolocation)
├── data/
│   ├── botswana_atms.json  # Primary database of ATM records (source of truth)
│   ├── botswana_atms.csv   # Spreadsheet-friendly flat version of the database
│   └── bank_sources.csv    # Official bank registry and locator source URLs
└── scripts/
    └── validate_atms.py    # Python Quality Assurance script for JSON/CSV parity & schema
