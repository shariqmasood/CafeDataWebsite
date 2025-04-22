# Cafe & Wifi

A Flask‑based web application for cataloging laptop‑friendly cafés around the world. Users can browse a directory of cafés with Wi‑Fi, seating, and other amenities, add new entries via a simple form, and remove cafés when they close.

---

## Features

- **List Cafés**  
  Browse all cafés in your database, sorted alphabetically.

- **Add Café**  
  Submit a form with name, location, image, map link, seating, price, and amenity checkboxes.

- **Delete Café**  
  Remove cafés you no longer want to show with a single click.

- **REST API**  
  - `GET /random`   Returns one random café in JSON  
  - `GET /all`      Returns all cafés in JSON  
  - `GET /search`  Query by location (`?loc=…`)  
  - `POST /add`    Create a new café via form data  
  - `PATCH /update-price/<id>` Update coffee price  
  - `DELETE /report-closed/<id>?api-key=KEY` Delete by ID

---

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/CafeDataWebsite.git
   cd CafeDataWebsite

2. **Create a virtual environment**

python3 -m venv venv
source venv/bin/activate    # macOS/Linux
.\venv\Scripts\activate     # Windows PowerShell

3. **Install dependencies**
   pip install -r requirements.txt

5. **Prepare the database**
   If you have a pre‑populated cafes.db, place it next to app.py.
   Otherwise, let Flask‑SQLAlchemy create it automatically on first run:
   flask run
   
6. **Usage**
Start the server

bash
Copy
Edit
flask run
Open your browser and go to http://127.0.0.1:5000/.

Navigate

Home page: hero banner with “Browse Cafés” & “Add a Café” buttons

/cafes: view all cafés in a Bootstrap‑styled card grid

/add-cafe: fill out the form to add a new café

Delete any café by clicking the red Delete button on its card.

Project Structure
bash
Copy
Edit
CafeDataWebsite/
├─ app.py                # Main Flask application
├─ cafes.db              # SQLite database (auto‑created or provided)
├─ requirements.txt      # Python package list
├─ /templates            # Jinja2 HTML templates
│    ├─ base.html
│    ├─ index.html
│    ├─ cafes.html
│    └─ add_cafe.html
└─ /static               # Static assets
     ├─ /css             # Custom CSS (optional)
     └─ /img/hero.jpg    # Local hero background image
Configuration
Database URI
In app.py:

python
Copy
Edit
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'cafes.db')}"
API Key for Deletion
The default key is TopSecretAPIKey. Change it in app.py if desired.

Contributing
Fork this repository

Create a new branch (git checkout -b feature/YourFeature)

Commit your changes (git commit -m "Add awesome feature")

Push to your branch (git push origin feature/YourFeature)

Open a Pull Request

Please follow PEP 8 styling and include descriptive commit messages.

License
This project is licensed under the MIT License. See the LICENSE file for details.


 


