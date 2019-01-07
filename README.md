# BBreaker!

## First version finished!!! :)

A brick breaker game in Python. There are multiple bricks with numbers written on them. The goal is to destroy the bricks by hitting them exactly the same amount of times as the number on each brick indicates. Luckily, there are multiple balls to use each round, but remember... each round the bricks go down and new ones are being created...
Let's see how long you are going to stand up! Good luck!

## Getting Started & Installing

### For playing

* go to [releases](https://github.com/harper25/BBreaker/releases) and download a last release, compatible with your OS
* create a virtual environment for the game (ex. `virtualenv .venv`) and activate it
* run `pip install <last-release-name>`
* run `python -m bbreaker`
* have fun!

### For development

The project was developed with [Poetry](https://poetry.eustace.io/). Therefore you have to:

* install Poetry: [GitHub](https://github.com/sdispater/poetry)
* git clone the repository
* create a virtual environment for development (ex. `virtualenv .venv`) and activate it
* cd to main folder and run: `poetry update` to get all dependencies from `pyproject.toml` installed to your virtual environment
* run `python -m bbreaker`
* modify and have fun!

The project uses common Python packages. No special prerequisites required.

## Tests

No tests yet!

## Built With

* [Poetry] - Dependency Management

## Contributing

Please, create pull requests in order to contribute.

## Authors

* [harper25](https://github.com/harper25)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Thanks to:

* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2) for a Readme template
* [Dillinger](https://dillinger.io/) for markdown online editor
* [BBTAN](http://www.111percent.net/) for inspiration

### Todos

* add a line of shot
* add bonuses
* write tests

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[Poetry]: <https://poetry.eustace.io/>
