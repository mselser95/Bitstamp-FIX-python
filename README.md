# Bitstamp Fix Connector

This repository is an example of a FIX connnector with Bitstamp. It connects vía fix API to the exchange to get real time market data and send orders. 

## Install

    pip install requirements.txt
    
or 

    pip3 install requirements.txt
    

After installing requirements, you will need strunnel since Bitstamp requires SSL conection and the quickfix API does not implement this functionality in Python. To install stunnel:
    
    apt-get install stunnel4
    
## Run

### Code

To run this example, you will need to do some things. First of all, you will have to request access to the fix interface in Bitstamp. To do this, you need to open a ticket with support indicating that you want to use FIX protocol. You will need to send them your IP address and your API key. This process may take a couple of days to complete.

Afterwards, you need to modify some lines in the code.

In config/config.cfg:

    [DEFAULT]
    ...
    DataDictionary="YOUR PATH TO THE DATA DICTIONARY"
    ...
    
    [SESSION]
    ...
    SenderCompID="YOUR USERNAME ID"
    ...
    AppataDictionary="YOUR PATH TO THE DATA DICTIONARY"
    ...

I copied data dictionaries in connector/spec, so you should replace that with
    
    [PATH_TO_PROJECT]/connector/spec/FIX44.xml

SenderCompID is the username BITSTAMP assigns you when you register.

In connector/fixconnector.py:

    def toAdmin(self, message, sessionID):
        username = fix.Username("YOUR API KEY")
        mypass = fix.Password("YOUR API SECRET")

and in classes/brain.py:

    def __init__(self):
        ...
        self.trading_client = bitstamp.client.Trading(
        username = 'YOUR USERNAME ID', key = 'YOUT API KEY', secret = 'YOUR API SECRET')

You have to replace your API KEY, API SECRET and USERNAME ID

### Stunnel

To init the SSL connection, you should run 
    
    cd [PATH_TO_PROJECT]/config
    sudo stunnel stunnel_config.conf
    
This will initiate the SSL tunnel between your instance and BITSTAMP. If the initialization fails, try changing the 
    
    accept=8880
    
To a different port but make sure to update it in the config.cfg too.

### Python

Finally, to run the code:

    python3 main.py config/config.cfg 
    

Any contribution is welcome to improve this connector.