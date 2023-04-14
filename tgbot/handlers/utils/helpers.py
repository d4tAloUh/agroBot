from tgbot.handlers.utils import static_text


def extract_page(callback_text: str) -> int:
    """
        Page should be first parameter after callback text
    """
    split_text = callback_text.split(static_text.callback_separator)
    return int(split_text[1])

extract_id = extract_page
def extract_string(callback_text: str) -> str:
    """
        string should be first parameter after callback text
    """
    split_text = callback_text.split(static_text.callback_separator)
    return split_text[1]

