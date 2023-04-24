from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, RadioField, SelectField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired(), Email()])
    sex = RadioField('Пол', choices=['Мужчина', 'Женщина'], validators=[DataRequired()])
    from_where = RadioField('Откуда вы?', choices=[
        'Из крупного города', 'Из небольшого поселения',
        'Мигрировал из бедной страны', 'Из Noon City'], validators=[DataRequired()])
    ambitions = RadioField('Чего вы хотите?', choices=[
        'Стать легендой Noon City', 'Уничтожить корпорацию АраСакэ',
        'Навести порядок в городе, уменьшить преступность', 'Разбогатеть'], validators=[DataRequired()])
    parameters = RadioField('В чём вы особенно сильны?', choices=[
        'Физическая сила', 'Интеллект', 'Технические способности', 'Харизма', 'Ловкость'], validators=[DataRequired()])
    favourite_gun = RadioField('Какое оружие предпочтёте в случае необходимости', choices=[
        'Скорострельные пушки - моё всё', 'Предпочитаю уничтожать одиночными выстрелами',
        'Тащусь с оружия ближнего боя', 'Импланты как у Алана Слэшера'], validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
