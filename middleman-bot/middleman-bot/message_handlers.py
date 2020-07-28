from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, CallbackContext, CallbackQueryHandler, CallbackContext, ConversationHandler
from enum import Enum, IntEnum

from lift import Lift, LiftState, load_lifts, add_lift
from pathlib import Path
from enums import BCD


class ConversationState(Enum):
    NONE = 0
    PHOTO = 1
    SITE = 2
    OPENING = 3
    NOTE = 4
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

    combine = "New Lift: ST" + str(id) + "\n" + site + "\n" + opening + '\n' + note

    print("COMBINED")

    return combine

def reply_lift(update : Update, context : CallbackContext):
        photo = 'https://telegram.org/img/t_logo.png'
        update.message.reply_photo(photo)

        keyboard = [[InlineKeyboardButton("Update State", callback_data = BCD.REPLY_LIFT_UPDATE_STATE.name),
                    InlineKeyboardButton("Delete", callback_data = BCD.REPLY_LIFT_DELETE.name),
                    InlineKeyboardButton("Link", callback_data = BCD.REPLT_LIFT_LINK.name)]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Modify Lift: " + update.message.text, reply_markup=reply_markup)

        return ConversationState.NONE

def reply_test(update : Update, context : CallbackContext):
    update.message.reply_text("Test!")

    photo = context.bot_data['photo']
    update.message.reply_photo(photo)

def reply_note(update : Update, context : CallbackContext):
    update.message.reply_text("Nice note!")

    context.user_data['lift'].note = update.message.text
    context.user_data['conv_state'] = ConversationState.PREVIEW

    if (ready(context) == True):
        photo = context.user_data['lift'].photo
        update.message.reply_text("Preview:")
        update.message.reply_photo(photo, combine(context))

        keyboard = [[InlineKeyboardButton("Yes", callback_data = BCD.REPLY_SEND_LIFT.name),
                    InlineKeyboardButton("No", callback_data = BCD.REPLY_CANCEL_LIFT.name)]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Create lift?', reply_markup=reply_markup)

    return ConversationState.PREVIEW


def reply_text(update : Update, context : CallbackContext):
        update.message.reply_text("?")

        return ConversationState.NONE

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

    update.message.reply_text("Which site?")
    
    context.user_data['lift'].site = None
    context.user_data['lift'].opening = None
    context.user_data['lift'].note = None


    context.user_data['conv_state'] = ConversationState.SITE

    return ConversationState.SITE


def reply_site(update : Update, context : CallbackContext):
    context.user_data['lift'].site = update.message.text

    context.user_data['site_set'] = True

    update.message.reply_text("Which opening?")

    context.user_data['conv_state'] = ConversationState.OPENING

    return ConversationState.OPENING

def reply_opening(update : Update, context : CallbackContext):
    context.user_data['lift'].opening = update.message.text
    context.user_data['opening_set'] = True

    update.message.reply_text("Type message:")

    context.user_data['conv_state'] = ConversationState.NOTE

    return ConversationState.NOTE
