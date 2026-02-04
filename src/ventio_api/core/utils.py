from datetime import datetime

def calculate_age(bday_str: str) -> str:
    """
    Calculates age from a YYYY-MM-DD string.
    """
    birth_date = datetime.strptime(bday_str, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return str(age)