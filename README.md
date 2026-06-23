# shop-bot-telegram

A modular and asynchronous Telegram bot built with Python and `aiogram` 3.x. This project serves as a dynamic product catalog with a dedicated, secure administration panel for inventory management. 

## Features

### 👤 User Features
* **Interactive Catalog:** Users can browse available products using dynamically generated inline keyboards.
* **Detailed Product View:** Displays product names, high-quality images, descriptions, and pricing (in TMT).
* **Intuitive Navigation:** Simple commands (`/start`, `/check_catalog`) and seamless callback queries for a smooth user experience.

### 🛡️ Admin Features (Secured by Telegram User ID)
* **Add Products (FSM):** A step-by-step Finite State Machine guides the admin through adding a new item (Name ➡️ Photo ➡️ Description ➡️ Price).
* **On-the-Fly Editing:** "Back" buttons at each step allow the admin to correct mistakes before saving the product.
* **Input Validation:** Prevents admins from accidentally sending text when a photo is required, or text when a numerical price is required.
* **Delete Products:** Admins can view the catalog and selectively delete items with a built-in safety confirmation step (✅ Yes delete / ❌ Cancel).

## Setup and Installation

1. Clone the repository:

Bash
git clone [https://github.com/oxide5/shop-bot-telegram.git](https://github.com/oxide5/shop-bot-telegram.git)
cd shop-bot-telegram

2. Create a virtual environment and install dependencies:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
3. Configure Environment Variables:
Create a .env file in the root directory and add your specific credentials:

BOT_TOKEN=your_telegram_bot_token_here
ADMIN_ID=your_personal_telegram_id
4. Run the bot:

Bash
python main.py

## Usage
Standard Users: Send /start to greet the bot and /check_catalog to pull up the dynamic inline menu of all available products.

Administrators: Send /admin from the authorized account (matching the ADMIN_ID in .env). This will unlock the custom reply keyboard to "Add item" or "Delete item".

## Project Structure

The bot is designed with modularity in mind, separating user and admin routing:

```text
├── admin_private.py      # Admin panel logic, FSM states, and secure routes
├── user_private.py       # User-facing commands and catalog browsing
├── database/
│   └── engine.py         # Database operations (get, save, delete products)
├── kbds/
│   └── reply.py          # Static reply keyboards and builders
├── .env                  # Environment variables (Token, Admin ID)
└── main.py               # Entry point for the bot (not included in snippets)

