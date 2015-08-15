# myvodacom_stats

This is a pretty simple python module that allows a user to query their Vodacom balances via a command line.

Authentication is done via a MyVodacom account and all requests are via the Rest API that vodacom uses to back its MyVodacom website.

## How to use:
```
$ git clone <this git repo>
$ python setup.py install
$ vodacom-balances <email_address> <password> <phone numbers ...>
```

It is recommended that instead of using your password in plaintext (which will end up in your shell history), you should
rather put your password in a access restricted file and call the command in the following manner:

```
$ vodacom-balances <email_address> `cat <your password file>` <phone numbers ...>
```

A `--json` flag is available to receive the output as a indented json object in order to pass it to other applications.
A `--verbose` flag is available if you really want to see the DEBUG level logging.

## Sample output:

```
$ vodacom-balances myuser@example.com hunter2 0760123456 0826543210
0760123456
    Airtime
       Remaining: 7784 cents
    Messaging
       Remaining: 0 count
    Voice
       Remaining: 0 seconds
    Data
       Remaining: 1024 kilobytes
0826543210
    Airtime
       Remaining: 0 cents
    Messaging
       Remaining: 6 count
    Voice
       Remaining: 123 seconds
    Data
       Remaining: 0 kilobytes
```

```
$ vodacom-balances --json myuser@example.com hunter2 0760123456 0826543210
{
  "0760123456": {
    "Airtime": {
      "description": "Total of your prepaid airtime that can be used to make calls, buy bundles, pay for content subscriptions and billing reports, etc.",
      "remaining": 7784,
      "unit": "cents"
    },
    "Data": {
      "description": "Total of your data including recurring and once-off bundles. It can be used at any time except while roaming abroad.",
      "remaining": 1024,
      "unit": "kilobytes"
    },
    "Messaging": {
      "description": "Total of your SMSs including recurring and once-off bundles. These can be sent to any network at any time, within South Africa. Premium-rated and international SMSs are not included.",
      "remaining": 0,
      "unit": "count"
    },
    "Voice": {
      "description": "Total of your voice minutes including recurring and once-off bundles. It can be used to call any network within South Africa at any time, but cannot be used to call premium-rated and international numbers.",
      "remaining": 0,
      "unit": "seconds"
    }
  },
  "0826543210": {
    "Airtime": {
      "description": "Total of your prepaid airtime that can be used to make calls, buy bundles, pay for content subscriptions and billing reports, etc.",
      "remaining": 0,
      "unit": "cents"
    },
    "Data": {
      "description": "Total of your data including recurring and once-off bundles. It can be used at any time except while roaming abroad.",
      "remaining": 0,
      "unit": "kilobytes"
    },
    "Messaging": {
      "description": "Total of your SMSs including recurring and once-off bundles. These can be sent to any network at any time, within South Africa. Premium-rated and international SMSs are not included.",
      "remaining": 6,
      "unit": "count"
    },
    "Voice": {
      "description": "Total of your voice minutes including recurring and once-off bundles. It can be used to call any network within South Africa at any time, but cannot be used to call premium-rated and international numbers.",
      "remaining": 123,
      "unit": "seconds"
    }
  }
}
```
