from dotenv import load_dotenv
import os
import google.generativeai as genai
from pathlib import Path


def load_api_key(env_var_name: str = "GOOGLE_API_KEY") -> str:
    # ŚCIEŻKA BEZWZGLĘDNA – DOPASUJ DO SWOJEGO SYSTEMU
    env_path = Path(r"C:\Users\jansl\OneDrive - uek.krakow.pl\Pulpit\ISSI\Projekt_dyplomowy\src\ai_answer_engine\.env")

    print(f"Ładuję .env z: {env_path}")  # debug
    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv(env_var_name)
    print(f"Załadowany klucz: {api_key}")  # debug

    if not api_key:
        raise ValueError(f"API key not found in environment variable: {env_var_name}")
    return api_key





def configure_gemini_client(api_key: str):
    """
    Configures the Gemini client with the provided API key.

    Args:
        api_key (str): Gemini API key.
    """
    genai.configure(api_key=api_key)


def get_profile_description(profile_name: str) -> str:
    """
    Returns a description for a given user profile.

    Args:
        profile_name (str): The predicted profile class name.

    Returns:
        str: Description of the profile.
    """
    descriptions = {
        "EcoFriendly": "Preferuje rozwiązania o niskiej emisji CO2 i rozsądnym koszcie.",
        "Saver": "Kładzie nacisk na jak najniższe koszty, nawet kosztem komfortu.",
        "QualitySeeker": "Ceni sobie komfort, wysoką jakość i niezawodność.",
        "Technophile": "Lubi nowoczesne i innowacyjne rozwiązania, nawet jeśli są droższe.",
        "Minimalist": "Stawia na prostotę i niską awaryjność, bez zbędnych funkcji."
    }
    return descriptions.get(profile_name, "Brak opisu tego profilu.")


def build_prompt(user_input: dict, predicted_profile: str, profile_description: str) -> str:
    """
    Constructs a prompt to be sent to the Gemini model.

    Args:
        user_input (dict): Dictionary of input features.
        predicted_profile (str): Predicted profile class.
        profile_description (str): Human-readable description of the profile.

    Returns:
        str: Complete prompt to send to the LLM.
    """
    return f"""
Użytkownik podał następujące wartości wejściowe:
- Koszt użytkowania (PLN): {user_input["cost_pln"]}
- Emisja CO2 (kg): {user_input["co2_emission_kg"]}
- Komfort: {user_input["normalized_comfort"]}
- Awaryjność: {user_input["normalized_failure_rate"]}
- Koszt urządzenia (ocena względna): {user_input["device_cost"]}
- Jakość gotowania: {user_input["cooking_quality"]}

Model ML przypisał użytkownikowi profil: **{predicted_profile}**
Opis profilu: {profile_description}

Wyjaśnij, dlaczego użytkownik został zaklasyfikowany jako {predicted_profile}, odnosząc się do podanych wartości.
Odpowiedz po polsku, zwięźle i jasno.
"""


def interpret_prediction_with_gemini(user_input: dict, predicted_profile: str, model_name: str = "gemini-2.0-flash") -> str:
    """
    Generates an explanation for a predicted user profile using a Gemini language model.

    Args:
        user_input (dict): Dictionary with user feature values.
        predicted_profile (str): Predicted profile class.
        model_name (str): Name of the Gemini model to use.

    Returns:
        str: Natural language explanation or error message.
    """
    profile_description = get_profile_description(predicted_profile)
    prompt = build_prompt(user_input, predicted_profile, profile_description)
    model = genai.GenerativeModel(model_name)

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Błąd podczas komunikacji z Gemini API: {e}"
