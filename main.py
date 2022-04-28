# flask_ngrok_example.py
from flask import Flask, request
from flask_ngrok import run_with_ngrok
import logging
import json
import random
from models.monsters.MonsterBase import MonsterBase
from models.bonuses.BonusBase import BonusBase
from models.race.RaceBase import RaceBase
from models.сurses.CurseBase import CurseBase
from models.armament.ArmamentBase import ArmamentBase

app = Flask(__name__)
run_with_ngrok(app)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

marks = '''!()-[]{};?@#$%:'"\,./^&amp;*_'''
link = '1533899/8ce30965e087db5e9bdc'
# первый элемент отвечает за монстра или нет, то есть 0 - это проклятье
monsters = [[1, 1, 'Молотая красотка', 'Бьет баба молотом… Потеряй уровень!', 1, 1],
            [1, 2, "Питбуль", 'В зад укушенный герой - позорище. Потеряй 2 уровня', 1, 1]]
proklates = [[0, 'Невыносимо гнусное проклятие! Потеряй рандомную шмотку!']]

# 0 - бонус, 1 - оружие
bonuses = [[0, 'Зелье холодного взрыва', 'Играй в любой бой. +3 любой стороне. Разовая шмотка',
            100, '+3 силе'], [0, 'Сюрприз', 'Получи уровень', 1000]]
armores = [[1, 3, 'Коротыширокне латы', 400, 3],
           [1, 3, 'Бензопила страшного расчленителя', 600, 1, 2]]
all_treasures = (bonuses + armores) * 3  # изменить!!!
all_doors_for_game = (monsters + proklates) * 3  # изменить!!!  # c проклятьями
all_doors_for_hero = monsters * 3  # изменить!!!

