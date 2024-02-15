# -*- coding: utf-8 -*-
# 1 : imports of python lib

# 2 : imports of odoo

# 3 : imports from odoo modules

# 4 : variable declarations


def l10n_hu_amount_to_text(amount):
    """ Get an amount as hungarian text

    :param amount: float

    :return dictionary
    """
    # Initialize variables
    debug_list = []
    error_list = []
    info_list = []
    result = {}
    warning_list = []

    # Amount
    debug_list.append(str(amount))

    # Absolute amount
    amount_absolute = abs(amount)
    debug_list.append(str(amount_absolute))

    # Integer absolute amount string
    amount_absolute_integer_string = str(int(amount_absolute))
    debug_list.append(amount_absolute_integer_string)

    # Digits amount
    amount_digits = amount % 1
    debug_list.append(str(amount_digits))

    # Digits amount string
    amount_digits_string = str(amount_digits).split('.')[1]
    debug_list.append(str(amount_digits_string))

    # Explore what we have
    if len(amount_absolute_integer_string) >= 1:
        single_1 = amount_absolute_integer_string[-1]
    else:
        single_1 = False
    if len(amount_absolute_integer_string) >= 2:
        tens_2 = amount_absolute_integer_string[-2]
    else:
        tens_2 = False
    if len(amount_absolute_integer_string) >= 3:
        hundreds_3 = amount_absolute_integer_string[-3]
    else:
        hundreds_3 = False
    if len(amount_absolute_integer_string) >= 4:
        thousands_4 = amount_absolute_integer_string[-4]
    else:
        thousands_4 = False
    if len(amount_absolute_integer_string) >= 5:
        thousands_5 = amount_absolute_integer_string[-5]
    else:
        thousands_5 = False
    if len(amount_absolute_integer_string) >= 6:
        thousands_6 = amount_absolute_integer_string[-6]
    else:
        thousands_6 = False
    if len(amount_absolute_integer_string) >= 7:
        millions_7 = amount_absolute_integer_string[-7]
    else:
        millions_7 = False
    if len(amount_absolute_integer_string) >= 8:
        millions_8 = amount_absolute_integer_string[-8]
    else:
        millions_8 = False
    if len(amount_absolute_integer_string) >= 9:
        millions_9 = amount_absolute_integer_string[-9]
    else:
        millions_9 = False
    if len(amount_absolute_integer_string) >= 10:
        billions_10 = amount_absolute_integer_string[-10]
    else:
        billions_10 = False
    if len(amount_absolute_integer_string) >= 11:
        billions_11 = amount_absolute_integer_string[-11]
    else:
        billions_11 = False
    if len(amount_absolute_integer_string) >= 12:
        billions_12 = amount_absolute_integer_string[-12]
    else:
        billions_12 = False

    # string part: between 0 and 10
    if single_1 and single_1 != '0':
        single_digit_string = l10n_hu_amount_to_text_part(int(single_1))
    elif 0 >= amount_absolute < 1:
        single_digit_string = "nulla"
    else:
        single_digit_string = ""
    debug_list.append("single_digit_string: " + single_digit_string)

    # string part for tens
    if tens_2 and tens_2 != '0':
        tens_string = l10n_hu_amount_to_text_part(int(tens_2+single_1))
    else:
        tens_string = ""
    debug_list.append("tens_string: " + tens_string)

    # string part for hundreds (we need position 3)
    if hundreds_3 and hundreds_3 != '0':
        hundreds_string = l10n_hu_amount_to_text_part(int(hundreds_3))
        hundreds_string += "száz"
    else:
        hundreds_string = ""
    debug_list.append("hundreds_string: " + hundreds_string)

    # string part for thousands
    if thousands_4 and thousands_5 and thousands_6:
        # hundreds position
        if thousands_6 != '0':
            thousands_string = l10n_hu_amount_to_text_part(int(thousands_6))
            thousands_string += "száz"
        else:
            thousands_string = ""
        # tens position
        thousands_string += l10n_hu_amount_to_text_part(int(thousands_5 + thousands_4))
        if thousands_4 != '0':
            thousands_string += l10n_hu_amount_to_text_part(int(thousands_4))
        thousands_string += "ezer"
        debug_list.append(thousands_6 + thousands_5 + thousands_4)
    elif thousands_4 and thousands_5:
        thousands_string = l10n_hu_amount_to_text_part(int(thousands_5 + thousands_4))
        if thousands_4 != '0':
            thousands_string += l10n_hu_amount_to_text_part(int(thousands_4))
        thousands_string += "ezer"
        debug_list.append(thousands_5 + thousands_4)
    elif thousands_4:
        thousands_string = l10n_hu_amount_to_text_part(int(thousands_4))
        thousands_string += "ezer"
        debug_list.append(thousands_4)
    else:
        thousands_string = ""
    debug_list.append("thousands_string: " + thousands_string)

    # string part for millions
    if millions_7 and millions_8 and millions_9:
        # hundreds position
        if millions_9 != '0':
            millions_string = l10n_hu_amount_to_text_part(int(millions_9))
            millions_string += "száz"
        else:
            millions_string = ""

        # tens position
        millions_string += l10n_hu_amount_to_text_part(int(millions_8 + millions_7))
        if millions_7 != '0':
            millions_string += l10n_hu_amount_to_text_part(int(millions_7))
        millions_string += "ezer"
        debug_list.append(millions_9 + millions_8 + millions_7)
    elif millions_7 and millions_8:
        millions_string = l10n_hu_amount_to_text_part(int(millions_8 + millions_7))
        if millions_7 != '0':
            millions_string += l10n_hu_amount_to_text_part(int(millions_7))
        millions_string += "millió"
        debug_list.append(millions_8 + millions_7)
    elif millions_7:
        millions_string = l10n_hu_amount_to_text_part(int(millions_7))
        millions_string += "millió"
        debug_list.append(millions_7)
    else:
        millions_string = ""
    debug_list.append("millions_string: " + millions_string)

    # string part for billions
    if billions_10 and billions_11 and billions_12:
        # hundreds position
        if billions_12 != '0':
            billions_string = l10n_hu_amount_to_text_part(int(billions_12))
            billions_string += "száz"
        else:
            billions_string = ""

        # tens position
        billions_string += l10n_hu_amount_to_text_part(int(billions_11 + billions_10))
        if billions_10 != '0':
            billions_string += l10n_hu_amount_to_text_part(int(billions_10))
        billions_string += "ezer"
        debug_list.append(billions_12 + billions_11 + billions_10)
    elif billions_10 and billions_11:
        billions_string = l10n_hu_amount_to_text_part(int(billions_11 + billions_10))
        if billions_10 != '0':
            billions_string += l10n_hu_amount_to_text_part(int(billions_10))
        billions_string += "milliárd"
        debug_list.append(billions_11 + billions_10)
    elif billions_10:
        billions_string = l10n_hu_amount_to_text_part(int(billions_10))
        billions_string += "milliárd"
        debug_list.append(billions_10)
    else:
        billions_string = ""
    debug_list.append("billions_string: " + billions_string)

    # Decimal strings TODO

    # Finalize string according to special rules
    # 1) until 2000 everything is one word
    if amount_absolute <= 2000:
        amount_text = thousands_string
        amount_text += hundreds_string
        amount_text += tens_string
        amount_text += single_digit_string
    # 2) above 2000 every rounded thousands and above are in one word
    elif single_1 == '0' and tens_2 == '0' and hundreds_3 == '0':
        amount_text = billions_string
        amount_text += millions_string
        amount_text += thousands_string
        amount_text += hundreds_string
        amount_text += tens_string
        amount_text += single_digit_string
    # 3) else we group by thousands separated by dash
    else:
        amount_text = ""
        if len(billions_string) > 0:
            amount_text += billions_string
            amount_text += "-"
        if len(millions_string) > 0:
            amount_text += millions_string
            amount_text += "-"
        amount_text += thousands_string
        amount_text += "-"
        amount_text += hundreds_string
        amount_text += tens_string
        amount_text += single_digit_string

    # Negative amounts
    if amount < 0:
        amount_text = "mínusz " + amount_text

    # Finalize result
    result.update({
        'amount': amount,
        'amount_text': amount_text,
        'debug_list': debug_list,
        'error_list': error_list,
        'info_list': info_list,
        'warning_list': warning_list
    })

    # Return result
    return result


