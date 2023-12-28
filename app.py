import logging

import streamlit as st


st.set_page_config(
    page_title='STRMная Анька',
    page_icon=(
        'https://raw.githubusercontent.com/Mathematician2000/'
        'aneks-gen/master/icon.png'
    ),
)


from model import (
    DEFAULT_MAX_LEN, HEIGHT, MAX_CHARS, MAX_LEN, MIN_LEN, MODEL,
)
from utils import set_background


set_background(
    'https://raw.githubusercontent.com/Mathematician2000/'
    'aneks-gen/master/background.png'
)


st.title('Привет, я STRMная Анька! Хочешь анекдот? :)')


prompt = st.text_area(
    'Начните текст, а Анька продолжит:',
    'Полина и Индиго сидят у костра, и вдруг',
    height=HEIGHT,
    max_chars=MAX_CHARS,
    help='Не тормози, вводи текст и жми кнопку :)',
    placeholder='Чтобы Индиго написал вам персональный анекдот, заведите тикет в очереди STRMDUTY.',
).lstrip()

max_length = st.slider(
    'Максимальная длина выходного текста (в словах)',
    MIN_LEN,
    MAX_LEN,
    DEFAULT_MAX_LEN,
    help='Обычный слайдер длины текста, что такого?',
)

button = st.button('Пошутить')


MODEL.clear_output()
if button:
    try:
        if prompt:
            MODEL.run_model(
                prompt,
                max_length=max_length,
            )

            output = MODEL.get_last_output()
            logging.info(f'Output: {output}')
    except Exception as err:
        st.exception(
            'OMG WHAT THE HELL IS GOING ON HERE '
            f'JUST LOOK AT THIS MADNESS:\n{err}'
        )

st.markdown(MODEL.get_last_output())

st.markdown('_' * 10)
st.markdown('by [Mathematician2000](https://gitlab.com/Mathematician2000)')
