# flask_ngrok_example.py
from flask import Flask, request
from flask_ngrok import run_with_ngrok
import logging
import json
import random
from classes import Monster, Bonus, Armament, Proklate, Race

app = Flask(__name__)
run_with_ngrok(app)

logging.basicConfig(level=logging.INFO)

cards_on_hands = [Monster(
    *[1, 'Молотая красотка', 'Бьет баба молотом… Потеряй уровень!', 1, 1])] * 5 + [
                     Bonus(*['Сюрприз', 'Получи уровень', 1000, '+1 уровень'])] * 2 + [Bonus(
    *['Зелье холодного взрыва', 'Играй в любой бой. +3 любой стороне. Разовая шмотка', 100,
      '+3 силе'])] * 2 + [Armament(*[3, 'Сандалеты-протекторы', 700, 4])]
sessionStorage = {
    '111': {'level': 8, 'epoch': '33', 'weapon': [Armament(*[4, 'Вездешний щит', 600, 1, 1]),
                                                  Armament(*[4, 'Мультиварка', 600, 1, 1]),
                                                  Armament(*[4, 'Big penis', 600, 1, 1])],
            'class': None, 'monster': None, 'overall_strength': 0,
            'bonus_strength': 0, 'money': 0,
            'armor': {'head': Armament(*[3, 'Бондана сволочизма', 400, 2]),
                      'body': Armament(*[1, 'Слизистая бочка', 200, 3]), 'leg': None},
            'cards_on_hands': cards_on_hands, 'is_alive': True, 'cards_to_sell': None}}
marks = '''!()-[]{};?@#$%:'"\,./^&amp;*_'''


