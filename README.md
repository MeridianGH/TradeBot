# TradeBot

![Last commit](https://img.shields.io/github/last-commit/meridianpy/tradebot.svg?color=green&label=Last%20commit) &nbsp;
![Pull Requests](https://img.shields.io/github/issues-pr-raw/meridianpy/tradebot.svg?color=yellow&label=Pull%20requests)  &nbsp;
![Issues](https://img.shields.io/github/issues-raw/meridianpy/tradebot.svg?color=red&label=Issues)

![Stars](https://img.shields.io/github/stars/meridianpy/tradebot.svg?style=social) &nbsp;
![Watchers](https://img.shields.io/github/watchers/meridianpy/tradebot.svg?label=Watchers&style=social) &nbsp;
![Followers](https://img.shields.io/github/followers/meridianpy.svg?label=Followers&style=social)

This is a Steam trading bot that operates with <abbr title="Team Fortress 2">TF2</abbr> items.
Currently it only trades with keys.
There are more items to come in the future.
Maybe also a system to trade every item if the price is in the bots favor.

Help
===
Since I just started learning Python this is my very first rather big project.
Therefore, there are many bad habits or bad code to find that could be improved.
[Contact me](mailto:meridianpy@gmail.com) if you find anything that I should know.
I greatly appreciate any feedback! :D

Functionality
===
* Logging in to Steam API
* Fetching trade offers
* Calculating <abbr title="Common selling price">CSP</abbr> and <abbr title="Common buying price">CBP</abbr> of <abbr title="Team Fortress 2">TF2</abbr> items
* Accepting / declining trade offers depending on offered / demanded currency
* more to come...

Disclaimers
===
* This project heavily relies on the Python library [steampy](https://github.com/bukson/steampy) by [bukson](https://github.com/bukson).
I want to thank [bukson](https://github.com/bukson) for providing this library, which without it this project would be completely impossible!

* I am also using the [steam](https://github.com/ValvePython/steam) library by [Rossen Georgiev](https://github.com/rossengeorgiev)
to access the chat in Steam. Thanks for providing this library!

* Also, the [backpack.tf](https://backpack.tf) website which provides the prices for items (currently only keys)
but without it I couldn't expand the bot's functionality.

* The [Steam Web API](https://developer.valvesoftware.com/wiki/Steam_Web_API) helps at dealing with trade offers and
using the Steam trading network