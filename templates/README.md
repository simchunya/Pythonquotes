# Pythonquotes

Is a simple message board where users can post quotes from any of Monty Python shows. 

I intentionally left out the feature to create an account so as to do away with the hassle of the user creating and authenticating his account just to use the message board. The intention of this projectis to give some short lived fun for every user. Security wise, should it be used for neferious reasons, an ip logger keeps track of every entry which may be handed over to the authorities should it be required.

This web application uses flask, sessions, form verifier (wtforms), sql databases, identifies user's ip address and location.

The user starts off in the bridgekeeper scene where a random is employed to give 3 possible bridgekeeper encounters as per the show(sir lancelot,sir robin and King Arthur) (whatever answer sir robin gives results in his death as Assyria has 2 capitals depending on which time. Also in the show he falls to his death to great comedic value.)

All the responses given in the form are used later in the message board where they get posted alongside the quote the user posted.

All users may only update or delete their quote. This feature is implemented through sessions so once they lose their session, they may not edit it any longer.

As i did away with the traditional login method, an admin may delete but not update any of the quotes by giving the correct combination of a name and quest.