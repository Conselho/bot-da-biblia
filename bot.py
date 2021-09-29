import random
import threading

import api

# permite que as threads sejam executadas por ordem.
# isto é porque o lock só permite que seja executada uma thread de cada vez,
# e sempre que chega uma nova thread que tem de ficar à espera esta vai ser colocada em fila
lock = threading.Lock()


def thread_func(update_):
    lock.acquire()
    text = api.get_message_text(update_)
    chat_id = api.get_chat_id(update_)

    word_list = text.strip().split(" ")
    # # para testar se o bot está a funcionar
    if "olá" in text.lower() and "bot" in text.lower():
        api.send_message(chat_id, "Olá. Bem-vindo ao Bot da Bíblia. Para já sou só um dado e um reconhecedor de"
                                  " referências bíblicas")
        api.send_message(chat_id, "Podes mandar uma mensagem a dizer 'lançar' para veres quanto te calha, ou mandar "
                                  "uma referência bíblica (para já, só se for Novo Testamento), que eu digo se existe "
                                  "ou não.")
    elif "lançar" in text.lower():
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        api.send_message(chat_id, "Calhou " + str(dado1) + " num dado e " + str(dado2)
                         + " no outro, um total de " + str(dado1 + dado2) + "!")
        api.send_message(chat_id, "Foi sorte?")
    elif len(word_list) < 20:
        # se a mensagem for de 20 ou mais palavras não será analisada
        for i in range(len(word_list) - 1):  # para cada palavra analisada
            # são analisadas 10 palavras à sua frente
            for k in range(2, 11):
                possivel_ref = ""
                for j in range(i, min(i + k, len(word_list) - 1)):
                    possivel_ref = possivel_ref + " " + word_list[j]
                possivel_ref.strip()
                api.send_message(chat_id, possivel_ref)

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
