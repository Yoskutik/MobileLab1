import pandas as pd


def count_telephony(k, T):
    return k * T


def count_sms(k, N):
    return N * k


TEL = 915783624
K_IN = 2
K_OUT = 0
K_SMS = 1

df = pd.read_csv('data.csv')

ingoing = count_telephony(K_IN, df[df.msisdn_dest == TEL].call_duration.values[0])
outgoing = count_telephony(K_OUT, df[df.msisdn_origin == TEL].call_duration.values[0])
sms = count_sms(K_SMS, df[df.msisdn_origin == TEL].sms_number.values[0] - 10)

print(f'Стоимость входящих звонков: {ingoing}')
print(f'Стоимость исходящих звонков: {outgoing}')
print(f'Стоимость СМС: {sms}')
print(f'Общая стоимость: {sms + ingoing + outgoing}')