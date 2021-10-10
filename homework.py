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
        today = dt.datetime.now().date()
        result = 0
        data_records = self.records
        for record in data_records:
            if type(record.amount) == int and record.date == today:
                result += record.amount
        return result

    def get_week_stats(self):
        """Считает кол-во потраченых каллорий/денег за текущую неделю."""
        today = dt.datetime.now().date()
        week = (dt.datetime.now() - dt.timedelta(days=7)).date()
        result = 0
        data_records = self.records
        for record in data_records:
            if type(record.amount) == int and week <= record.date <= today:
                result += record.amount
        return result


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
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    """Калькулятор каллорий, вычисляет кол-во потребления калорий:
    за текущий день, за неделю, оставшийся лимит за день."""

    def __init__(self, limit: float):
        super().__init__(limit)

    def get_calories_remained(self):
        """Выводит результат проверки калькулятора калорий за текущий день."""
        today_calories = super().get_today_stats()
        limit = self.limit
        calories_remained = self.limit - super().get_today_stats()
        if today_calories < limit:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор денежных расходов, вычисляет траты за день, за неделю,
    оставшийся лимит за день."""

    def __init__(self, limit: float):
        super().__init__(limit)
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
        today_cash = super().get_today_stats()
        today_cash_remained = round((self.limit - today_cash) / rate, 2)
        if today_cash_remained > 0:
            return f'На сегодня осталось {today_cash_remained} {currency_name}'
        elif today_cash_remained == 0:
            return 'Денег нет, держись'
        else:
            today_cash_remained = -1 * today_cash_remained
            return ('Денег нет, держись: '
                    f'твой долг - {today_cash_remained} {currency_name}')
