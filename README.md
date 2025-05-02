# Telegram Bot - Fshare Direct Link Generator

This Telegram bot fetches direct download links from Fshare URLs.

## Features

*   Retrieves direct download links for Fshare files.
*   Restricts usage to an authorized Telegram user ID.
*   Loads configuration from environment variables.

## Prerequisites

*   Python 3.7+
*   pip (Python package installer)
*   An Fshare account
*   A Telegram Bot Token

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/huythedev/telegram_bot_get_direct-link_fshare.git
    cd telegram_bot_get_direct-link_fshare
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Rename the `.env_example` file to `.env`:
    ```bash
    # On Windows
    rename .env_example .env
    # On macOS/Linux
    mv .env_example .env
    ```
2.  Edit the `.env` file and fill in your details:
    *   `BOT_TOKEN`: Your Telegram Bot token obtained from BotFather.
    *   `AUTHORIZED_USER_ID`: Your Telegram User ID. You can get this from bots like `@userinfobot`.
    *   `FSHARE_USERNAME`: Your Fshare account email.
    *   `FSHARE_PASSWORD`: Your Fshare account password.
    *   `API_KEY`: Your Fshare API Key (obtainable from Fshare developer settings if available, or use a default/provided one if applicable).
    *   `ARIA2_RPC_URL` (Optional): URL for your Aria2 JSON-RPC endpoint if you intend to integrate Aria2 downloads (e.g., `http://localhost:6800/jsonrpc`).
    *   `ARIA2_SECRET` (Optional): Secret token for your Aria2 RPC if required.
    *   `SAVE_DIR` (Optional): Default directory where Aria2 should save downloads.
    *   `CUSTOM_STORAGE_URL` (Optional): Base URL for a custom storage solution if used.

**Important:** Keep your `.env` file secure and **do not** commit it to version control. The included `.gitignore` file should prevent this.

## Usage

1.  Run the bot:
    ```bash
    python bot.py
    ```
2.  Open Telegram and send an Fshare URL to your bot.
3.  The bot will reply with the direct download link if successful.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License

[Specify your license here, e.g., MIT License]
