from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputTextMessageContent
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
    EDIT_SHIPMENT_PING = 8

    FOLLOW_SITE = 9

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
    from_user = "- " + context.user_data[UD.NEW_LIFT].from_user

    combine = "- New Lift: ST" + str(id) + " -\n" + site + "\n" + opening + '\n' + note + '\n' + from_user

    print("COMBINED")

    return combine

def follow_site(update : Update, context : CallbackContext):
    print("FOLLOW")

    site = update.message.text

    context.user_data[UD.FOLLOW_SITE] = site

    keyboard = [[InlineKeyboardButton("Follow " + u'\U0001F91D', callback_data = BCD.FOLLOW_SITE_YES.name)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Site: " + site, reply_markup = reply_markup)

    return ConversationState.FOLLOW_SITE

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
                    InlineKeyboardButton("Ping! " + u'\U0001F6CE', callback_data = BCD.REPLY_LIFT_PING.name),
                    InlineKeyboardButton("Users", callback_data = BCD.REPLY_LIFT_ADD_LINKS.name)],
                    
                    [InlineKeyboardButton("Follow " + u'\U0001F91D', callback_data = BCD.REPLY_LIFT_FOLLOW.name)]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("Modify Lift: " + update.message.text, reply_markup=reply_markup)

        return ConversationState.EDIT_SHIPMENT

def reply_test(update : Update, context : CallbackContext):
    print("Test Print:")
    print("message id: ", update.message.message_id)
    print("chat id: ", update.message.chat.id)

    sender = update.message.from_user
    mention = sender.text_markdown_v2(name = "TEST")

    text = InputTextMessageContent(message_text = mention, parse_mode = 'MarkdownV2')

    update.message.reply_text(text)


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
        print(update.message.text)
        #print("Test Print:")
        #print("message id: ", update.message.message_id)
        #print("chat id: ", update.message.chat.id)

def reply_photo(update : Update, context : CallbackContext):

    update.message.reply_text("New Lift Created!")

    template_lift = Lift(0, 'https://telegram.org/img/t_logo.png', LiftState.NONE, "S", "O", "None") 
    context.user_data[UD.NEW_LIFT] = template_lift

    # NEW
    id = context.bot_data[BD.LAST_ID] + 1
    context.user_data[UD.NEW_LIFT].id = id

    context.user_data[UD.NEW_LIFT].from_user = update.message.from_user.name

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
