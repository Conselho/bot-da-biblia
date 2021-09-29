import random
import threading
import api

condition1 = True  # esta vai ser para comandos
condition2 = True  # esta vai ser para referências encontradas
condition3 = True  # esta vai ser para frases encontradas

# permite que as threads sejam executadas por ordem.
# isto é porque o lock só permite que seja executada uma thread de cada vez,
# e sempre que chega uma nova thread que tem de ficar à espera esta vai ser colocada em fila
lock = threading.Lock()


def add_condition1(new_condition):
    global condition1
    condition1 = condition1 and new_condition


def add_condition2(new_condition):
    global condition2
    condition2 = condition2 and new_condition


def add_condition3(new_condition):
    global condition3
    condition3 = condition3 and new_condition


def thread_func(update_):
    lock.acquire()
    global condition1
    global condition2

    text = api.get_message_text(update_)
    chat_id = api.get_chat_id(update_)

    # aqui cria-se condições para uma resposta possível do bot
    condition1 = True
    add_condition1("olá" in text.lower())
    add_condition1("bot" in text.lower())
    # se nenhuma das acima for True, mas uma destas
    condition2 = True
    add_condition2("lançar" in text.lower())

    if condition1:
        api.send_message(chat_id, "Olá. Bem-vindo ao Bot da Bíblia. Para já sou só um dado. Podes mandar uma mensagem "
                                  "a dizer 'lançar' para veres quanto te calha")
    elif condition2:
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        api.send_message(chat_id, "Calhou " + str(dado1) + " num dado e " + str(dado2)
                         + " no outro, um total de " + str(dado1 + dado2) + "!")
        api.send_message(chat_id, "Foi sorte?")
    lock.release()


if __name__ == '__main__':
    update = api.last_update(0)
    # isto garante que o bot não responde ao último update quando é ligado
    last_resolved_update_id = api.get_update_id(update)
    while True:
        update = api.last_update(last_resolved_update_id)
        if api.get_update_id(update) != last_resolved_update_id:
            thread = threading.Thread(target=thread_func, args=[update])
            last_resolved_update_id = update["update_id"]
            thread.start()