def l10n_hu_amount_to_text_part(amount):
    """ Process a part of a number

    Input amount is maximum 2 digits (eg: 1, 23) all other are managed in the parent method

    :param amount: integer

    :return: string
    """
    # Single digits
    if len(str(amount)) == 1:
        if amount == 0:
            amount_text = 'nulla'
        elif amount == 1:
            amount_text = 'egy'
        elif amount == 2:
            amount_text = 'kettő'
        elif amount == 3:
            amount_text = 'három'
        elif amount == 4:
            amount_text = 'négy'
        elif amount == 5:
            amount_text = 'öt'
        elif amount == 6:
            amount_text = 'hat'
        elif amount == 7:
            amount_text = 'hét'
        elif amount == 8:
            amount_text = 'nyolc'
        elif amount == 9:
            amount_text = 'kilenc'
        else:
            amount_text = 'single_digit_error ' + str(amount)

    # Double digits
    elif len(str(amount)) == 2:
        if amount == 10:
            amount_text = 'tíz'
        elif 10 < amount < 20:
            amount_text = 'tizen'
        elif amount == 20:
            amount_text = 'húsz'
        elif 20 < amount < 30:
            amount_text = 'huszon'
        elif 30 <= amount < 40:
            amount_text = 'harminc'
        elif 40 <= amount < 50:
            amount_text = 'negyven'
        elif 50 <= amount < 60:
            amount_text = 'ötven'
        elif 60 <= amount < 70:
            amount_text = 'hatvan'
        elif 70 <= amount < 80:
            amount_text = 'hetven'
        elif 80 <= amount < 90:
            amount_text = 'nyolcvan'
        elif 90 <= amount < 100:
            amount_text = 'kilencven'
        else:
            amount_text = 'double_digit_error ' + str(amount)
    else:
        amount_text = 'error ' + str(amount)

    # Return
    return amount_text
