from ccxt import ethfinex


class dev_ethfinex_api(ethfinex):
    def describe(self):
        return self.deep_extend(super(ethfinex, self).describe(), {
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/37555526-7018a77c-29f9-11e8-8835-8e415c038a18.jpg',
                'api': 'https://hackathon.ethfinex.com',
                'www': 'https://www.ethfinex.com',
                'doc': [
                    'https://bitfinex.readme.io/v1/docs',
                    'https://github.com/bitfinexcom/bitfinex-api-node',
                    'https://www.ethfinex.com/api_docs',
                ],
            },
        })
