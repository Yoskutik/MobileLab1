from fpdf import FPDF
from num2words import num2words


MAX_WIDTH = 210
PAD = 20


def draw_bank_table(pdf: FPDF, **kwargs):
    l_col_w = 95
    m_col_w = 16
    height = 30
    r_col_w = MAX_WIDTH - PAD * 2 - l_col_w - m_col_w
    pdf.line(PAD, PAD, MAX_WIDTH - 20, PAD)
    pdf.line(PAD, PAD, PAD, height + PAD)
    pdf.line(MAX_WIDTH - PAD, PAD, MAX_WIDTH - PAD, height + PAD)
    pdf.line(PAD, height + PAD, MAX_WIDTH - PAD, height + PAD)

    pdf.line(PAD, height * 9 / 21 + PAD, MAX_WIDTH - PAD, height * 9 / 21 + PAD)
    pdf.line(PAD, height * 12 / 21 + PAD, l_col_w + PAD, height * 12 / 21 + PAD)
    pdf.line(l_col_w + PAD, PAD, l_col_w + PAD, height + PAD)
    pdf.line(l_col_w + PAD + m_col_w, PAD, l_col_w + PAD + m_col_w, height + PAD)
    pdf.line(l_col_w + PAD, PAD + height * 3 / 21, l_col_w + m_col_w + PAD, PAD + height * 3 / 21)
    pdf.line(PAD + l_col_w / 2, PAD + height * 9 / 21, PAD + l_col_w / 2, PAD + height * 12 / 21)

    pdf.set_font("DejaVu", size=9)
    pdf.set_y(PAD)
    pdf.cell(10)
    pdf.multi_cell(95, 4, kwargs['beneficiary_bank'])
    pdf.set_y(PAD + 12.5)
    pdf.cell(10)
    pdf.cell(l_col_w / 2, 5, f'ИНН    {kwargs["INN"]}')
    pdf.cell(l_col_w / 2, 5, f'КПП    {kwargs["KPP"]}')
    pdf.set_y(PAD + 17.5)
    pdf.cell(10)
    pdf.multi_cell(95, 4, kwargs['beneficiary'])
    pdf.set_y(PAD)
    pdf.cell(10 + l_col_w)
    pdf.cell(m_col_w, 5, 'БИК')
    pdf.cell(r_col_w, 5, kwargs['BIK'])
    pdf.set_y(PAD + 5)
    pdf.cell(10 + l_col_w)
    pdf.cell(m_col_w, 5, 'Сч. №')
    pdf.cell(r_col_w, 5, kwargs['account1'])
    pdf.set_y(PAD + height * 9 / 21)
    pdf.cell(10 + l_col_w)
    pdf.cell(m_col_w, 5, 'Сч. №')
    pdf.cell(r_col_w, 5, kwargs['account2'])

    pdf.set_font("DejaVu", size=8)
    pdf.set_y(PAD + height * 6 / 21)
    pdf.cell(10)
    pdf.cell(l_col_w, 4, 'Банк получателя')
    pdf.set_y(PAD + height * 18 / 21)
    pdf.cell(10)
    pdf.cell(l_col_w, 4, 'Получатель')

    return PAD + height


def draw_title(pdf: FPDF, **kwargs):
    pdf.set_font("DejaVuBold", size=13)
    pdf.set_y(kwargs['height'] + 4)
    pdf.cell(10)
    pdf.cell(MAX_WIDTH - PAD, 9, f'Счет на оплату № {kwargs["number"]} от 20{kwargs["year"]} г.')
    pdf.set_line_width(0.6)
    pdf.line(PAD, kwargs['height'] + 13.5, MAX_WIDTH - PAD, kwargs['height'] + 13.5)

    return kwargs['height'] + 14.1


