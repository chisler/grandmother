import time

from external.dev_ethfinex import dev_ethfinex_api


def _create_exchange(api_key, secret_key):
    return dev_ethfinex_api(config={
        "apiKey": api_key,
        "secret": secret_key
    })


def _convert_to_usd(tickers, currency, amount):
    if currency == 'BTC':  # TODO: we support only USDT market, remove on production
        eth_btc_price = tickers['ETH/BTC']['last']
        eth_usdt_price = tickers['ETH/USDT']['last']
        return (amount / eth_btc_price) * eth_usdt_price
    return tickers[currency + '/USDT']['last'] * amount


class ExternalExchange:
    def __init__(self,
                 api_key='8OX5G23ptQMdgLZteOCFyS5WCWkNCCIoOOLGVf8x1J6',
                 secret_key='CpfLsJjVVqFoTEFLeNJkKkvCIN6wB4yWCy0F9BNutvX"'):
        self.exchange = _create_exchange(api_key, secret_key)

    def _make_market_order(self,
                           currency_pair,
                           amount,
                           side):
        print("Placing market order " + str(currency_pair) + ", amount = " + str(amount) + ", side = " + side)
        response = self.exchange.create_order(
            symbol=currency_pair,
            type='market',
            side=side,
            amount=amount
        )
        order_id = response['info']['id']

        max_attempts = 15
        while max_attempts > 0:
            order = self.exchange.fetch_order(order_id)
            is_closed = order['status'] == 'closed'
            if is_closed:
                avg_execution_price = order['info']['avg_execution_price']
                return avg_execution_price
            time.sleep(0.5)
            max_attempts -= 1

        # Error ¯\_(ツ)_/¯
        return 300

    def _batch_market_order(self,
                            orders,
                            side):
        # TODO: make it in parallel
        for order in orders:
            self._make_market_order(order['currency'], order['amount'], side)

    # {
    #   "ETH": 14,
    #   "USDT": 298.402
    # }
    def get_user_wallets(self):
        balances = self.exchange.fetch_balance()
        return balances['free']

    # {
    #   "average_execution_price": 300,
    # }
    def market_order_buy(self,
                         currency_pair,  # for example ETH/USDT
                         amount):
        return self._make_market_order(currency_pair, amount, 'buy')

    # {
    #   "average_execution_price": 300,
    # }
    def market_order_sell(self,
                          currency_pair,
                          amount):
        return self._make_market_order(currency_pair, amount, 'sell')

    # Pass array: [{'currency': 'ETH/USDT', amount: 1}, ...]
    def batch_market_buy(self, orders):
        self._batch_market_order(orders, 'buy')

    # Pass array: [{'currency': 'ETH/USDT', amount: 1}, ...]
    def batch_market_sell(self, orders):
        self._batch_market_order(orders, 'sell')

    def get_current_user_usd_balance(self):
        user_wallets = self.get_user_wallets()
        return self.get_usd_balance_from_wallets(user_wallets)

    def get_usd_balance_from_wallets(self, wallets):
        tickers = self.exchange.fetch_tickers()
        usdt_sum = 0
        for currency, amount in wallets.items():
            if currency == 'USDT':
                usdt_sum += amount
            else:
                usdt_sum += _convert_to_usd(tickers, currency, amount)
        return usdt_sum

    def get_current_rate_usd(self, currency, amount):
        tickers = self.exchange.fetch_tickers()
        return _convert_to_usd(tickers, currency, amount)
