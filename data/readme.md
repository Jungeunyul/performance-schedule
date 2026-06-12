# 📂 data/ (Project Assets Directory)

This folder integrates and manages the core dataset, final presentation slides, and the speech script for the **'Korea Dance Performance Tracking Dashboard'** project.

---

## 📄 File Directory

| File Name | Format | Description & Role |
| :--- | :--- | :--- |
| **`data.csv`** | CSV Data | A structured dataset containing 40 major Korean dance performances used for dashboard visualization. |
| **`art and big data ppt.pptx`** | PPTX | The final presentation slides covering the project's background, design goals, and development process. |

---

## 📊 1. Dataset Overview (`data.csv`)
* **Data Scale:** Total of 40 large-scale dance performance repertoires.
* **Main Genres:** Ballet, Contemporary, and Traditional Korean Dance.
* **Collected Attributes:** Performance Name, Organization, Genre, Venue, Region, Price (KRW), Booking Rate (%), Start Date, End Date, and Booking Link.
* **Key Highlights:**
  - Includes real-time seasonal lineups from major national companies and venues (Seoul Arts Center, National Theater of Korea, etc.).
  - Structured carefully to support seamless runtime data transformation for the multilingual toggle feature.
  - Text-preprocessed venue names to connect automatically with the Kakao Map URL shared links.

---

## 🎤 2. Presentation & Script Guide (`art and big data ppt.pptx`)
* **Final Presentation Slides:** Summarizes the core achievements with a focus on the engineering development lifecycle: *Planning ➔ Structuring ➔ UX Implementation ➔ Deployment & Optimization*.
* **Speech Script (Embedded/Included):**
  - Emphasizes the artistic management perspective driven by a dance major.
  - Demonstrates technical troubleshooting and problem-solving through data-code decoupling.
  - Explains the execution of critical UX elements: the 4-tier intersection filter, bilingual layout toggle, and interactive location service (**📍 Map**).

---

## 🛠️ Data Integration & Maintenance
The `data.csv` file in this directory is dynamically linked to the main `app.py` script located in the root repository. Any future updates, additions, or deletions made directly inside this CSV file will be reflected automatically on the live Streamlit dashboard website.
