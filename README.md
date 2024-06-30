A chat server in the development by me for a mobile messenger app.

Current functionality:
Working authentication proof of concept, sending and delivering messages to users, keeping active users in an "online pool" to deliver messsages instantly
and logging message in the database if the receiver user is not connected,
saving messages in DB.

Upcoming steps in the near future:
-  Switching to log(n) time search algorithm in online pool
-  Full paralellazation
-  Full duplex tcp usage
-  Full group chat support
