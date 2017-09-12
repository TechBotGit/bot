def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
button_list = [
    InlineKeyboardButton("col 1", text("Testing")),
    InlineKeyboardButton("col 2", text("Testing2")),
    InlineKeyboardButton("row 2", text("Testing3"))
]
reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
bot.send_message(..., "A two-column menu", reply_markup=reply_markup)