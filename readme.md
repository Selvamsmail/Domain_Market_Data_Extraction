# Domain Market Data Extraction

This project automates the extraction of real estate data from Domain using Selenium, processes the data, and stores it in a MySQL database and Excel output.

---

## 📁 Project Structure

```bash
.
├── 1_domain_click.py          # Step 1: Extract property data
├── 2_domain_click.py          # Step 2: Extract property data
├── 3_domain_click.py          # Step 3: Extract property data
├── reset.py                   # Resets progress tracking and deletes previous outputs
├── runscripts.py              # Runs all 3 extractions in parallel
├── Domain_Mergefile.ipynb     # Merges and cleans data; pushes to MySQL; exports Excel
├── fix_cities.ipynb           # Optional cleaning of suburb/city names
├── Latitude_and_Longitude_Extract_20230802.xlsx  # External mapping for suburbs to lat/lon
├── sub_city_latandlon.xlsx    # Suburb-to-coordinate lookup
├── suburbs.xlsx               # Suburb input list
