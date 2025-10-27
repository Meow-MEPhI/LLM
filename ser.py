import json
import requests
from bs4 import BeautifulSoup
from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage


AUTH_KEY = ""

ARTICLE_URL = "https://cyberleninka.ru/article/n/ugolovnyy-kodeks-finlyandii-1889-g-kak-zakonodatelnyy-istochnik-evropeyskoy-integratsii/viewer"

try:

    response = requests.get(ARTICLE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    text = (soup.find('div', class_='article__body') or soup).get_text(' ', strip=True)

    # Рубрикация текста
    giga = GigaChat(credentials=AUTH_KEY, verify_ssl_certs=False)
    prompt = f"Ответ нужен в JSON с ключами!!! Ты — редактор-верстальщик и библиограф; задача: построить рубрикацию научной статьи как систему взаимосвязанных и соподчинённых заголовков, где заголовки старших уровней логически включают младшие, а одноуровневые заголовки равнозначны и не пересекаются; правила: 1) один признак деления на каждом уровне (не смешивай основания деления внутри одного уровня); 2) полнота: сумма подразделов покрывает содержание родительского раздела, «пустых» или дублирующих пунктов нет; 3) одноуровневые разделы не пересекаются и не включают друг друга; 4)заголовки краткие, терминологичные, без лишних слов;"
    prompt = f"Ты — редактор-верстальщик и библиограф; задача: построить рубрикацию научной статьи как систему взаимосвязанных и соподчинённых заголовков, где заголовки старших уровней логически включают младшие, а одноуровневые заголовки равнозначны и не пересекаются; правила: 1) один признак деления на каждом уровне (не смешивай основания деления внутри одного уровня); 2) полнота: сумма подразделов покрывает содержание родительского раздела, «пустых» или дублирующих пунктов нет; 3) одноуровневые разделы не пересекаются и не включают друг друга; 4)заголовки краткие, терминологичные, без лишних слов;"
    messages = [SystemMessage(content=prompt), HumanMessage(content=text)]
    result = giga.invoke(messages).content

    # Вывод результата
    #print(json.dumps(json.loads(result), ensure_ascii=False, indent=2))
    print(result)

except Exception as e:
    print(f"Произошла ошибка: {e}")
