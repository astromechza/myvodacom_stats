import logging
import requests
import urllib2

log = logging.getLogger(__name__)

LOGIN_URL = "https://myvodacom.secure.vodacom.co.za/rest/services/v1/context/loginUser/%s"
BUNDLE_BALANCES_URL = "https://myvodacom.secure.vodacom.co.za/rest/services/v1/bundlebalances/getbundlebalances"
CONTEXT_URL = "https://myvodacom.secure.vodacom.co.za/rest/services/v1/context/set/%s"


class MyVodacom(object):

    post_headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0",
        'Accept': "application/json, text/plain, */*",
        'Accept-Language': "en-US,en;q=0.5",
        'DNT': "1",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Referer': "https://myvodacom.secure.vodacom.co.za/vodacom/log-in?intendedURL=http%3A%2F%2Fmyvodacom."
                   "secure.vodacom.co.za%2Fvodacom%2Fmyvodacom%2Fmy-summary",
        'Pragma': "no-cache",
        'Cache-Control': "no-cache"
    }

    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.session = None

    def login(self):
        """
        Create a new active authenticated session by logging in with the
        credentials. This must be done before any other calls are made.
        :returns: self, for method chaining convenience
        """

        data = {
            'password': self.password,
            'mobile': "false",
            'referer': "https://myvodacom.secure.vodacom.co.za/vodacom/log-in",
            'currentUrl': "https://myvodacom.secure.vodacom.co.za/vodacom/log-in"
        }

        session = requests.Session()
        log.info("sending login request")
        r = session.post(LOGIN_URL % self.email_address, data=data, headers=self.post_headers)

        if r.status_code != 200:
            raise urllib2.HTTPError(r.request.url, r.status_code, "Login request failed.", {}, None)

        data = r.json()
        if not data['successfull']:
            error_messages = map(lambda m: m['message'], filter(lambda m: m['errorMessage'], data['messages']))
            raise ValueError("Login request failed. " + "; ".join(error_messages))

        self.session = session
        log.info("logged in.")
        return self

    def get_bundle_balances(self, phone_numbers):
        """
        Get the balances for each service type associated with each phone number.

        :return: nested dictionary. phone number -> services* -> name, description, remaining, unit
        """
        if self.session is None:
            raise Exception("Cannot get bundle balances without a valid login session. Please use login().")

        output = {}

        for phone_number in phone_numbers:
            log.info("switching context to %s.", phone_number)
            r = self.session.post(CONTEXT_URL % phone_number,
                                  data={"tracker": "numberDropdownMainTracker"}, headers=self.post_headers)
            if r.status_code != 200:
                raise urllib2.HTTPError(r.request.url, r.status_code, "Context switch request failed.", {}, None)

            log.info("getting bundle balances.")
            r = self.session.get(BUNDLE_BALANCES_URL)
            if r.status_code != 200:
                raise urllib2.HTTPError(r.request.url, r.status_code, "Bundle balances request failed.", {}, None)

            data = r.json()

            services = {}
            for service in data['bundleBalances'].get('serviceTypesList', []):
                services[service['name']] = {
                    'description': service['tooltip'],
                    'remaining': service['totalRemaining'],
                    'unit': service['unit'].lower()
                }
            output[phone_number] = services

        return output
