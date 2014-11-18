Check Floating License Expiration
=================================

Overview
--------

Nagios plugin that monitors floating licenses and warns you when they are about to expire. My default it warns you 45 days in advance.

### License Managers Supported

#### FlexNet (formerly FlexLM)

User must obtain lmutil from www.macrovision.com

Installation
------------

Usage
-----

usage: check_floating_license_expiration.py [-h] [-p PORT] [-s SERVER]
                                            [-f FEATURE] [-t THRESHOLD]
                                            [-m LICENSE_MANAGER] [-v VERBOSE]

Test a Seat license feature for expiration

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  The port the license deamon is running on.
  -s SERVER, --server SERVER
                        The ip address or name of the license server.
  -f FEATURE, --feature FEATURE
                        The Name of the feature you are checking for
                        expiration
  -t THRESHOLD, --threshold THRESHOLD
                        The Number of days before a warning state should
  -m LICENSE_MANAGER, --license_manager LICENSE_MANAGER
                        name of license manger the vendor is using
  -v VERBOSE, --verbose VERBOSE
                        Increaser verbosity