def draw_supplier_buyer(pdf: FPDF, **kwargs):
    l_col_w = 28
    r_col_w = MAX_WIDTH - 2 * PAD - l_col_w
    line_height = 5
    pdf.set_font("DejaVu", size=9)
    pdf.set_y(kwargs['height'] + 2)
    pdf.cell(10)
    pdf.multi_cell(l_col_w, line_height, 'Поставщик (Исполнитель):')

    pdf.set_font("DejaVuBold", size=9)
    pdf.set_y(kwargs['height'] + 2)
    pdf.cell(10 + l_col_w)
    supplier = pdf.multi_cell(r_col_w, line_height, kwargs['supplier'], split_only=True)
    pdf.multi_cell(r_col_w, line_height, kwargs['supplier'])

    height = kwargs['height'] + 6 + 5 * len(supplier)
    pdf.set_font("DejaVu", size=9)
    pdf.set_y(height)
    pdf.cell(10)
    pdf.multi_cell(l_col_w, line_height, 'Покупатель (Заказчик):')

    pdf.set_font("DejaVuBold", size=9)
    pdf.set_y(height)
    pdf.cell(10 + l_col_w)
    buyer = pdf.multi_cell(r_col_w, line_height, kwargs['buyer'], split_only=True)
    pdf.multi_cell(r_col_w, line_height, kwargs['buyer'])

    height += len(buyer) * 5 + 6
    pdf.set_y(height)
    pdf.cell(10)
    pdf.set_font("DejaVu", size=9)
    pdf.cell(l_col_w, line_height, 'Основание:')
    pdf.set_font("DejaVuBold", size=9)
    pdf.cell(r_col_w, line_height, kwargs['base'])

    return height + line_height


def draw_goods_table(pdf: FPDF, goods, **kwargs):
    col1_w = 8
    col3_w = 20
    col4_w = 18
    col5_w = 18
    col2_w = MAX_WIDTH - 2 * PAD - col1_w - col3_w - col4_w - col5_w
    height = kwargs['height'] + 6
    start = height
    total = 0
    pdf.set_line_width(0.5)
    pdf.line(PAD, height, MAX_WIDTH - PAD, height)
    pdf.set_line_width(0.2)
    pdf.line(PAD, height + 5, MAX_WIDTH - PAD, height + 5)

    pdf.set_font("DejaVuBold", size=9)
    pdf.set_y(height)
    pdf.cell(10)
    pdf.cell(col1_w, 5, '№', align='C')
    pdf.cell(col2_w, 5, 'Товары (работы, услуги)', align='C')
    pdf.cell(col3_w, 5, 'Кол-во', align='C')
    pdf.cell(col4_w, 5, 'Цена', align='C')
    pdf.cell(col5_w, 5, 'Сумма', align='C')

    pdf.set_font("DejaVu", size=9)
    height += 6
    index = 0
    for id, good in enumerate(goods):
        is_last = id == len(goods) - 1
        index += 1
        pdf.set_y(height)
        pdf.cell(10)
        pdf.cell(col1_w, 5, str(index), align='C')
        pdf.multi_cell(col2_w, 5, good['Name'])
        pdf.set_y(height)
        pdf.cell(10 + col1_w + col2_w)
        pdf.cell(col3_w, 5, f'{good["Amount"]}{" " + good["Amount_unit"] if "Amount_unit" in good else ""}', align='L')
        pdf.cell(col4_w, 5, f'{good["Price"]} {"p/" + good["Amount_unit"] if "Amount_unit" in good else "p"}', align='L')
        pdf.cell(col5_w, 5, f'{good["Price"] * good["Amount"]} р', align='R')
        total += good["Price"] * good["Amount"]

        height += 5 * len(pdf.multi_cell(col2_w, 100, good['Name'], split_only=True))
        if not is_last:
            pdf.line(PAD, height + 1, MAX_WIDTH - PAD, height + 1)
            height += 2
        else:
            height += 1

    pdf.set_line_width(0.5)
    pdf.line(PAD, start, PAD, height)
    pdf.line(PAD, height, MAX_WIDTH - PAD, height)
    pdf.line(MAX_WIDTH - PAD, start, MAX_WIDTH - PAD, height)

    pdf.set_line_width(0.2)
    pdf.line(PAD + col1_w, start, PAD + col1_w, height)
    pdf.line(PAD + col1_w + col2_w, start, PAD + col1_w + col2_w, height)
    pdf.line(PAD + col1_w + col2_w + col3_w, start, PAD + col1_w + col2_w + col3_w, height)
    pdf.line(PAD + col1_w + col2_w + col3_w + col4_w, start, PAD + col1_w + col2_w + col3_w + col4_w, height)
    pdf.line(PAD + col1_w + col2_w + col3_w + col4_w + col5_w, start, PAD + col1_w + col2_w + col3_w + col4_w + col5_w, height)

    height += 5
    pdf.set_font("DejaVuBold", size=9)
    pdf.set_y(height)
    total_str = f'{total:,.2f}'.replace(',', ' ')
    nds_str = f'{total * 0.167:,.2f}'.replace(',', ' ')
    pdf.multi_cell(10 + MAX_WIDTH - 2 * PAD, 5, f'Итого: {total_str:>15} р.', align='R')
    pdf.multi_cell(10 + MAX_WIDTH - 2 * PAD, 5, f'В том числе НДС: {nds_str:>15} р.', align='R')
    pdf.multi_cell(10 + MAX_WIDTH - 2 * PAD, 5, f'Всего к оплате: {total_str:>15} р.', align='R')

    pdf.set_font("DejaVu", size=9)
    pdf.cell(10)
    pdf.multi_cell(MAX_WIDTH - 2 * PAD, 5, f'Всего наименований {index} на сумму {total_str} руб.')
    pdf.set_font("DejaVuBold", size=9)
    pdf.cell(10)
    pdf.multi_cell(MAX_WIDTH - 2 * PAD, 5, f'{num2words(int(total), lang="ru").capitalize()} рублей '
                                           f'{total_str[-2:].zfill(2)} копеек.')

    return height + 25


