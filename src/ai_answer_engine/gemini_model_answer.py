from dotenv import load_dotenv
import os
import google.generativeai as genai
from pathlib import Path

def load_api_key(env_var_name: str = "GOOGLE_API_KEY") -> str:
    # ŚCIEŻKA BEZWZGLĘDNA – DOPASUJ DO SWOJEGO SYSTEMU
    #env_path = Path(r"C:\Users\jansl\OneDrive - uek.krakow.pl\Pulpit\ISSI\Projekt_dyplomowy\src\ai_answer_engine\.env")
    env_path = Path(r"/Volumes/T7/Projekty/Projekt-Dyplomowy-ISSI-Jan-lusarek-Kacper-Gruca/src/ai_answer_engine/.env")

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
        "EcoFriendly": "Priorytetem jest minimalna emisja CO₂. Użytkownik toleruje umiarkowane koszty, awaryjność i komfort, jeśli oznacza to bardziej ekologiczne rozwiązanie.",
        "Saver": "Najważniejsze są niskie koszty użytkowania. Komfort, emisja CO₂ i inne cechy mają drugorzędne znaczenie – liczy się oszczędność.",
        "ComfortSeeker": "Najbardziej liczy się komfort użytkowania. Osoba z tym profilem stawia wygodę ponad kosztami czy efektywnością energetyczną.",
        "Budget": "Najważniejszy jest niski koszt zakupu urządzenia. Pozostałe aspekty są mniej istotne – użytkownik szuka budżetowych opcji.",
        "RiskAware": "Najważniejsza jest niska awaryjność. Osoba z tym profilem unika ryzyka związanego z zawodnością sprzętu, nawet kosztem innych parametrów.",
        "QualitySeeker": "Skupia się na jakości, niezawodności oraz wysokim komforcie. Jest gotów ponieść wyższe koszty, byle produkt spełniał wysokie standardy.",
        "Bourgeois": "Stawia na wysoką jakość, komfort oraz prestiż. Może akceptować wyższe koszty i emisje CO₂, jeśli urządzenie wpisuje się w styl życia klasy wyższej."
    }
    return descriptions.get(profile_name, "Brak opisu tego profilu.")


def interpret_prediction_with_gemini(
    user_input: dict,
    predicted_profiles: tuple[str, str, str],
    model_name: str = "gemini-2.0-flash"
) -> str:
    """
    Generates an explanation for top-2 most probable and the least probable user profile using Gemini.
    """
    profile_1_desc = get_profile_description(predicted_profiles[0])
    profile_2_desc = get_profile_description(predicted_profiles[1])
    print(predicted_profiles)

    prompt = build_prompt(
        user_input,
        predicted_profiles,
        profile_1_desc,
        profile_2_desc,
    )

    model = genai.GenerativeModel(model_name)

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Błąd podczas komunikacji z Gemini API: {e}"

    

def build_prompt(user_input: dict, predicted_profiles: tuple[str, str], profile_1_desc: str, profile_2_desc: str) -> str:
    """
    Constructs a prompt to be sent to the Gemini model.

    Args:
        user_input (dict): Dictionary of input features.
        predicted_profiles (tuple): Tuple with 1st and 2nd most probable profile names.
        profile_1_desc (str): Description of the most probable profile.
        profile_2_desc (str): Description of the second most probable profile.

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

Model ML przypisał użytkownikowi profil: **{predicted_profiles[0]}**
Opis profilu: {profile_1_desc}

Wyjaśnij, dlaczego użytkownik został zaklasyfikowany jako najbardziej prawdopodobnie {predicted_profiles[0]}, odnosząc się do podanych wartości.

Następnie skomentuj drugi możliwy wynik jako alternatywny: **{predicted_profiles[1]}**
Opis profilu: {profile_2_desc}

Opowiedz w podsumowaniu że rekomendujesz najbardziej prawdopodobny wynik, ale czasem alternatywa jest zasadna .

Odpowiedz po polsku, zwięźle i jasno.
"""

