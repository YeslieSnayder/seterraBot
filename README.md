# Table of content

- [Table of content](#table-of-content)
- [Description](#description)
   - [Seterra](#seterra)
   - [Game modes](#game-modes)
      - [Continents](#continents)
      - [Countries](#countries)
   - [Config](#config)
      - [Available languages](#available-languages)
- [Installation](#installation)
- [Contacts](#contacts)

# Description

This project is a bot for popular online game **Seterra**.

The bot starts a new window (**Chrome** browser) and waiting for a full-page load. After this, the bot restarts a timer and starts working until all entities are guessed.

You can start the game immediately after loading the game window.

After entities have been guessed, the bot will save the statistics and write them into the file `log/history.log`. After all, the user should press `Enter` in the console where (s)he started the program.

## Seterra

**Seterra Geography** - The Ultimate Map Quiz Site.

Become a geography expert and have fun at the same time! Seterra is an entertaining and educational geography game that gives you access to over 400 customizable quizzes.

Seterra will challenge you with quizzes about countries, capitals, flags, oceans, lakes, and more! Introduced in 1997 and available in more than 40 different languages, Seterra has helped thousands of people study geography and learn about their world.

Link: [https://online.seterra.com/en?img=1](https://online.seterra.com/en?img=1)

## Game modes

At the moment the bot supports only 2 game modes:

- World: Continents → [https://online.seterra.com/en/vgp/3004](https://online.seterra.com/en/vgp/3004)
- 150 Largest Countries By Area → [https://online.seterra.com/en/vgp/3198](https://online.seterra.com/en/vgp/3198)

### Continents

In this mode, the player should make a guess where is a **continent** located on World Map. There are 7 continents.

### Countries

In this mode, the player should make a guess where is a **country** located on World Map. There are 150 countries.

## Config

The SeterraBot has a **Config** file: `config.ini`. There is information about the paths to log, driver (in this case: ***Chrome driver***), and language. Be careful to change them.

### Available languages

- Russian: `ru` - By default
- English: `en`

# Installation

1. Clone repo: `git clone https://github.com/YeslieSnayder/seterraBot.git`
2. Append the project's path to `PYTHONPATH`:

    If you are using **Ubuntu** or another Linux distributive:

    ```bash
    export PYTHONPATH="${PYTHONPATH}:~/seterraBot/"
    ```

    If you are using **Windows** (Please, before running this command exchange the path `C:\path\to\the\project` to the current directory where project is located):

    ```bash
    set PYTHONPATH=%PYTHONPATH%:C:\path\to\the\project\seterraBot
    ```

3. Launch the bot: `python3 ./seterraBot`

# Contacts

If you have some problems/troubles ⇒ Please, create an issue with the description of your problem for this repository.

Also, you can support my project by creating a fork and make pull request. If you have estimable advice, then it will be merged to the main branch.