dict_treasures = {i: all_treasures[i] for i in range(len(all_treasures))}
dict_doors_for_game = {i: all_doors_for_game[i] for i in range(len(all_doors_for_game))}
dict_doors_for_hero = {i: all_doors_for_hero[i] for i in range(len(all_doors_for_hero))}


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

    handle_dialog(request.json, response)  # функция

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {'is_started': False, 'level': 1, 'epoch': '11', 'weapon': [],
                                   'class': None,
                                   'armor': {'head': None, 'body': None, 'leg': None},
                                   'cards_on_hands': [], 'is_alive': True,
                                   'what_treasures_stay': list(range(len(dict_treasures))),
                                   'what_doors_stay': list(range(len(dict_doors_for_hero)))}
        # Заполняем текст ответа
        res['response']['text'] = 'Привет! Добро пожаловать в игру "mini Манчкин"!' \
                                  ' Ты уже знаешь правила этой игры!?'
        # Получим подсказки
        res['response']['buttons'] = [{'title': 'Да', 'hide': True}, {'title': 'Нет', 'hide': True}]
        return
    if sessionStorage[user_id]['epoch'][0] == '1':
        if sessionStorage[user_id]['epoch'] == '11':  # знает ли правила
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Хорошо! Ты готов к приключениям по подземельям!?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '12'  # начинаем ли игру
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Тогда давай я расскажу тебе правила: ...\n' \
                                          'Вы поняли правила?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '13'  # доп правила
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
        elif sessionStorage[user_id]['epoch'] == '12':  # согласились ли играть <----
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Вы зашли в лабиринт, везде темно,' \
                                          ' но вы увидели несколько дверей, в которых могут' \
                                          ' таяться монстры и проклятья.... Берегите себя,' \
                                          ' да будет игра!!!\n'
                ids_treasures = random.sample(sessionStorage[user_id]['what_treasures_stay'],
                                              4)  # берем id сокровищ
                ids_doors = random.sample(sessionStorage[user_id]['what_doors_stay'],
                                          4)  # берем id дверей
                # sessionStorage[user_id]['cards_on_hands'] = [dict_treasures[i] for i in
                #                                              ids_treasures] + [dict_doors_for_hero[i]
                #                                                                for i in ids_doors]
                # так если у нас в списке будут классы, иначе:
                print(dict_treasures[0])
                # создаем 4 карты двери и сокровищ
                treasures = [
                    ArmamentBase(*dict_treasures[i][1:]) if dict_treasures[i][0] != 0 else BonusBase(
                        *dict_treasures[i][1:]) for i in ids_treasures]
                doors = [MonsterBase(*dict_doors_for_hero[i][1:]) if dict_doors_for_hero[i][0] != 0
                         else CurseBase(*dict_doors_for_hero[i][1:]) for i in ids_doors]
                # пуляем в user
                sessionStorage[user_id]['cards_on_hands'] = treasures + doors
                # сортируем
                sessionStorage[user_id]['cards_on_hands'] = sort_cards(user_id)
                # даем ответ для алисы
                text = show_names(user_id)  # создаем текст для вывода всех предметов
                res['response']['text'] += '---------\n'
                res['response']['text'] += text
                res['response']['text'] += find_free_cards(user_id)  # какие карты можно положить?
                res['response']['text'] += '---------\n'
                res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '2'  # начинаем игру
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Приходите когда будете готовы! До скорых встреч!'
                res['response']['end_session'] = True
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]

        elif sessionStorage[user_id]['epoch'] == '13':  # поняли ли правила
            if req['request']['original_utterance'].lower() in ['да']:
                res['response']['text'] = 'Хорошо! Ты готов к приключениям по подземельям!?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
                sessionStorage[user_id]['epoch'] = '12'  # начинаем ли игру
            elif req['request']['original_utterance'].lower() in ['нет']:
                res['response']['text'] = 'Тогда лови ссылку для углубленного' \
                                          ' разбора: https://add-hobby.ru/munchkin.html \n' \
                                          'Хорошо! Ты готов к приключениям по подземельям!?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True},
                                              {"title": "Правила",
                                               "url": "https://add-hobby.ru/munchkin.html",
                                               "hide": True}]
                sessionStorage[user_id]['epoch'] = '12'  # начинаем ли игру
            else:  # не поняли
                res['response']['text'] = 'Я вас не поняла, извините... Так да или нет?'
                res['response']['buttons'] = [{'title': 'Да', 'hide': True},
                                              {'title': 'Нет', 'hide': True}]
    elif sessionStorage[user_id]['epoch'][0] == '2':
        if sessionStorage[user_id]['epoch'] == '2':  # какие карты он достает
            text_res = req['request']['original_utterance'].lower()
            if 'никакие' in text_res:  # ничего не хочет выкладывать
                res['response']['text'] = 'Вы отказались класть карты!\n'
                res['response']['text'] += '---------\n'
                res['response']['text'] += 'Хорошо, на вашем столе:\n'
                res['response']['text'] += show_names(user_id)
                res['response']['text'] += '---------\n'
                res['response'][
                    'text'] += 'Вы стучитесь в дверь и вам выпадает: (выпавшая карта)'  # доделать
                sessionStorage[user_id]['epoch'] = '24'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                return
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
                res['response']['text'] += '---------\n'
                res['response']['text'] += show_names(user_id)
                res['response']['text'] += find_free_cards(user_id)  # какие карты можно положить?
                res['response']['text'] += '---------\n'
                res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
                res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                return
            res['response'][
                'text'] = f'Вы выбрали позиции: {", ".join(num)}\n'
            for x in num:
                if int(x) <= 0 or int(x) > len(sessionStorage[user_id]['cards_on_hands']):
                    res['response'][
                        'text'] += f'Ошибка! Вы должны говорить цифры в диапазоне от 1 до {len(sessionStorage[user_id]["cards_on_hands"])}\n'
                    res['response']['text'] += '---------\n'
                    res['response']['text'] += show_names(user_id)
                    res['response']['text'] += find_free_cards(
                        user_id)  # какие карты можно положить?
                    res['response']['text'] += '---------\n'
                    res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
                    res['response']['buttons'] = [{'title': 'Никакие', 'hide': True}]
                    return
            t, cards = is_all_right(user_id, [int(i) - 1 for i in
                                              num])  # t - без ошибок? cards - текст функции
            if t:
                res['response']['text'] += 'Вы выбрали карточки:\n' + cards
                res['response']['text'] += '---------\n'
                res['response']['text'] += show_names(user_id)
                res['response']['text'] += '---------\n'

            else:
                res['response']['text'] += 'Ошибка!\n' + cards
                res['response']['text'] += '---------\n'
                res['response']['text'] += show_names(user_id)
                res['response']['text'] += find_free_cards(
                    user_id)  # какие карты можно положить?
                res['response']['text'] += '---------\n'
                res['response']['text'] += 'Какие карты вы хотите положить на стол? (номера)'
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
        elif card.__class__.__name__ == 'Proklate':
            if card.price != 1000:
                return False, f'Вы выбрали бонус "{card.title}",но его не как нельзя применить!'
            else:
                cards_choose['Bonus'].append(card)
        elif card.__class__.__name__ == 'Race':
            cards_choose['Race'].append(card)
        elif card.__class__.__name__ == 'Bonus':
            cards_choose['Bonus'].append(card)
    # предметы
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
        sessionStorage[user_id]['armor']['head'] = cards_choose['head'][0]
        all_names_cards += f"{cards_choose['head'][0].title}\n"
    if len(cards_choose['body']) != 0:
        sessionStorage[user_id]['armor']['body'] = cards_choose['body'][0]
        all_names_cards += f"{cards_choose['body'][0].title}\n"
    if len(cards_choose['leg']) != 0:
        sessionStorage[user_id]['armor']['leg'] = cards_choose['leg'][0]
        all_names_cards += f"{cards_choose['leg'][0].title}\n"
    if len(cards_choose['weapon']) != 0:
        sessionStorage[user_id]['weapon'] = cards_choose['weapon']
        if len(cards_choose['weapon']) == 1:
            all_names_cards += f"{cards_choose['weapon'][0].title}\n"
        else:
            all_names_cards += f"{cards_choose['weapon'][0].title}\n"
            all_names_cards += f"{cards_choose['weapon'][1].title}\n"
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


