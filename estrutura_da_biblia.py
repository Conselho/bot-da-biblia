import json

json_file = open("biblia.json")
json_str = json_file.read()
biblia = json.loads(json_str)


class ReferenciaBiblica:
    falsy_livro = ""
    falsy_capitulo = 0
    falsy_lista_versiculos = set()

    def __init__(self, livro: str, capitulo: int, versiculos: set[int]):
        self.livro = livro
        self.capitulo = capitulo
        self.versiculos = versiculos

    def __bool__(self):
        return self.livro != "" and self.capitulo != 0

    def __str__(self):
        if len(self.versiculos) == 0:
            return self.livro + " " + str(self.capitulo)
        else:
            versiculos_str = str(self.versiculos)  # TODO melhor apresentação dos versículos
            return self.livro + " " + str(self.capitulo) + ":" + versiculos_str

    def __eq__(self, other):
        if type(other) == ReferenciaBiblica:
            return self.livro == other.livro and self.capitulo == other.capitulo and self.versiculos == other.versiculos
        else:
            return False


referencia_false = ReferenciaBiblica(ReferenciaBiblica.falsy_livro, ReferenciaBiblica.falsy_capitulo, ReferenciaBiblica.falsy_lista_versiculos)


def get_nomes_alternativos(nome_livro: str) -> [str]:
    return biblia[nome_livro]["nomes alternativos"]


def get_capitulos(nome_livro: str) -> [int]:
    return biblia[nome_livro]["capitulos"]


def abreviatura_from_str(nome: str) -> str:
    """
    Verifica se um livro existe na Bíblia, dado o seu nome. São verificadas todas as abreviaturas e nomes alternativos
    de cada livro.
    :param nome: abreviatura ou nome alternativo do livro
    :return: a key do livro se ele for encontrado, ou uma string de valor False se não for encontrado
    """
    for key in biblia:
        if key.lower() == nome.lower():
            return key
        else:
            for nome_alternativo in biblia[key]["nomes_alternativos"]:
                if nome.lower() == nome_alternativo.lower():
                    return key
    return ""


def capitulo_existe(nome: str, cap: int) -> bool:
    """
    verifica se um capítulo existe
    :rtype: False se o capítulo não existir, True se existir
    """
    if nome in biblia:  # evitar chamar a função mais temporalmente complexa
        abreviatura = nome
    else:
        abreviatura = abreviatura_from_str(nome)
    if abreviatura:
        return 1 <= cap <= len(biblia[abreviatura]["capitulos"])
    else:
        return False


def versiculo_existe(nome: str, cap: int, ver: int) -> bool:
    """
    Verifica se o versículo existe no capítulo dado do livro dado.
    :param nome: nome do livro
    :param cap: capítulo do versículo
    :param ver: número do versículo
    :return: bool True se o versículo existe, e false se não existe
    """
    if nome in biblia:  # evitar chamar a função mais temporalmente complexa
        abreviatura = nome
    else:
        abreviatura = abreviatura_from_str(nome)
    if abreviatura:
        try:
            return 1 <= ver <= biblia[abreviatura]["capitulos"][cap-1]
        except KeyError or IndexError:
            return False  # o capítulo não existia
    else:
        return False


def get_referencia_from_str(ref: str) -> ReferenciaBiblica:
    """
    Verifica se uma referência é válida e se for retorna-a sob o formato de objeto ReferenciaBiblica.
    Uma referência pode ter estes formatos:
        <l> <c>
        <l> <c>, <v>
        <l> <c>, <v_inicial>-<v_final> (intervalo de versículos)
        <l> <c>, <v>.[...].<v_inicial>-<v_final>.[...] (conjunto de versículos e intervalos de versículos)
        <l> <c>:<v>
        <l> <c>:<v_inicial>-<v_final> (intervalo de versículos)
        <l> <c>:<v>.[...].<v_inicial>-<v_final>.[...] (conjunto de versículos e intervalos de versículos)

    :param ref: referência em str
    :return: um objeto de ReferenciaBiblica se tiver sido válida, ou um objeto com valor False se não
    """
    # verificar qual é o caractere de divisão
    split_virgulas = ref.strip().split(',')
    split_colon = ref.strip().split(':')
    if len(split_virgulas) == 2 and len(split_colon) != 2:
        split = split_virgulas
    elif len(split_colon) == 2 and len(split_virgulas) != 2:
        split = split_colon
    else:
        split = [ref.strip()]  # <l> <c>

    # analisar lado esquerdo do caractere de divisão
    lado_esquerdo = split[0].split(' ')
    nome_livro = ' '.join(lado_esquerdo[0:len(lado_esquerdo) - 1])
    abreviatura = abreviatura_from_str(nome_livro)
    if not abreviatura:
        return referencia_false
    capitulo = int(lado_esquerdo[len(lado_esquerdo) - 1])
    if not capitulo_existe(abreviatura, capitulo):
        return referencia_false

    versiculos = set()
    # analisar lado direito do caractere de divisão
    if len(split) > 1:
        lado_direito = split[1].strip()
        conjunto = lado_direito.split('.')
        for e in conjunto:
            try:
                # adicionar o número
                n_versiculo = int(e)
                if versiculo_existe(abreviatura, capitulo, n_versiculo):
                    versiculos.add(n_versiculo)
            except ValueError:
                # adicionar o intervalo de versículos
                intervalo = e.split('-')
                if len(intervalo) != 2:  # tem de ter 2 e só 2 valores
                    continue
                try:
                    inicial = int(intervalo[0])
                    final = int(intervalo[1])
                except ValueError:  # têm de ser dois números
                    continue
                if final < inicial:
                    continue
                # adicionar cada versículo
                for n_versiculo in range(inicial, final + 1):
                    if versiculo_existe(abreviatura, capitulo, n_versiculo):
                        versiculos.add(n_versiculo)

    return ReferenciaBiblica(abreviatura, capitulo, versiculos)
