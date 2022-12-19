# jim

![GitHub](https://img.shields.io/github/license/jibstack64/jim)
![Coolness](https://img.shields.io/badge/coolness-100%25-yellowgreen)

A calorie and weight logger I made for my personal gymventures.

Not meant to be used seriously - use an online service, or something (no, seriously, I made this in half an hour).

### Arguments
- `help` -> duh.
- `log {calories} [weight (kg)]` -> associates the current date and time with the calorie count and weight provided.
- `read` -> displays all past data in a pretty format.
- `reset` -> resets all data

### Install
If you're on *nix (preferably Linux) you can `chmod +x` the `jim.sh` script and create a link to it in your `.local/bin` or other location. I also recommend that you create a `~/.jim` directory and move the contents of the cloned `jim` folder there. It just means that you don't have a random `jim` folder in your machine.

Otherwise, you will have to just use a normal directory somewhere in your `Documents`.
