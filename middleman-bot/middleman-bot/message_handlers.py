from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, CallbackContext, CallbackQueryHandler, CallbackContext
from enum import IntEnum

from lift import Lift, LiftState, load_lifts, add_lift
from pathlib import Path


class ConversationState(IntEnum):
    NONE = 0
    PHOTO = 1
    SITE = 2
    OPENING = 3
    MESSAGE = 4
    PREVIEW = 5

def ready(context : CallbackContext):
    if (context.user_data['lift'].photo != None and
        context.user_data['conv_state'] == ConversationState.PREVIEW):
        return True
    else:
        print("not ready")
        return False

def combine(context : CallbackContext):
    id = context.user_data['lift'].id
    site = "Site: " + context.user_data['lift'].site
    opening = "Opening: " + context.user_data['lift'].opening
    note = "# " + context.user_data['lift'].note

    combine = "New Lift: " + str(id) + "\n" + site + "\n" + opening + '\n' + note

    print("COMBINED")

    return combine


def reply_test(update : Update, context : CallbackContext):
    update.message.reply_text("Test!")

    photo = context.bot_data['photo']
    update.message.reply_photo(photo)

def reply_text(update : Update, context : CallbackContext):
    if (context.user_data['conv_state'] == ConversationState.MESSAGE):
        update.message.reply_text("Nice message!")

        context.user_data['lift'].note = update.message.text
        context.user_data['conv_state'] = ConversationState.PREVIEW
    
    if (ready(context) == True):
        photo = context.user_data['lift'].photo
        update.message.reply_text("Preview:")
        update.message.reply_photo(photo, combine(context))

        keyboard = [[InlineKeyboardButton("Yes", callback_data = "send_lift"),
                    InlineKeyboardButton("No", callback_data = "cancel_lift")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Create lift?', reply_markup=reply_markup)

    else:
        update.message.reply_text("?")

def reply_photo(update : Update, context : CallbackContext):

    update.message.reply_text("New Lift Created!")

    template_lift = Lift(0, 'https://telegram.org/img/t_logo.png', LiftState.NONE, "S", "O", "None") 
    context.user_data['lift'] = template_lift

    # NEW
    id = context.bot_data['last_id'] + 1
    context.user_data['lift'].id = id

    photo = update.message.photo[-1]
    file_id = photo.file_id


    context.user_data['lift'].photo = photo


    new_file = context.bot.getFile(file_id)

    file_path = "photos/" + str(id) + ".jpg"
    new_file.download(Path(file_path))

    update.message.reply_text("Nice photo!")
    
    context.user_data['lift'].site = None
    context.user_data['lift'].opening = None
    context.user_data['lift'].note = None


    context.user_data['conv_state'] = ConversationState.SITE


def reply_site(update : Update, context : CallbackContext):
    context.user_data['lift'].site = update.message.text

    context.user_data['site_set'] = True

    update.message.reply_text("Nice site!")

    context.user_data['conv_state'] = ConversationState.OPENING

    #if (ready(context) == True):
    #    update.message.reply_text(combine(context))

def reply_opening(update : Update, context : CallbackContext):
    context.user_data['lift'].opening = update.message.text
    context.user_data['opening_set'] = True

    update.message.reply_text("Nice opening!")

    context.user_data['conv_state'] = ConversationState.MESSAGE
