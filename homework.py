import datetime as dt
from typing import List, Union, Optional


class Calculator:
    """Делает общие вычисления для введеных данных."""

    def __init__(self, limit: float):
        self.limit = limit
        self.records: List[Union[int, str]] = []

    def add_record(self, data_records):
        """Добравляет запись в список."""
        self.records.append(data_records)

    def get_today_stats(self):
        """Считает кол-во потраченых каллорий/денег за текущий день."""
        today = dt.date.today()
        result = sum(
            [record.amount for record in self.records if record.date == today])
        return result

    def get_week_stats(self):
        """Считает кол-во потраченых каллорий/денег за текущую неделю."""
        today = dt.date.today()
        week = (dt.datetime.now() - dt.timedelta(days=7)).date()
        result = sum(
            [record.amount for record in self.records
                if week <= record.date <= today])
        return result

    def get_today_remained(self):
        """Вычисляет остаток калорий/денег за текущий день"""
        return self.limit - self.get_today_stats()


class Record:
    """Создает записи в виде
    amoutn - денежная сумма или количество килокалорий,
    comment - комментарий, поясняющий,
        на что потрачены деньги или откуда взялись калории,
    date - дата создания записи, по умолчанию текущая дата.
    """

    def __init__(
            self, amount: float, comment: str, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    """Калькулятор каллорий, вычисляет кол-во потребления калорий:
    за текущий день, за неделю, оставшийся лимит за день."""

    def get_calories_remained(self):
        """Выводит результат проверки калькулятора калорий за текущий день."""
        calories_remained = self.get_today_remained()
        if calories_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор денежных расходов, вычисляет траты за день, за неделю,
    оставшийся лимит за день."""

    USD_RATE = 60.0
    EURO_RATE = 70.0
    currency_dict = {
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE),
        'rub': ('руб', 1)
    }

    def get_today_cash_remained(self, currency):
        """Выводит результат проверки трат за текущий день."""
        currency_name, rate = self.currency_dict[currency]
        today_cash_remained = round(self.get_today_remained() / rate, 2)
        if today_cash_remained > 0:
            return f'На сегодня осталось {today_cash_remained} {currency_name}'
        elif today_cash_remained == 0:
            return 'Денег нет, держись'
        else:
            today_cash_remained = abs(today_cash_remained)
            return ('Денег нет, держись: '
                    f'твой долг - {today_cash_remained} {currency_name}')
