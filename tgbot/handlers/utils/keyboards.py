from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from tgbot.handlers.utils import static_text


def make_paginated_keyboard(**kwargs) -> InlineKeyboardMarkup:
    items = kwargs.get("items")
    page = kwargs.get("page")
    is_last_page = kwargs.get("is_last_page")
    item_text_getter = kwargs.get("item_text_getter", lambda x: x.name)
    get_item_callback = kwargs.get("get_item_callback")
    prev_page_callback = kwargs.get("prev_page_callback")
    next_page_callback = kwargs.get("next_page_callback")
    go_back_callback = kwargs.get("go_back_callback")
    go_back_text = kwargs.get("go_back_text", static_text.go_back_text)
    per_row = kwargs.get("per_row", 3)
    rows = kwargs.get("rows", 2)
    markup = []
    row_markup = []
    # Add prev/next buttons
    if not is_last_page:
        row_markup.append(
            InlineKeyboardButton(
                text=static_text.next_page_text,
                callback_data=next_page_callback
            )
        )
    if page != 1:
        row_markup.append(
            InlineKeyboardButton(
                text=static_text.prev_page_text,
                callback_data=prev_page_callback
            )
        )
    markup.append(row_markup)
    # Add items
    for row_num in range(rows):
        row_markup = []
        for item in items[row_num * per_row: (row_num + 1) * per_row]:
            row_markup.append(InlineKeyboardButton(
                text=item_text_getter(item),
                callback_data=get_item_callback(item)
            ))
        markup.append(row_markup)
    # Add go back button
    markup.append(
        [InlineKeyboardButton(
            text=go_back_text,
            callback_data=go_back_callback
        )]
    )
    return InlineKeyboardMarkup(markup)