def draw_footer(pdf: FPDF, **kwargs):
    def add_text(text, height):
        pdf.cell(10)
        height += 4 * len(pdf.multi_cell(MAX_WIDTH - 2 * PAD, 4, text, split_only=True))
        pdf.multi_cell(MAX_WIDTH - 2 * PAD, 4, text)
        return height
    height = kwargs['height'] + 10
    pdf.set_font("DejaVu", size=8)
    pdf.set_y(height)
    height = add_text('Внимание!', height)
    height = add_text('Оплата данного счета означает согласие с условиями поставки товара.', height)
    height = add_text('Уведомление об оплате обязательно, в противном случае не гарантируется наличие товара на складе.', height)
    height = add_text('Товар отпускается по факту прихода денег на р/с Поставщика, самовывозом, при наличии доверенности и паспорта.', height)

    pdf.set_line_width(0.5)
    pdf.line(PAD, height + 4, MAX_WIDTH - PAD, height + 4)
    height += 10

    pdf.set_y(height)
    pdf.set_font("DejaVuBold", size=9)
    pdf.cell(10)
    pdf.cell(30, 5, 'Руководитель')
    pdf.set_font("DejaVu", size=9)
    pdf.cell(60, 5, kwargs['director'], align='R')
    pdf.set_font("DejaVuBold", size=9)
    pdf.cell(30, 5, 'Бухгалтер', align='C')
    pdf.set_font("DejaVu", size=9)
    pdf.cell(MAX_WIDTH - 2 * PAD - 120, 5, kwargs['accountant'], align='R')

    pdf.set_line_width(0.2)
    pdf.line(PAD + 35, height + 5, PAD + 90, height + 5)
    pdf.line(PAD + 120, height + 5, MAX_WIDTH - PAD, height + 5)

    return height
