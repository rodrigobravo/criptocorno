from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import json
import urllib.request

from conf.settings import TELEGRAM_TOKEN
from conf.urls import BASE_API_URL, BASE_PRODUCTS_URL


def start(update, context):
    response_message = "=^._.^="
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message
    )


def http_cats(update, context):
    context.bot.sendPhoto(
        chat_id=update.effective_chat.id, photo=BASE_API_URL + context.args[0]
    )


def bitcoin_base(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=get_coin_data(context.args[0], context.args[1])
    )


def list_coins(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=get_main_list()
    )


def unknown(update, context):
    response_message = "Meow? =^._.^="
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message
    )


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("http", http_cats))
    dispatcher.add_handler(CommandHandler("cotacao", bitcoin_base))
    dispatcher.add_handler(CommandHandler("list", list_coins))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()

    updater.idle()


def get_main_list():
    url = BASE_PRODUCTS_URL
    data = urllib.request.urlopen(url).read().decode()

    obj = json.loads(data)
    result = []
    for coin in obj:
        result.append(coin['display_name'])

    return result


def get_coin_data(coin, share):
    url = BASE_PRODUCTS_URL + coin + "-" + share + "/ticker"
    data = urllib.request.urlopen(url).read().decode()

    # parse json object
    obj = json.loads(data)
    result = coin.upper() + " PRICE: " + "(" + share.upper() + ")" + ('$ ' + obj['price'])

    return result


if __name__ == "__main__":
    print("press CTRL + C to cancel.")
    main()