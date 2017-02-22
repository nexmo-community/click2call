# Click 2 Call
This is an example of a  Click To Call application built using the Nexmo Voice API, you could embed the web form on your companies website and configure the applicaiton with your sales phon number, 

When customers want to talk to you they enter their name and number into the form and Nexmo will setup a call between you and the customer, firstly your number is called and the call is announced with the customers name then the customers number is called an you are connected.

You can test out your own copy of this right now on heroku by clicking this button.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/nexmo-community/click2call)

You will then be asked for a few parameters, and once you know the hostname (eg `example.herokuapp.com`) of your application you will need to create a Nexmo Application using the Nexmo CLI

`nexmo app:create "My Click to Call Demo" "https://YOUR-HOSTNAME/ncco" "https://YOUR-HOSTNAME/event"`

