import os
import re
import tempfile
import logging
from flask_babel import gettext as _
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, jsonify, send_file,session
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from openai import OpenAI, APIStatusError, APIConnectionError, RateLimitError, Timeout

from utils.utils import (
    login_required, html_text_to_pdf, html_text_to_pptx,
    validate_inputs, load_categories_translated,load_focuses_translated,load_grades_translated,
)

from db import get_categories,get_unread_notifications

load_dotenv()

ai_bp = Blueprint("ai", __name__)
logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Helpery ---
def query_openai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful teacher assistant creating high-quality educational content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()

    except (RateLimitError, Timeout):
        return _("⚠️ OpenAI API je preťažené alebo odpovedá príliš dlho. Skúste znova neskôr.")
    except (APIStatusError, APIConnectionError) as e:
        logger.warning(f"🌐 API error: {e}")
        return _("⚠️ AI odpovedalo chybou: ") + str(e)
    except Exception as e:
        logger.exception (_("❌ Neznáma chyba OpenAI API:"))
        return _("⚠️ Interná chyba AI: ") + str(e)

def format_output_to_html(raw: str) -> str:
    raw = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", raw)
    raw = raw.replace("\n", "<br>")
    return raw

def generate_ai_output(topic: str, level: str, material_type: str, num_mcq: int = 5, num_open: int = 2) -> str:
    from app import get_locale
    locale = get_locale()
    is_sk = locale == "sk"

    level_map = {
        "1": "žiakov základnej školy" if is_sk else "primary school",
        "2": "študentov strednej školy" if is_sk else "high school",
        "3": "študentov vysokej školy" if is_sk else "university"
    }
    level_text = level_map.get(level, _("študentov") if is_sk else _("students"))

    prompt = ""

    if material_type == "Test":
        if is_sk:
            prompt = (
                f"Vytvor test na tému '{topic}' pre {level_text}.\n\n"
                "Požiadavky:\n"
                "- 5 výberových otázok (A–D) s odpoveďami.\n"
                "- 2 otvorené otázky na samostatné riešenie.\n"
                "- Začni jednoduchšími otázkami a postupne zvyšuj náročnosť.\n"
                "- Pri výberových otázkach urob všetky odpovede realisticky znejúce. Nesprávne možnosti nesmú byť očividné alebo triviálne nesprávne.\n"
                "- Každá otázka a odpoveď majú byť jasné, presné a odborné a musia mat primeranú naročnosť stupňu vzdelávania.\n"
                "- Používaj jednoduchý, stručný a zrozumiteľný jazyk.\n"
                "- Nepoužívaj HTML, markdown ani dodatočné komentáre mimo zadania.\n\n"
                "Formát výberovej otázky:\n"
                "Otázka: Aká je hlavná funkcia mitochondrie?\n"
                "A) Produkcia proteínov\n"
                "B) Riadenie bunkového delenia\n"
                "C) Výroba energie vo forme ATP\n"
                "D) Skladovanie vody\n\n"
                "Formát otvorenej otázky:\n"
                "Otvorená otázka: Vysvetli, akú úlohu má ribozóm v bunke.\n\n"
                "Na konci, na samostatnej strane, uveď:\n"
                "1. Správne odpovede na výberové otázky (napr. 1C, 2B...)\n"
                "2. Správne odpovede na otvorené otázky v stručných odsekoch."
            )
        else:
            prompt = (
                f"Create a test about the topic '{topic}' for {level_text} students.\n\n"
                "Requirements:\n"
                "- 5 multiple-choice questions (A–D) with answers.\n"
                "- 2 open-ended questions.\n"
                "- Start with easier questions and gradually move to harder ones.\n"
                "- Make all multiple-choice options sound realistic. Incorrect choices should not be obviously wrong.\n"
                "- Each question and answer must be clear, accurate, and well-thought-out, .\n"
                "- Use simple, concise, and understandable language.\n"
                "- Do not use HTML, markdown, or any extra commentary outside the tasks.\n\n"
                "Multiple-choice question format:\n"
                "Question: What is the main function of mitochondria?\n"
                "A) Production of proteins\n"
                "B) Control of cell division\n"
                "C) Generation of energy as ATP\n"
                "D) Storage of water\n\n"
                "Open-ended question format:\n"
                "Open Question: Explain the role of the ribosome in the cell.\n\n"
                "At the end, on a separate page, provide:\n"
                "1. Correct answers to multiple-choice questions (e.g., 1C, 2B...)\n"
                "2. Correct answers to open-ended questions in short paragraphs."
            )
    else:
        if is_sk:
            prompt_map = {
                "Poznámky":( f"Vytvor prehľadné poznámky k téme '{topic}' pre {level_text}.\n\n"
                            "Požiadavky:\n"
                            "- Jasná a stručná štruktúra.\n"
                            "- Používaj krátke odseky alebo bodové zoznamy tam, kde je to vhodné.\n"
                            "- Vysvetľuj pojmy jednoducho, ale odborne správne.\n"
                            "- Postupuj logicky od základných faktov ku komplexnejším súvislostiam.\n"
                            "- Používaj jednoduchý jazyk.\n"
                            "- Nepoužívaj HTML, markdown ani komentáre mimo poznámok."),
                "Prezentácia": (
                    f"Vytvor prezentáciu na tému '{topic}' pre {level_text}.\n\n"
                    "Požiadavky:\n"
                    "- Každý slide začni nadpisom 'Slide X: <Nadpis>'.\n"
                    "- Pod nadpisom uveď 2–4 odrážky začínajúce '--'.\n"
                    "- Jazyk prezentácie má byť jasný a stručný.\n"
                    "- Na konci pridaj cvičenia pre zopakovanie témy, zachovaj začiatok priklady v rovnakom formate teda '--'.\n"
                    "- Nepoužívaj HTML, markdown ani dodatočné komentáre mimo slidov."
                ),
                "Otázky a odpovede": f"Vytvor 5 otázok a odpovedí k téme '{topic}' pre {level_text}."
            }
        else:
            prompt_map = {
                "Poznámky": (f"Create clear and organized study notes about '{topic}' for {level_text} students.\n\n"
                    "Requirements:\n"
                    "- Use a clean structure with short paragraphs or bullet points where appropriate.\n"
                    "- Explain terms simply but accurately.\n"
                    "- Start with basic facts and logically build up to more complex ideas.\n"
                    "- Use concise, educational language.\n"
                    "- Do not use HTML, markdown, or any extra explanations outside the notes."),
                "Prezentácia": ( f"Create a presentation about '{topic}' for {level_text} students.\n\n"
                    "Requirements:\n"
                    "- Each slide must start with a heading 'Slide X: <Title>'.\n"
                    "- Below the heading, include 2–4 bullet points starting with '--'.\n"
                    "- Language should be clear and concise.\n"
                    "- Add review exercises at the end, dont forget to start also with '--'.\n"
                    "- Do not use HTML, markdown, or any external comments outside slides."
                    ),
                "Otázky a odpovede": f"Create 5 question and answer pairs about '{topic}' for {level_text} students."
            }
        prompt = prompt_map.get(material_type, "")

    if not prompt:
        return _("⚠️ Neznámy typ materiálu.")

    result = query_openai(prompt)
    if not result.strip():
        return _("⚠️ AI nevrátilo žiadny výstup.")
    if len(result) > 5000:
        result = result[:5000] + "<br><br>" + _("⚠️ Výstup bol skrátený.")

    return format_output_to_html(result)

