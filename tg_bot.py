import logging
from data import db_session
from data.users import User
from werkzeug.security import check_password_hash
from data.news import NewsForm, News
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

token = '5956782574:AAGBRdrCmAfLbC7yX_ALdeR4ucMCLU6NuNM'


async def start(update, context, first=True):
    user = update.effective_user

    await update.message.reply_html(
        f'''Привет {user.mention_html()}! Добро пожаловать в Noon City! Скажи, ''' +
        '''ты у нас впервые, или просто я тебя раньше не видел?''' +
        '''Напиши "новый", если хочешь завести акк, или "войти", если уже бывалый''',
    )
    return 'purpose'


async def login_or_registration(update, context):
    purpose = update.message.text.lower()
    context.user_data['purpose'] = purpose
    if purpose.lower() == 'новый':
        return 'name'
    elif purpose.lower() == 'войти':
        await update.message.reply_html('Окей, самурай, говори почту')
        return 'email'
    else:
        await update.message.reply_html('Видимо, опечатка. Скажи ещё раз')
        return 'purpose'


async def email(update, context):
    email = update.message.text
    context.user_data['email'] = email
    db_sess = db_session.create_session()
    if context.user_data['purpose'] == 'войти':
        emails = db_sess.query(User).filter(User.email == email).first()
        if emails:
            await update.message.reply_html('Прелестно, теперь сообщи мне свой пароль. ' +
                                            'Не переживай, если и продам, то только за дорого)')
            return 'password'
        else:
            await update.message.reply_html('Well, такой почты не зарегано, попробуй еще раз')
    else:
        pass


async def password(update, context):
    password = update.message.text
    context.user_data['password'] = password
    db_sess = db_session.create_session()
    hached_password = db_sess.query(User.hashed_password).filter(User.email == context.user_data['email']).first()
    if check_password_hash(hached_password, password):
        await update.message.reply_html('Найс, чувствуй себя как дома')
        return ConversationHandler.END
    else:
        await update.message.reply_html('Пароль не похож на нужный, попробуй-ка еще раз')
        return 'password'

async def stop():
    pass


def main():
    db_session.global_init("db\\noon_town.db")
    application = Application.builder().token(token).build()
    start_conversation = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            'purpose': [MessageHandler(filters.TEXT & ~filters.COMMAND, login_or_registration)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            'email': [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            'password': [MessageHandler(filters.TEXT & ~filters.COMMAND, password)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(start_conversation)
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == '__main__':
    main()
