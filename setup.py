import os
import subprocess
import venv
from pathlib import Path
import secrets
try:
    from dotenv import load_dotenv, set_key
except ImportError:
    print("📦 Inštalujem knižnicu 'python-dotenv'...")
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv, set_key

# Routes
ENV_FILE = Path(".env")
VENV_DIR = Path("venv")
REQUIREMENTS_FILE = "requirements.txt"
SQL_FILE = "schema.sql"
APP_FILE = "app.py"

# Default values for .env
ENV_DEFAULTS = {
    "DATABASE_HOST": "127.0.0.1",
    "DATABASE_PORT": "5432",
    "DATABASE_NAME": "mydb",
    "DATABASE_USER": "xovsonka",
    "DATABASE_PASSWORD": "SuperTajneHeslo",
    "UPLOAD_FOLDER": "static/uploads",
    "SECRET_KEY": "",  # filled automaticly
    "OPENAI_API_KEY": "",
    "WKHTMLTOPDF_PATH": r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

}

def generate_secret_key():
    return secrets.token_hex(32)

def create_env_file():
    print("📄 Creating env file..")
    with open(ENV_FILE, "w") as f:
        for key, value in ENV_DEFAULTS.items():
            f.write(f"{key}={value}\n")

def ensure_env_values():
    load_dotenv(override=False)
    updated = False
    for key, default in ENV_DEFAULTS.items():
        if os.getenv(key) is None or os.getenv(key) == "":
            value = generate_secret_key() if key == "SECRET_KEY" else default
            set_key(str(ENV_FILE), key, value)
            updated = True
    if updated:
        print("🔑 Added values to env")

def create_venv():
    if not VENV_DIR.exists():
        print("🐍 Creating venv")
        venv.create(str(VENV_DIR), with_pip=True)
    else:
        print("✅ Venv exist.")

def install_requirements():
    print("📦 Installing requirements.txt...")
    pip = VENV_DIR / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")
    subprocess.run([str(pip), "install", "-r", REQUIREMENTS_FILE], check=True)

def init_postgres():
    print("🗄️ Setting up PostgreSQL")
    load_dotenv(override=True)
    env = os.environ.copy()
    env["PGPASSWORD"] = os.getenv("DATABASE_PASSWORD")

    # Creating DB
    check_cmd = [
        "psql",
        "-h", os.getenv("DATABASE_HOST"),
        "-p", os.getenv("DATABASE_PORT"),
        "-U", os.getenv("DATABASE_USER"),
        "-d", "postgres",
        "-tc", f"SELECT 1 FROM pg_database WHERE datname = '{os.getenv('DATABASE_NAME')}';"
    ]
    result = subprocess.run(check_cmd, env=env, capture_output=True, text=True)
    if '1' not in result.stdout:
        print("🆕 Creating db")
        subprocess.run([
            "createdb",
            "-h", os.getenv("DATABASE_HOST"),
            "-p", os.getenv("DATABASE_PORT"),
            "-U", os.getenv("DATABASE_USER"),
            os.getenv("DATABASE_NAME")
        ], env=env, check=True)
    else:
        print("✅ DB alredy exist.")

    # Import SQL
    subprocess.run([
        "psql",
        "-h", os.getenv("DATABASE_HOST"),
        "-p", os.getenv("DATABASE_PORT"),
        "-U", os.getenv("DATABASE_USER"),
        "-d", os.getenv("DATABASE_NAME"),
        "-f", SQL_FILE
    ], env=env, check=True)

def run_app():
    python = VENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    print("🚀 Spúšťam aplikáciu...")
    subprocess.run([str(python), APP_FILE])

def main():
    try:
        if not ENV_FILE.exists():
            create_env_file()
        ensure_env_values()
        create_venv()
        install_requirements()
        init_postgres()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error:{e}")
        exit(1)

if __name__ == "__main__":
    main()
