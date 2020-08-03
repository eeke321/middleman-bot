from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, CallbackContext, CallbackQueryHandler, CallbackContext, ConversationHandler
from enum import Enum, IntEnum

from lift import Lift, LiftState, load_lifts, add_lift
from pathlib import Path
from enums import BCD, UD, BD


class ConversationState(Enum):
    NONE = 0
    PHOTO = 1
    SITE = 2
    OPENING = 3
    NOTE = 4
    PREVIEW = 5

    EDIT_SHIPMENT = 6
    EDIT_SHIPMENT_LINK = 7

def ready(context : CallbackContext):
    if (context.user_data[UD.NEW_LIFT].photo != None):
        return True
    else:
        print("not ready")
        return False

def combine(context : CallbackContext):
    id = context.user_data[UD.NEW_LIFT].id
    site = "Site: " + context.user_data[UD.NEW_LIFT].site
    opening = "Opening: " + context.user_data[UD.NEW_LIFT].opening
    note = "# " + context.user_data[UD.NEW_LIFT].note

    combine = "New Lift: ST" + str(id) + "\n" + site + "\n" + opening + '\n' + note

    print("COMBINED")

    return combine

def reply_user(update : Update, context : CallbackContext):
    new_user = update.message.text

    item_id = context.user_data[UD.SHIPMENT_ID] + 1

    lift = context.bot_data[BD.LIFT_LIST][item_id]

    lift.users.append(new_user)

    keyboard = [[InlineKeyboardButton("End Linking", callback_data = BCD.REPLY_USER_END_LINK.name)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Linked user: " + new_user, reply_markup = reply_markup)

    return ConversationState.EDIT_SHIPMENT_LINK

def reply_lift(update : Update, context : CallbackContext):
        l = len(update.message.text)
        st_id = update.message.text[2:l]

        file_path = "A:\photos/" + str(st_id) + ".jpg"
        photo = open(Path(file_path), 'rb')

        update.message.reply_photo(photo)

        context.user_data[UD.SHIPMENT_ID] = int(st_id)



        keyboard = [[InlineKeyboardButton("Update State", callback_data = BCD.REPLY_LIFT_UPDATE_STATE.name),
                    InlineKeyboardButton("Delete", callback_data = BCD.REPLY_LIFT_DELETE.name),
                    InlineKeyboardButton("Add Links", callback_data = BCD.REPLT_LIFT_ADD_LINKS.name)]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("Modify Lift: " + update.message.text, reply_markup=reply_markup)

        return ConversationState.EDIT_SHIPMENT

def reply_test(update : Update, context : CallbackContext):
    update.message.reply_text("Test!")

    photo = context.bot_data['photo']
    update.message.reply_photo(photo)

def reply_note(update : Update, context : CallbackContext):

    context.user_data[UD.NEW_LIFT].note = update.message.text

    if (ready(context) == True):
        photo = context.user_data[UD.NEW_LIFT].photo
        update.message.reply_text("Preview:")
        update.message.reply_photo(photo, combine(context))

        keyboard = [[InlineKeyboardButton("Yes", callback_data = BCD.REPLY_SEND_LIFT.name),
                    InlineKeyboardButton("No", callback_data = BCD.REPLY_CANCEL_LIFT.name)]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Create lift?', reply_markup=reply_markup)

    return ConversationState.PREVIEW


def reply_text_default(update : Update, context : CallbackContext):
        update.message.reply_text("?")

        print("Test Print:")
        print("message id: ", update.message.message_id)
        print("chat id: ", update.message.chat.id)

def reply_photo(update : Update, context : CallbackContext):

    update.message.reply_text("New Lift Created!")

    template_lift = Lift(0, 'https://telegram.org/img/t_logo.png', LiftState.NONE, "S", "O", "None") 
    context.user_data[UD.NEW_LIFT] = template_lift

    # NEW
    id = context.bot_data[BD.LAST_ID] + 1
    context.user_data[UD.NEW_LIFT].id = id

    photo = update.message.photo[-1]
    file_id = photo.file_id


    context.user_data[UD.NEW_LIFT].photo = photo


    new_file = context.bot.getFile(file_id)

    file_path = "A:\photos/" + str(id) + ".jpg"
    new_file.download(Path(file_path))

    update.message.reply_text("Which site?")
    
    context.user_data[UD.NEW_LIFT].site = None
    context.user_data[UD.NEW_LIFT].opening = None
    context.user_data[UD.NEW_LIFT].note = None


    return ConversationState.SITE

def reply_site(update : Update, context : CallbackContext):
    context.user_data[UD.NEW_LIFT].site = update.message.text


    update.message.reply_text("Which opening?")


    return ConversationState.OPENING

def reply_opening(update : Update, context : CallbackContext):
    context.user_data[UD.NEW_LIFT].opening = update.message.text

    update.message.reply_text("Type note:")


    return ConversationState.NOTE
