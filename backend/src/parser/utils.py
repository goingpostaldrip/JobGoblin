import re
from typing import Dict

def clean_tags(html_text: str | None) -> str:
    if html_text is None:
        return ""
    return re.sub(r"<.*?>", "", html_text)


def __convert_gross(is_gross: bool) -> float:
    return 0.87 if is_gross else 1


def parse_salary(salary: Dict, rates: Dict) -> Dict:
    result = {"from": None, "to": None, "currency": None}
    if not salary:
        return result

    gross_factor = __convert_gross(salary.get("gross", False))
    currency = salary.get("currency", "RUR")
    currency_rate = rates.get(currency, 1)

    for k in ("from", "to"):
        value = salary.get(k)
        if value is not None:
            result[k] = round(value * gross_factor / currency_rate)

    result["currency"] = "RUR"
    return result
