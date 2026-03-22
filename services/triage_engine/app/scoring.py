def calculate_urgency(symptoms: str) -> int:

    symptoms = symptoms.lower()

    if "chest pain" in symptoms:
        return 5
    elif "breathing" in symptoms:
        return 4
    elif "fever" in symptoms:
        return 2
    else:
        return 1