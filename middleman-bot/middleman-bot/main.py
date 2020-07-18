
# MORJES TÄSSÄ MUN MUUTOS
# LIT 

""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

import os
print(os.getcwd())

import openpyxl
wb = openpyxl.load_workbook('file.xlsx')


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')




def ready(context):
    if (context.user_data['photo'] != None and
        context.user_data['site'] != None and
        context.user_data['opening'] != None):
        return True
    else:
        return False

def combine(context):
    site = "To site: " + context.user_data['site']
    opening = "From opening: " + context.user_data['opening']

    combine = "New Lift: \n" + site + "\n" + opening

    print("COMBINED")

    context.user_data['site'] = None
    context.user_data['opening'] = None

    return combine

def echo_text(update, context):
    update.message.reply_text('?')
    print("message id: ", update.message.message_id)
    print("chat id: ", update.message.chat.id)

def reply_pic(update, context):
    context.user_data['photo'] = update.message.photo[-1]
    update.message.reply_text("Nice photo!")

    context.user_data['site'] = None
    context.user_data['opening'] = None


def reply_site(update, context):
    context.user_data['site'] = update.message.text
    context.user_data['site_set'] = True

    update.message.reply_text("Nice site!")

    #if (ready(context) == True):
    #    update.message.reply_text(combine(context))

def reply_opening(update, context):
    context.user_data['opening'] = update.message.text
    context.user_data['opening_set'] = True

    update.message.reply_text("Nice opening!")

    if (ready(context) == True):
        photo = context.user_data['photo']
        update.message.reply_photo(photo, combine(context))

def main():
    
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1182411075:AAGsO0gh6609YJTeGa09CBRAZePXm6m5Ivo", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    print(wb.sheetnames)

    site_code_sheet = wb['sites']
    opening_code_sheet = wb['openings']

    i = 0
    sites = []
    openings = []

    """Initialize"""

    # Todo: Multiple loops
    while True:
        i += 1
        # Get value from sheet cell
        site_code = site_code_sheet.cell(row = i, column = 1).value
        opening_code = opening_code_sheet.cell(row = i, column = 1).value

        # If all cells empty
        if (site_code == None and opening_code == None):
            break

        # Add value to list
        if (site_code != None):
            sites.append(site_code)
        if (opening_code != None):
            openings.append(opening_code)


    print(sites)
    print(openings)

    dp.add_handler(MessageHandler(Filters.photo, reply_pic))
    dp.add_handler(MessageHandler(Filters.text(sites), reply_site))
    dp.add_handler(MessageHandler(Filters.text(openings), reply_opening))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo_text))



    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == '__main__':
    main()
