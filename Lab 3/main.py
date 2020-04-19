from functions import *


pdf = FPDF()
pdf.add_page()
pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
pdf.add_font('DejaVuBold', '', 'DejaVuSans-Bold.ttf', uni=True)
height = draw_bank_table(pdf,
                         beneficiary_bank='ОАО "Железный банк КАКБУДТОИЗИГРЫПРЕСТОЛОВ"',
                         INN='88005553535',
                         KPP='56277277353',
                         beneficiary='ОOО "Его величество Демиург - Великий Создатель, повелитель интернета"',
                         BIK='313915886',
                         account1='888833333386428',
                         account2='64242313185757')
height = draw_title(pdf,
                    number=82,
                    year=20,
                    height=height)
height = draw_supplier_buyer(pdf,
                             height=height,
                             supplier='ОOО "Его величество Демиург - Великий Создатель, повелитель интернета", '
                                      'с. Белый Сад, д. У конюшни',
                             buyer='ООО ЛАГУНА, ИНН 7714037378, КПП 777550001, 119361, '
                                   'Москва г, , ТУЛЬСКАЯ М. ул, дом № 4, строение 1',
                             base='№ 20022016 от 12.02.2016')
height = draw_goods_table(pdf, [
    {
        'Name': 'Входящие вызовы',
        'Amount': 12.34,
        'Amount_unit': 'мин.',
        'Number': '',
        'Price': 0,
    }, {
        'Name': 'Исходящие вызовы',
        'Amount': 36.23,
        'Amount_unit': 'мин.',
        'Number': '',
        'Price': 2,
    }, {
        'Name': 'СМС',
        'Amount': 5,
        'Amount_unit': 'шт.',
        'Number': '',
        'Price': 1,
    }, {
        'Name': 'Исходящий трафик',
        'Amount': 0,
        'Amount_unit': 'Мб',
        'Number': '',
        'Price': 0.5,
    }, {
        'Name': 'Входящий трафик',
        'Amount': 176.81,
        'Amount_unit': 'Мб',
        'Number': '',
        'Price': 0.5,
    },
], height=height)
height = draw_footer(pdf,
                     height=height,
                     director='Александрович Д.А.',
                     accountant='Александрович   Д.А.')

pdf.output('file.pdf')
