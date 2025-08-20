# Discord Bot Project

## Overview
This project is a Discord bot designed to manage matches, tournaments, and leagues. It features interactive panel generators with multi-language support, allowing users to register, create teams, join matches, view ongoing matches, tournaments, or leagues, check their statistics, and modify their profiles.

## Project Structure
The project is organized into several modules, each responsible for different functionalities:

- **src/bot**: Contains the main bot logic and event handling.
- **src/commands**: Houses command files for managing matches, tournaments, leagues, teams, statistics, and user profiles.
- **src/database**: Manages database connections, models, and migrations.
- **src/logic**: Implements the core logic for matches, tournaments, and leagues.
- **src/panels**: Generates interactive panels and modals for user interaction.
- **src/utils**: Provides utility functions for localization, validation, and other helper tasks.
- **src/config**: Contains configuration settings for the bot.

## Features
- **Multi-language Support**: The bot supports multiple languages through JSON files for modals.
- **User Interaction**: Users can register, create teams, join matches, and view statistics.
- **Tournament and League Management**: The bot includes systems for managing tournaments, scrims, and leagues.
- **Database Integration**: All data is stored in a database, allowing for persistent storage and retrieval of information.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd discord-bot-project
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration
- Create a `.env` file based on the `.env.example` file provided, and fill in the necessary environment variables.

## Running the Bot
To start the bot, run the following command:
```
python src/bot/main.py
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.