def find_free_cards(user_id):  # передаю num от 1 - бес
    list_obj = sessionStorage[user_id]['cards_on_hands']
    d = {'class': [], 'head': [], 'body': [], 'leg': [], 'bonus': [], 'weapon': []}
    for i in range(len(list_obj)):
        if list_obj[i].__class__.__name__ == 'Bonus':
            if list_obj[i].price == 1000:
                d['bonus'].append(str(i + 1))
        if list_obj[i].__class__.__name__ == 'Race':
            if sessionStorage[user_id]['class'] is not None:
                d['class'].append(str(i + 1))
        if list_obj[i].__class__.__name__ == 'Armament':
            if list_obj[i].what == 1:
                if len(sessionStorage[user_id]['weapon']) != 2:
                    if len(sessionStorage[user_id]['weapon']) == 1 and list_obj[
                        i].if_weapon_hand == 2:
                        pass
                    else:
                        d['weapon'].append(str(i + 1))
            if list_obj[i].what == 2:
                if sessionStorage[user_id]['armor']['head'] is None:
                    d['head'].append(str(i + 1))
            if list_obj[i].what == 3:
                if sessionStorage[user_id]['armor']['body'] is None:
                    d['body'].append(str(i + 1))
            if list_obj[i].what == 4:
                if sessionStorage[user_id]['armor']['leg'] is None:
                    d['leg'].append(str(i + 1))
    text = 'Вы можете положить:\n'
    for k, v in d.items():
        if k == 'class' and len(d['class']) != 0:
            text += f'Раса: {", ".join(sorted(v))}\n'
        if k == 'weapon' and len(d['weapon']) != 0:
            text += f'Оружие: {", ".join(sorted(v))}\n'
        if k == 'head' and len(d['head']) != 0:
            text += f'Головняк: {", ".join(sorted(v))}\n'
        if k == 'body' and len(d['body']) != 0:
            text += f'Броник: {", ".join(sorted(v))}\n'
        if k == 'leg' and len(d['leg']) != 0:
            text += f'Поножи: {", ".join(sorted(v))}\n'
        if k == 'bonus' and len(d['bonus']) != 0:
            text += f'Получи уровень: {", ".join(sorted(v))}\n'
    return text


def sort_cards(user_id):  # сортировка карт в руке
    list_obj = sessionStorage[user_id]['cards_on_hands']
    s = []
    for i in list_obj:
        s.append([i.__class__.__name__, i])
    res = [i[1] for i in sorted(s, key=lambda x: x[0])]
    return res


def show_names(user_id):  # показ амундирования
    armor = sessionStorage[user_id]['armor']
    weapon = sessionStorage[user_id]['weapon']
    class_human = sessionStorage[user_id]['class']
    list_obj = sessionStorage[user_id]['cards_on_hands']
    text = ''
    text += f'Ваш level: {sessionStorage[user_id]["level"]}\n'
    if weapon != []:  # оружие
        if len(weapon) == 1 or weapon[0].title == weapon[1].title:
            text += f'Ваше оружие:\n1) {weapon[0].title} (+{weapon[0].bonus} к силе)\n'
        else:
            text += f'Ваше оружие:\n1) {weapon[0].title} (+{weapon[0].bonus} к силе) \n2) {weapon[1].title} (+{weapon[1].bonus} к силе)\n'
    else:
        text += f'Ваше оружие: -\n'
    text += 'На вас одет: \n'
    for k, v in armor.items():  # 'head': None, 'body': None, 'leg': None
        if k == 'head':
            if armor[k] is not None:
                text += f'Головняк: {v.title} (+{v.bonus} к силе) \n'
            else:
                text += f'Головняк: - \n'
        if k == 'body':
            if armor[k] is not None:
                text += f'Броник: {v.title} (+{v.bonus} к силе) \n'
            else:
                text += f'Броник: - \n'
        if k == 'leg':
            if armor[k] is not None:
                text += f'Поножи: {v.title} (+{v.bonus} к силе) \n'
            else:
                text += f'Поножи: - \n'
    if class_human is not None:
        text += f'Ваша раса: {class_human.title}\n'
    else:
        text += f'Ваша раса: -\n'

    if list_obj != []:
        text += f'Ваши карты на руках: \n'
        for i in range(len(list_obj)):
            if list_obj[i].__class__.__name__ == 'Bonus':
                text += f'{i + 1}) Бонус: "{list_obj[i].title}" ({list_obj[i].mini_text})\n'
            elif list_obj[i].__class__.__name__ == 'Armament':
                text += f'{i + 1}) Одежка: "{list_obj[i].title}" (+{list_obj[i].bonus} strength)\n'
            elif list_obj[i].__class__.__name__ == 'Monster':
                text += f'{i + 1}) Монстр: "{list_obj[i].title}"; level={list_obj[i].level}\n'
            elif list_obj[i].__class__.__name__ == 'Race':
                text += f'{i + 1}) Раса: "{list_obj[i].title}"\n'
    else:
        text += f'Ваши карты на руках: -\n'
    print(text)
    return text


if __name__ == '__main__':
    app.run()
