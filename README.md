# Click 2 Call
This is an example of a  Click To Call application built using the Nexmo Voice API, you could embed the web form on your companies website and configure the applicaiton with your sales phon number, 

When customers want to talk to you they enter their name and number into the form and Nexmo will setup a call between you and the customer, firstly your number is called and the call is announced with the customers name then the customers number is called an you are connected.

You can test out your own copy of this right now on heroku by clicking this button.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/nexmo-community/click2call)

This will launch the heroku installer console, you will be asked to enter a name for your app (we need this twice) something like "CallFred" is good.
It will also ask you to enter your number where you want callers to be connected to, enter your number in internatonal format without the + eg `447790900123` 
It will also ask you for your nexmo API Key and Secret and finally it will ask you to enter a country where you would like to purchase a nexmo number, For this demo the number is only used for the Caller ID.
