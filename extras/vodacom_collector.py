
import diamond.collector
from myvodacom_stats.myvodacom import MyVodacom

"""
It would be very useful to be able to graph the balances over time.

For this reason, this file contains a implementation of a diamond collector that
will get the balances and log them to a diamond/carbon/graphite setup.

For more info see: https://github.com/BrightcoveOS/Diamond/wiki/CustomCollectors
"""


class MyVodacomCollector(diamond.collector.Collector):

    def get_default_config(self):
        config = super(MyVodacomCollector, self).get_default_config()
        config.update({
            'email_address': '',
            'password': '',
            'phone_numbers': []
        })
        return config

    def collect(self):
        if self.config.get('enabled', False):
            email = self.config.get('email_address', '').strip()
            password = self.config.get('password', '').strip()
            if email and password:
                phone_numbers = self.config.get('phone_numbers', [])
                if isinstance(phone_numbers, basestring):
                    phone_numbers = map(lambda pn: pn.strip(), phone_numbers.split(','))
                    phone_numbers = filter(lambda pn: len(pn) > 0, phone_numbers)

                data = MyVodacom(email, password).get_bundle_balances(phone_numbers)

                for number, services in data.items():
                    for service, details in services:
                        name = "%s.%s.remaining" % (number, service)
                        self.publish_gauge(name, float(details['remaining']))

                return True
            else:
                self.log.error("No email or password configured")
        return None