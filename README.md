# 📚 EduForm – How to Run the Application

## ✅ Requirements

Make sure the following tools are installed:

- **Python 3.10+**
- **wkhtmltopdf** (installed and available in system `PATH`)
- **pip** – Python package manager
- **PostgreSQL** – Running database server
- **psql** – PostgreSQL CLI client in `PATH`
- **Git** – Installed and available in `PATH`
- **OpenAI API key** (optional, requires paid account)

---

## 🛠 1. Installing `wkhtmltopdf`

### Windows

1. Download from: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)  
2. Install it and add the following path to your system `PATH`:  
   ```
   C:\Program Files\wkhtmltopdf\bin
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install wkhtmltopdf
```

### macOS

```bash
brew install wkhtmltopdf
```

### Verify Installation

```bash
wkhtmltopdf --version
```

---

## 📦 2. Clone the Repository

```bash
git clone https://github.com/xovsonka/EduForm.git
cd EduForm
```

---

## ⚙️ 3. Configuration via `setup.py` (One of two set up options)

Open `setup.py` and edit the following variables:

- `DATABASE_NAME`
- `DATABASE_USER`
- `DATABASE_PASSWORD`
- `UPLOAD_FOLDER`
- `WKHTMLTOPDF_PATH`

Then run the script:

```bash
python setup.py
```

> ⚠️ Make sure `psql` is in your system `PATH`; otherwise, the DB setup will fail.

---

## 🧪 4. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📥 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 6. Create a `.env` File

In the project root directory, create a file named `.env` with the following content:

```env
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DATABASE_NAME=your_database
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
UPLOAD_FOLDER=static/uploads
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
WKHTMLTOPDF_PATH=C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
```

> Adjust the `WKHTMLTOPDF_PATH` based on your operating system.

### Generate `SECRET_KEY`

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it into the `.env` file.

---

## 🗄 7. Initialize the Database

Using `psql`:

```bash
psql -U your_username -d your_database -f schema.sql
```

Or use **pgAdmin** to import `schema.sql` manually.

---

## 🚀 8. Run the Application

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000/login
```

---

✅ You're now ready to use **EduForm**!
