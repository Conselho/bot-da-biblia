import random
import threading

import api
# permite que as threads sejam executadas por ordem.
# isto é porque o lock só permite que seja executada uma thread de cada vez,
# e sempre que chega uma nova thread que tem de ficar à espera esta vai ser colocada em fila
import estrutura_da_biblia

lock = threading.Lock()


def thread_func(update_):
    lock.acquire()
    text = api.get_message_text(update_)
    chat_id = api.get_chat_id(update_)

    word_list = text.strip().split(" ")
    # # para testar se o bot está a funcionar
    if "olá" in text.lower() and "bot" in text.lower():
        api.send_message(chat_id, "Olá. Sou o Bot da Bíblia. Para já sou só um dado e um reconhecedor de"
                                  " referências bíblicas.")
        api.send_message(chat_id, "Podes mandar uma mensagem a dizer 'lançar' para veres quanto te calha, ou mandar "
                                  "uma referência bíblica (para já, só se for Novo Testamento), que eu digo se existe "
                                  "ou não.")
    elif "lançar" in text.lower():
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        api.send_message(chat_id, "Calhou " + str(dado1) + " num dado e " + str(dado2)
                         + " no outro, um total de " + str(dado1 + dado2) + "!")
        api.send_message(chat_id, "Foi sorte?")
    elif len(word_list) < 12:
        referencias_list = []
        # se a mensagem for comprida demais não será analisada
        for i in range(len(word_list) - 1):
            # para cada palavra analisada (não se analisa a última porque uma referência tem no mínimo 2 palavras)
            # são analisadas 10 palavras à sua frente
            for k in range(1, min(10, len(word_list) - i)):
                possivel_ref = ""
                for j in range(i, i + k + 1):
                    if word_list[i] is not None:
                        possivel_ref = possivel_ref + " " + word_list[j]
                possivel_ref.strip()
                ref = estrutura_da_biblia.get_referencia_from_str(possivel_ref)
                if ref:
                    referencias_list.append(ref)
        # vamos devolver a referência com mais versículos (no caso de haver mais que uma válida)
        if len(referencias_list) > 0:
            ref = referencias_list[0]
            for i in range(1, len(referencias_list)):
                if len(referencias_list[i].versiculos) > len(ref.versiculos):
                    ref = referencias_list[i].versiculos
            api.send_message(chat_id, str(ref))

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