# --- ROUTES ---

@ai_bp.route("/generate", methods=["GET", "POST"])
@limiter.limit("5 per minute")
@login_required
def generate():
    if request.method == "POST":
        topic = request.form.get("topic")
        level = request.form.get("level")
        material_type = request.form.get("material_type")
        num_mcq = int(request.form.get("num_mcq", 5))
        num_open = int(request.form.get("num_open", 2))

        errors = validate_inputs(topic, level, material_type)
        if errors:
            for error in errors:
                flash(f"❗ {error}", "danger")
            return redirect(url_for("ai.generate"))

        generated = generate_ai_output(topic, level, material_type, num_mcq, num_open)
        categories = load_categories_translated()
 


        flash(_("✅ Materiál bol úspešne vygenerovaný."), "success")
        return render_template(
            "ai_generate.html",
            generated=generated,
            topic=topic,
            level=level,
            material_type=material_type,
            categories=categories,
            focuses=load_focuses_translated(),
            grades=load_grades_translated()
        )

    return render_template(
        "ai_generate.html",
        generated=None,
        topic=None,
        level=None,
        material_type=None,
        categories=load_categories_translated(),
        focuses=load_focuses_translated(),
        grades=load_grades_translated()
    )

@ai_bp.route("/ai/download-material", methods=["POST"])
@login_required
def download_material():
    data = request.get_json()
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    material_type = data.get("material_type", "Poznámky")
    extension = "pptx" if material_type == "Prezentácia" else "pdf"
    filename = f"{secure_filename(title or material_type)}.{extension}"

    if not title or not content:
        return jsonify({"error": _("Názov a obsah sú povinné.")}), 400

    fd, tmp_path = tempfile.mkstemp(suffix=f".{extension}")
    os.close(fd)

    try:
        if material_type == "Prezentácia":
            html_text_to_pptx(title, content, tmp_path)
        else:
            html_text_to_pdf(content, output_path=tmp_path)

        response = send_file(
            tmp_path,
            as_attachment=True,
            download_name=filename
        )

        @response.call_on_close
        def cleanup():
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    logger.exception(_("⚠️ Nepodarilo sa zmazať dočasný súbor:"))

        return response

    except Exception as e:
        logger.exception(_("❌ Chyba pri generovaní súboru:"))
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        return jsonify({"error": _("Chyba generovania: ") + str(e)}), 500
