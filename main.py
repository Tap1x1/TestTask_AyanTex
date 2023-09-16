import multiprocessing
from bot.telegram_bot import main as run_telegram_bot
from server.app import app

if __name__ == "__main__":
    bot_thread = multiprocessing.Process(target=run_telegram_bot)
    bot_thread.start()

    app.run(host='0.0.0.0', port=5000)
