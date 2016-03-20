# Superhero Twitter Bot
The purpose of this app is to create a Twitter Bot that generates random superhero names to users that tweet it. The Twitter account linked to this bot will be a 'Superhero Club'.


###The bot responds to a user in one of two ways: 
1. On first tweet to bot, bot assigns random superhero name to user and welcomes them to the club.
2. On all additional tweets to bot, bot responds to user by their superhero name as assigned on first tweet.

The bot stores Twitter user ids, as well as superhero names in an SQL database.

###All superhero names are comprised of:
1. A title (selected randomly from a list of titles).
2. An adjective (selected at random using Wordnik API).
3. A noun (selected at random using Wordnik API).

The app will be deployed using Heroku.
