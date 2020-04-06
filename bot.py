#Importing needed libraries
import telebot
import emoji

from keyboards import *
from functions import *

token = '1027166109:AAH-VqLwJLRNfbPegg3hqFjdxrI6z0z4oGU'

bot = telebot.TeleBot(token, threaded=True)


@bot.message_handler(commands=['start'])
def start(msg):
    """
    Starting ROIPartyBot
    """
    user = get_or_create_user(msg)
    keyboard = main_menu()

    bot.send_message(
        user.id,
        emoji.emojize(
            """
    :circus_tent: Hello {0}, Welcome to ROI Party Bot  :circus_tent:
            """.format(msg.from_user.name),
            use_aliases=True,
        ),
        reply_markup=keyboard
    )



@bot.message_handler(regexp='^Balance')
def balance(msg):
    "Returns Balance"
    user = get_or_create_user(msg)

    bot.send_message(
        user.id,
        """
    Your Account Balance:

    {0} BTC
    {1} XRP
        """.format(float(user.btc_balance), float(user.xrp_balance))
    )



@bot.message_handler(regexp='^Deposit')
def deposit(msg):
    "Deposit Function"
    user = get_or_create_user(msg)
    keyboard = deposit_keyboard()

    bot.send_message(
        user.id,
        "Please Select A Currency",
        reply_markup=keyboard,
    )



@bot.message_handler(regexp='^Withdraw')
def withdraw(msg):
    "Withdraw Functions"
    user = get_or_create_user(msg)
    keyboard = withdraw_keyboard()

    bot.send_message(
        user.id,
        "Please Select Balance To Withdraw From",
        reply_markup=keyboard,
    )


def btc_withdraw1(user):
    "Ask How much To Withdraw"
    question = bot.send_message(
        user.id,
        "How much do you wish to withdraw from your available balance?",
    )
    bot.register_next_step_handler(question, btc_withdraw2)


def btc_withdraw2(msg):
    """
    Checks user available balance and reuqest if available balance enough to make payment
    """
    amount = float(msg.text)
    user = get_or_create_user(msg)

    if float(user.balance) >= amount:
        bot.send_message(
            user.id,
            emoji.emojize(
                """
        :hourglass_flowing_sand: Processin Payment, you will be notified shortly. :hourglass:
                """,
                use_aliases = True,
            )
        )

    else:
        bot.send_message(
            user.id,
            emoji.emojize(
                """
        :warning: Insufficient balance. Give it another shot after checking your balance.
                """,
                use_aliases=True,
            ),
        )
    



@bot.message_handler(regexp='^Invest')
def invest(msg):
    """
    Return Balance
    """
    user = get_or_create_user(msg)
    keyboard = invest_keyboard()

    bot.send_message(
        user.id,
        "Please Select A Currency",
        reply_markup=keyboard,
    )




@bot.message_handler(regexp='^Help')
def help(msg):
    """
    Return Help Information
    """
    bot.send_message(
        msg.from_user.id,
        "Please call your mother for help. haha",
    )




# Callback Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    """
    Button Response
    """
    user = get_or_create_user(call)
    
    # BTC DEPOSIT
    if call.data == "1":
        bot.send_message(
            user.id,
            "Send Your Bitcoin to this address --> adkjandkjandkahsdajsbdjasdh",
        )

    # XRP DEPOSIT
    elif call.data == "2":
        bot.send_message(
            user.id,
            "Send Your Ripplecoin to this address --> jdfnhjfhjdfbjdbfjdfhdfjh",
        )

    # BTC WITHDRAW REQUEST
    elif call.data == "3":
        btc_withdraw1(user)

    # XRP WITHDRAW REQUEST
    elif call.data == "4":
        # xrp_withdraw1(user)
        pass


print("bot polling...")
bot.polling(none_stop=True)