@app.route('/', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {  # то что отправляем
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    # добавляем в ответ картинку
    # response['response']['card'] = {}
    # response['response']['card']['type'] = 'BigImage'
    # response['response']['card']['title'] = f'Что это за город?'
    # response['response']['card']['image_id'] = link
    gg = ''
    handle_dialog(request.json, response)  # функция

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    global gg
    user_id = req['session']['user_id']
    user_id = '111'
    if sessionStorage[user_id]['epoch'][0] == '3':
        if sessionStorage[user_id][
            'epoch'] == '33':  # готов продолжать + У пользователя больше 5 карт на руке?
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Хорошо! Тогда продолжим!\n'
                # У пользователя больше 5 карт на руке?
                if sessionStorage[user_id]['level'] >= 10:
                    res['response'][
                        'text'] = f'У вас {sessionStorage[user_id]["level"]} уровень! Вы выиграли!!!\n'
                    res['response']['end_session'] = True
                else:
                    if len(sessionStorage[user_id]['cards_on_hands']) > 5:
                        res['response'][
                            'text'] += 'У вас больше 5 карт на руках. Вы хотите убрать карту со стола?'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                        sessionStorage[user_id]['epoch'] = '42'  # доп правила
                    else:
                        res['response'][
                            'text'] += 'Вы прошли круг, молодец! Вы остались живы!!! Давайте открывать еще двери! Вы готовы продолжать?'
                        res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                      {'title': 'Нет', 'hide': True}]
                        sessionStorage[user_id]['epoch'] = '41'  # доп правила
            elif req['request']['original_utterance'].lower() in ['нет']:  # выход из игры
                res['response']['text'] = 'Приходите когда будете готовы! До скорых встреч!'
                res['response']['end_session'] = True
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
    elif sessionStorage[user_id]['epoch'][0] == '4':
        if sessionStorage[user_id]['epoch'] == '42':  # готов продолжать + новый цикл
            if req['request']['original_utterance'].lower() in ['да']:
                main_list = []
                for i in sessionStorage[user_id]['weapon']:
                    main_list.append([i.title, 'оружие'])
                try:
                    main_list.append([sessionStorage[user_id]['armor']['head'].title, 'шлем'])
                except:
                    pass
                try:
                    main_list.append([sessionStorage[user_id]['armor']['body'].title, 'броник'])
                except:
                    pass
                try:
                    main_list.append([sessionStorage[user_id]['armor']['leg'].title, 'ботинки'])
                except:
                    pass
                if len(main_list) != 0:
                    res['response']['text'] = f'Какие карты вы хотите убрать со стола в руки?\n'
                    for i in range(len(main_list)):
                        res['response'][
                            'text'] += f'{i + 1}. {main_list[i][0]} - {main_list[i][1]}\n'
                    sessionStorage[user_id]['epoch'] = '421'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
                else:
                    res['response'][
                        'text'] += f'У вас {len(sessionStorage[user_id]["cards_on_hands"])} карт. Вы хотите положить карты на стол?'
                    res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                  {'title': 'Нет', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '43'
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response'][
                    'text'] = f'У вас {len(sessionStorage[user_id]["cards_on_hands"])} карт. Вы хотите положить карты на стол?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '43'
            else:
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '421':
            if req["request"]["original_utterance"].lower() in ['никакие']:
                res['response'][
                    'text'] += f'У вас {len(sessionStorage[user_id]["cards_on_hands"])} карт. Вы хотите положить карты на стол?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '43'
            main_list = []
            for i in sessionStorage[user_id]['weapon']:
                main_list.append([i, 'weapon'])
            # снаряжение
            x1 = sessionStorage[user_id]['armor']['head']
            if x1 is not None:
                main_list.append([sessionStorage[user_id]['armor']['head'], 'head'])
            x2 = sessionStorage[user_id]['armor']['body']
            if x2 is not None:
                main_list.append([sessionStorage[user_id]['armor']['body'], 'body'])
            x3 = sessionStorage[user_id]['armor']['leg']
            if x3 is not None:
                main_list.append([sessionStorage[user_id]['armor']['leg'], 'leg'])
            # проверка
            input_text = req["request"]["original_utterance"].lower()
            num = []
            for i in input_text.split():
                # просто удаляем знаки препинания
                word = ''
                for x in i:
                    if x not in marks:
                        word += x
                print(word)
                if word.isdigit():
                    num.append(word)
            if len(num) == 0:
                res['response'][
                    'text'] = 'В вашем ответе отсутствуют цифры! Введите цифры! Например 1, 2...\n'
                res['response']['text'] = f'Какие карты вы хотите убрать со стола в руки?\n'
                for i in range(len(main_list)):
                    res['response'][
                        'text'] += f'{i + 1}. {main_list[i][0].title} - {main_list[i][1]}\n'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                return
            res['response'][
                'text'] = f'Вы выбрали позиции: {", ".join(num)}\n'
            for x in num:
                if int(x) <= 0 or int(x) > len(main_list):
                    res['response'][
                        'text'] += f"Ошибка! Вы должны говорить цифры в диапазоне от 1 до {len(main_list)}\n"
                    res['response']['text'] = f'Какие карты вы хотите убрать со стола в руки?\n'
                    for i in range(len(main_list)):
                        res['response'][
                            'text'] += f'{i + 1}. {main_list[i][0].title} - {main_list[i][1]}\n'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
            ml = []
            words = [int(i) for i in num]
            for i in words:
                if main_list[int(i) - 1][1] == 'body':
                    sessionStorage[user_id]['overall_strength'] -= sessionStorage[user_id]['armor']['body'].bonus
                    sessionStorage[user_id]['armor']['body'] = None
                elif main_list[int(i) - 1][1] == 'head':
                    sessionStorage[user_id]['overall_strength'] -= sessionStorage[user_id]['armor']['head'].bonus
                    sessionStorage[user_id]['armor']['head'] = None
                elif main_list[int(i) - 1][1] == 'leg':
                    sessionStorage[user_id]['overall_strength'] -= sessionStorage[user_id]['armor']['leg'].bonus
                    sessionStorage[user_id]['armor']['leg'] = None
                elif main_list[int(i) - 1][1] == 'weapon':
                    sessionStorage[user_id]['overall_strength'] -= main_list[int(i) - 1][0].bonus
                    sessionStorage[user_id]['weapon'].remove(main_list[int(i) - 1][0])
            for i in words:
                ml.append(main_list[int(i) - 1][0])
            for i in ml:
                sessionStorage[user_id]['cards_on_hands'].append(i)
            res['response']['text'] = f'Вы убрали со стола:\n'
            a = 1
            for i in ml:
                res['response']['text'] += f'{a}. {i.title} \n'
                a += 1
            res['response']['text'] += 'Вы хотите продолжить?\n'
            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                          {'title': 'Нет', 'hide': True}]
            sessionStorage[user_id]['epoch'] = '422'
        elif sessionStorage[user_id]['epoch'] == '422':
            if req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Приходите когда будете готовы! До скорых встреч!'
                res['response']['end_session'] = True
            elif req['request']['original_utterance'].lower() in ['да']:
                # res['response']['text'] = 'У вас осталось\n'
                # for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                #     res['response'][
                #         'text'] += f'{i + 1}. {sessionStorage[user_id]["cards_on_hands"][i].title}\n'
                res['response'][
                    'text'] = f'У вас {len(sessionStorage[user_id]["cards_on_hands"])} карт. Вы хотите положить карты на стол?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '43'
            else:
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '43':
            if req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Какие карты вы хотите скинуть или продать?\n'
                for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                    try:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                    except:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                sessionStorage[user_id]['epoch'] = '44'
            elif req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = ''
                show_not_all_cards(user_id, res)
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '431'
            else:
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '44':
            gg = req['request']['original_utterance'].lower()
            if 'никакие' in gg:  # ничего не хочет продавать
                # проверка больше ли 5 карт
                if len(sessionStorage[user_id]['cards_on_hands']) >= 6:
                    res['response']['text'] = 'Карт на руках должно быть не больше 5\n'
                    res['response']['text'] += 'Какие карты вы хотите скинуть или продать?\n'
                    for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                        try:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                        except:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                    sessionStorage[user_id]['epoch'] = '44'
                    return
            else:
                # проверка на правильность
                num = []

                for i in gg.split():
                    # просто удаляем знаки препинания
                    word = ''
                    for x in i:
                        if x not in marks:
                            word += x
                    print(word)
                    if word.isdigit():
                        num.append(word)
                # проверка
                if len(num) == 0:
                    res['response'][
                        'text'] = 'В вашем ответе отсутствуют цифры! Введите цифры! Например 1, 2...\n'
                    res['response']['text'] += 'Какие карты вы хотите скинуть или продать?\n'
                    for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                        try:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                        except:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                    sessionStorage[user_id]['epoch'] = '44'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
                res['response'][
                    'text'] = f'Вы выбрали позиции: {", ".join(num)}\n'
                for x in num:
                    if int(x) <= 0 or int(x) > len(sessionStorage[user_id]['cards_on_hands']):
                        res['response'][
                            'text'] += f'Ошибка! Вы должны говорить цифры в диапазоне от 1 до {len(sessionStorage[user_id]["cards_on_hands"])}\n'
                        res['response']['text'] += 'Какие карты вы хотите скинуть или продать?\n'
                        for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                            try:
                                res['response'][
                                    'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                            except:
                                res['response'][
                                    'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                        sessionStorage[user_id]['epoch'] = '44'
                        res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                        return
                sessionStorage[user_id]['cards_to_sell'] = [int(i) for i in num]
                res['response']['text'] = 'Вы действительно хотите продать эти карты?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                          {'title': 'Нет', 'hide': True}]
            sessionStorage[user_id]['epoch'] = '45'
        elif sessionStorage[user_id]['epoch'] == '45':
            if req['request']['original_utterance'].lower() in ['да']:
                main_list = []
                for i in sessionStorage[user_id]['weapon']:
                    main_list.append([i, 'weapon'])
                try:
                    main_list.append([sessionStorage[user_id]['armor']['head'], 'head'])
                except:
                    pass
                try:
                    main_list.append([sessionStorage[user_id]['armor']['body'], 'body'])
                except:
                    pass
                try:
                    main_list.append([sessionStorage[user_id]['armor']['leg'], 'leg'])
                except:
                    pass
                if len(sessionStorage[user_id]['cards_on_hands']) - len(sessionStorage[user_id]['cards_to_sell']) >= 6:
                    res['response']['text'] = 'Карт на руках должно быть не больше 5\n'
                    res['response']['text'] += 'Какие карты вы хотите скинуть или продать?\n'
                    for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                        try:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                        except:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                    sessionStorage[user_id]['epoch'] = '44'
                else:
                    try:
                        ml = []
                        kl = []
                        count = 0
                        for i in sessionStorage[user_id]['cards_to_sell']:
                            ml.append(sessionStorage[user_id]['cards_on_hands'][int(i) - 1])
                        for i in ml:
                            if i.__class__.__name__ == 'Monster':
                                sessionStorage[user_id]['cards_on_hands'].remove(i)
                                continue
                            count += int(i.price)
                            sessionStorage[user_id]['cards_on_hands'].remove(i)
                        res['response']['text'] = f'Вы получили за них: {count} монет\n'
                        level = count // 1000
                        sessionStorage[user_id]['level'] += level
                        ost = count % 1000
                        sessionStorage[user_id]["money"] += ost
                        res['response'][
                            'text'] += f'У вас {sessionStorage[user_id]["money"]} монет\n'
                        res['response']['text'] += f'+{level} level\n'
                        res['response']['text'] += f'У вас остались карты:\n'
                        a = 1
                        for i in sessionStorage[user_id]['cards_on_hands']:
                            res['response']['text'] += f'{a}. {i.title} \n'
                            a += 1
                        if sessionStorage[user_id]['level'] >= 10:
                            res['response'][
                                'text'] += f'У вас {sessionStorage[user_id]["level"]} уровень! Вы выиграли!!!\n'
                            res['response']['end_session'] = True
                        else:
                            res['response'][
                                'text'] += 'Вы прошли круг, молодец! Вы остались живы!!! Давайте открывать еще двери! Вы готовы продолжать?'
                            res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                                          {'title': 'Нет', 'hide': True}]
                            sessionStorage[user_id]['epoch'] = '41'  # доп правила
                    except:
                        res['response']['text'] = 'Ошибка! Давайте заного'
                        sessionStorage[user_id]['epoch'] = '43'
            elif req['request']['original_utterance'].lower() in ['нет']:
                gg = req['request']['original_utterance'].lower()
                res['response']['text'] = 'Какие карты вы хотите скинуть или продать?\n'
                for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                    try:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                    except:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                sessionStorage[user_id]['epoch'] = '44'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '431':
            text_res = req['request']['original_utterance'].lower()
            if 'никакие' in text_res:  # ничего не хочет выкладывать
                res['response']['text'] = 'Вы отказались класть карты!\n'
                res['response']['text'] = 'Какие карты вы хотите скинуть или продать?\n'
                for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                    try:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                    except:
                        res['response'][
                            'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '44'
                return
            else:
                # проверка на правильность
                num = []

                for i in text_res.split():
                    # просто удаляем знаки препинания
                    word = ''
                    for x in i:
                        if x not in marks:
                            word += x
                    print(word)
                    if word.isdigit():
                        num.append(word)
                # проверка
                if len(num) == 0:
                    res['response'][
                        'text'] = 'В вашем ответе отсутствуют цифры! Введите цифры! Например 1, 2...\n'
                    show_not_all_cards(user_id, res)
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
                res['response'][
                    'text'] = f'Вы выбрали позиции: {", ".join(num)}\n'
                for x in num:
                    if int(x) <= 0 or int(x) > len(sessionStorage[user_id]['cards_on_hands']):
                        res['response'][
                            'text'] += f'Ошибка! Вы должны говорить цифры в диапазоне от 1 до {len(sessionStorage[user_id]["cards_on_hands"])}\n'
                        show_not_all_cards(user_id, res)
                        res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                        return
                t, cards = is_all_right(user_id, [int(i) - 1 for i in
                                                  num])  # t - без ошибок? cards - текст функции
                if t:
                    res['response']['text'] += 'Ваши действия применились!\n'
                    res['response']['text'] += 'Какие карты вы хотите скинуть или продать?\n'
                    for i in range(len(sessionStorage[user_id]['cards_on_hands'])):
                        try:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} ({sessionStorage[user_id]["cards_on_hands"][i].price} $)\n'
                        except:
                            res['response'][
                                'text'] += f'{i + 1}) {sessionStorage[user_id]["cards_on_hands"][i].title} (0 $)\n'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    sessionStorage[user_id]['epoch'] = '44'
                    return
                else:
                    res['response']['text'] += 'Ошибка!\n' + cards
                    show_not_all_cards(user_id, res)
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return


def is_all_right(user_id, nums):  # проверяем на правильность выбора карт
    cards_choose = {'Bonus': [], 'Race': [], 'head': [], 'body': [], 'leg': [], 'weapon': []}
    #  Monster, Bonus, Armament, Proklate, Race
    # записываем в словарь
    for i in nums:
        card = sessionStorage[user_id]['cards_on_hands'][i]
        if card.__class__.__name__ == 'Armament':
            if card.what == 1:
                cards_choose['weapon'].append(card)
            if card.what == 2:
                cards_choose['head'].append(card)
            if card.what == 3:
                cards_choose['body'].append(card)
            if card.what == 4:
                cards_choose['leg'].append(card)
        elif card.__class__.__name__ == 'Monster':
            return False, 'Вы выбрали монстра!\nЕго нельзя одеть на себя или еще лучше применить как бонус!\n'
        elif card.__class__.__name__ == 'Proklate':
            return False, 'Вы выбрали проклятье!\nЕго нельзя одеть на себя или еще лучше применить как бонус!\n'
        elif card.__class__.__name__ == 'Bonus':
            if card.price != 1000:
                return False, f'Вы выбрали бонус "{card.title}",но его не как нельзя применить!'
            else:
                cards_choose['Bonus'].append(card)
        elif card.__class__.__name__ == 'Race':
            cards_choose['Race'].append(card)
        elif card.__class__.__name__ == 'Bonus':
            cards_choose['Bonus'].append(card)
    # предметы
    kol_head = 0
    kol_body = 0

    if len(cards_choose['head']) > 1:
        return False, f'Вы выбрали {len(cards_choose["head"])} шлемов! Куда вам столько?'
    if len(cards_choose['body']) > 1:
        return False, f'Вы выбрали {len(cards_choose["body"])} брони! Куда вам столько?'
    if len(cards_choose['leg']) > 1:
        return False, f'Вы выбрали {len(cards_choose["body"])} поножь! Куда вам столько?'
    if len(cards_choose['weapon']) > 2:
        return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Куда вам столько?'
    # оружие
    elif len(cards_choose['weapon']) == 2:
        if cards_choose['weapon'][0].if_weapon_hand == 1 and cards_choose['weapon'][
            1].if_weapon_hand == 1 and len(sessionStorage[user_id]['weapon']) == 0:
            pass
        else:
            return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Превышен лимит оружия на руках'
    elif len(cards_choose['weapon']) == 1:
        if cards_choose['weapon'][0].if_weapon_hand == 1:
            if len(sessionStorage[user_id]['weapon']) == 0:
                pass
            elif len(sessionStorage[user_id]['weapon']) == 1:
                if sessionStorage[user_id]['weapon'].if_weapon_hand == 1:
                    pass
                else:
                    return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Превышен лимит оружия на руках'
            else:
                return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Превышен лимит оружия на руках'
        else:
            if len(sessionStorage[user_id]['weapon']) == 0:
                pass
            else:
                return False, f'Вы выбрали {len(cards_choose["weapon"])} оружия! Превышен лимит оружия на руках'
    # засовываем все в героя!
    print(cards_choose)
    all_names_cards = '---------\n'
    if len(cards_choose['head']) != 0:
        if sessionStorage[user_id]['armor']['head'] is None:
            sessionStorage[user_id]['overall_strength'] += cards_choose['head'][0].bonus
        else:
            sessionStorage[user_id]['overall_strength'] -= sessionStorage[user_id]['armor']['head'].bonus
            sessionStorage[user_id]['overall_strength'] += cards_choose['head'][0].bonus
        sessionStorage[user_id]['armor']['head'] = cards_choose['head'][0]
        all_names_cards += f"{cards_choose['head'][0].title}\n"
    if len(cards_choose['body']) != 0:
        if sessionStorage[user_id]['armor']['body'] is None:
            sessionStorage[user_id]['overall_strength'] += cards_choose['body'][0].bonus
        else:
            sessionStorage[user_id]['overall_strength'] -= sessionStorage[user_id]['armor']['body'].bonus
            sessionStorage[user_id]['overall_strength'] += cards_choose['body'][0].bonus
        sessionStorage[user_id]['armor']['body'] = cards_choose['body'][0]
        all_names_cards += f"{cards_choose['body'][0].title}\n"
        sessionStorage[user_id]['overall_strength'] += cards_choose['body'][0].bonus
    if len(cards_choose['leg']) != 0:
        if sessionStorage[user_id]['armor']['leg'] is None:
            sessionStorage[user_id]['overall_strength'] += cards_choose['leg'][0].bonus
        else:
            sessionStorage[user_id]['overall_strength'] -= sessionStorage[user_id]['armor']['leg'].bonus
            sessionStorage[user_id]['overall_strength'] += cards_choose['leg'][0].bonus
        sessionStorage[user_id]['armor']['leg'] = cards_choose['leg'][0]
        all_names_cards += f"{cards_choose['leg'][0].title}\n"
        sessionStorage[user_id]['overall_strength'] += cards_choose['leg'][0].bonus
    if len(cards_choose['weapon']) != 0:
        sessionStorage[user_id]['weapon'] = cards_choose['weapon']
        if len(cards_choose['weapon']) == 1:
            all_names_cards += f"{cards_choose['weapon'][0].title}\n"
            sessionStorage[user_id]['overall_strength'] += cards_choose['weapon'][0].bonus
        else:
            all_names_cards += f"{cards_choose['weapon'][0].title}\n"
            all_names_cards += f"{cards_choose['weapon'][1].title}\n"
            sessionStorage[user_id]['overall_strength'] += cards_choose['weapon'][0].bonus
            sessionStorage[user_id]['overall_strength'] += cards_choose['weapon'][1].bonus
    if len(cards_choose['Race']) != 0:
        sessionStorage[user_id]['class'] = cards_choose['Race'][0]
        all_names_cards += f"{cards_choose['Race'][0].title}\n"
    if len(cards_choose['Bonus']) != 0:
        sessionStorage[user_id]['level'] += len(cards_choose['Bonus'])
        all_names_cards += f"{cards_choose['Bonus'][0].title} * {len(cards_choose['Bonus'])}\n"
    all_names_cards += '---------\n'
    # удаляем карточки, которые использовали
    for i in range(len(nums)):
        sessionStorage[user_id]['cards_on_hands'].pop(nums[i] - i)
    print(sessionStorage[user_id]['cards_on_hands'])
    return True, all_names_cards + 'Ваши действия применились для героя! Он стал сильнее!!!\n'


def show_not_all_cards(user_id, res):
    armor = sessionStorage[user_id]['armor']
    weapon = sessionStorage[user_id]['weapon']
    class_human = sessionStorage[user_id]['class']
    list_obj = sessionStorage[user_id]['cards_on_hands']
    res['response']['text'] += 'Характеристики героя: '
    res['response']['text'] += f'level: {sessionStorage[user_id]["level"]}; '
    res['response'][
        'text'] += f'Cила: {sessionStorage[user_id]["overall_strength"] + sessionStorage[user_id]["level"]}; '
    if class_human is not None:
        res['response']['text'] += f'Раса: {class_human.title}; '
    else:
        res['response']['text'] += f'Раса: -; '
    if len(weapon) != 0:
        res['response']['text'] += f'Оружие: +{" +".join([str(i.bonus) for i in weapon])}; '
    else:
        res['response']['text'] += f'Оружие: -; '
    if armor['head'] is not None:
        res['response']['text'] += f'Головняк: {armor["head"].bonus}; '
    else:
        res['response']['text'] += f'Головняк: -; '
    if armor['body'] is not None:
        res['response']['text'] += f'Броня: {armor["body"].bonus}; '
    else:
        res['response']['text'] += f'Броня: -; '
    if armor['leg'] is not None:
        res['response']['text'] += f'Поножи: {armor["leg"].bonus}; '
    else:
        res['response']['text'] += f'Поножи: -; '
    res['response']['text'] += '\nКарты на руках:\n'
    for i in range(len(list_obj)):
        if list_obj[i].__class__.__name__ == 'Bonus':
            res['response'][
                'text'] += f'{i + 1}) Бонус: "{list_obj[i].title}" ({list_obj[i].mini_text})\n'
        elif list_obj[i].__class__.__name__ == 'Armament':
            res['response'][
                'text'] += f'{i + 1}) Одежка: "{list_obj[i].title}" (+{list_obj[i].bonus})\n'
        elif list_obj[i].__class__.__name__ == 'Monster':
            res['response'][
                'text'] += f'{i + 1}) Монстр: "{list_obj[i].title}" ({list_obj[i].level} lvl)\n'
        elif list_obj[i].__class__.__name__ == 'Race':
            res['response']['text'] += f'{i + 1}) Раса: "{list_obj[i].title}"\n'
    res['response']['text'] += 'Какие карты вы хотите положить: (номера)'


if __name__ == '__main__':
    app.run()
