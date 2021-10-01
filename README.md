# bot-da-biblia

escreves uma frase bíblica e ele diz de onde é

escreves uma referência bíblica e ele cita

hehe

## à malta do projeto ##

**__para pôr o bot a correr é executar o ficheiro bot.py__**

----

Para definir a variável de ambiente com a nossa chave (se não se fizer isso, obviamente não dá para correr o bot)

### fish ###
adicionar ao ficheiro ~/.config/fish/config.fish a linha:

    set -gx BOT_BIBLIA_API_TOKEN "<a chave>"

### bash/zsh ###
adicionar a linha:

    export BOT_BIBLIA_API_TOKEN="<a chave>"

na bash ao ficheiro ~/.bash_profile, e no zsh ao ficheiro ~/.zshenv (acho eu. se não for então é o ~/.zshrc) 

### windows ###
se estiverem no windows, vão às definições -> sistema -> acerca de -> definições avançadas de sistema (à direita) -> (aba avançadas) variáveis de ambiente. aqui é adicionar uma nova variável de utilizador com o nome ```BOT_BIBLIA_API_TOKEN```, e no valor a nossa chave

