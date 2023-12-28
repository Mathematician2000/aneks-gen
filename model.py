import os
from pathlib import Path
import re
from typing import Any

from razdel import sentenize
from simpletransformers.language_generation import LanguageGenerationModel
import streamlit as st
from yadisk import YaDisk


TOP_K = 50
TOP_P = 0.95

MIN_LEN = 20
MAX_LEN = 100
DEFAULT_MAX_LEN = 50

HEIGHT = 200
MAX_CHARS = 1000


MODEL_ARGS = {
    'do_sample': True,
    'top_k': TOP_K,
    'top_p': TOP_P,
    'max_length': DEFAULT_MAX_LEN,
    'verbose': True,
}


class AnkaModel:
    def __init__(self, *args: Any, **kwargs: Any):
        self.model = LanguageGenerationModel(*args, **kwargs)
        self.output = ''

    def run_model(self, prompt: str, **kwargs: Any) -> str:
        output = self.model.generate(prompt, args=kwargs)[0]
        puncts = ',.!?…»'
        continuation = re.sub(
            rf'(?P<punct>[\{puncts}])(?P<ch>[А-ЯЁA-Z"«-])',
            r'\g<punct> \g<ch>',
            output[len(prompt):],
        )

        sentences = list(sent.text for sent in sentenize(continuation))
        if len(sentences) > 1 and sentences[-1][-1] not in puncts:
            sentences.pop()
        continuation = ' '.join(sentences)

        output = f'**{prompt}** {continuation}'.replace('  ', ' ')
        for ch in puncts:
            output = output.replace(f' {ch} ', f'{ch} ')
        self.output = output

        return output

    def get_last_output(self) -> str:
        return self.output

    def clear_output(self) -> None:
        self.output = ''


FOLDER_LENGTH = 8


@st.cache_resource(max_entries=1)
def load_model(**kwargs: Any) -> AnkaModel:
    folder = 'LM_outputs'
    folder_path = Path(folder)
    if not folder_path.is_dir() or len(list(folder_path.iterdir())) < FOLDER_LENGTH:
        with st.spinner('Скачиваем модельку... Придётся подождать.'):
            folder_path.mkdir(exist_ok=True)
            ya = YaDisk(token=os.environ.get('YADISK_OAUTH_TOKEN'))
            if not ya.check_token():
                raise ValueError('Token check failed')
            for file in ya.listdir(f'/yaship/aneks-gen/{folder}'):
                filename = file.name
                path = f'{folder}/{filename}'
                ya.download(f'/yaship/aneks-gen/{path}', path)

    return AnkaModel(
        'gpt2',
        'LM_outputs',
        use_cuda=False,
        args=kwargs,
    )


MODEL = load_model(**MODEL_ARGS)
