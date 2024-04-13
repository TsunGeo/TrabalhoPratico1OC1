import sys


def sep_imed(s):
    x = s.replace("(", "").replace(")", "").split("x")
    return x

# Separa a vírgula do rs1/rs2
def anti_x_virgula(s):
    x = s.replace(",", "").replace("x", "")
    return x

# Separa a instrução lw e sw
def sep_swlw(linha):
    vet_aux = linha.split()
    imm_rs1 = vet_aux[2]
    temp = sep_imed(vet_aux[2])
    vet_aux.pop()
    vet_aux.append(temp[0])
    vet_aux.append(temp[1])
    vet_aux[1] = vet_aux[1][1:]
    return vet_aux

# Define o opcode
def opcode(opr):
    if opr == "sub":
        return "0110011"
    if opr == "xor":
        return "0110011"
    if opr == "srl":
        return "0110011"
    if opr == "addi":
        return "0010011"
    if opr == "beq":
        return "1100011"
    if opr == "sw":
        return "0100011"
    if opr == "lw":
        return "0000011"
    return "Erro de sintaxe: opcode não reconhecido"

# Define o funct3
def funct3(opr):
    if opr == "addi":
        return "000"
    if opr == "beq":
        return "000"
    if opr == "sw":
        return "010"
    if opr == "lw":
        return "010"
    if opr == "sub":
        return "000"
    if opr == "xor":
        return "100"
    if opr == "srl":
        return "101"
    return "Erro de sintaxe: funct3 não reconhecido"

# Define o funct7
def funct7(opr):
    if opr == "sub":
        return "0100000"
    if opr == "srl":
        return "0000000"
    return "0000000"

# Soma binária
def somaBinario(a, b):
    for ch in a:
        assert ch in {'0', '1'}, 'bad digit: ' + ch
    for ch in b:
        assert ch in {'0', '1'}, 'bad digit: ' + ch
    sumx = int(a, 2) + int(b, 2)
    return bin(sumx)[2:]

# Converte para binário
def binario(num, size):
    num_str = str(num).replace(",", "")  # Remover vírgulas e outros caracteres extras
    if int(num_str) < 0:
        bin2 = "{0:b}".format(int(num_str) * (-1))
        bin1 = "0"
    else:
        bin2 = "{0:b}".format(int(num_str))
        bin1 = "0"
    for i in range(size - len(bin2) - 1):
        bin1 = bin1 + "0"
    if len(bin2) == size:
        return bin2
    bin = bin1 + bin2
    if int(num_str) < 0:
        aux = ""
        for i in range(12):
            if bin[i] == "0":
                aux += "1"
            else:
                aux += "0"
        return somaBinario(aux, "1")
    return bin


# Gera o código binário
def gerar_codigo(linha):
    if linha == "nop":
        linha = "addi x0, x0, 0"

    vet = linha.split()
    opr = vet[0]

    if opr == "sub" or opr == "xor" or opr == "srl":
        if len(vet) != 4:
            return "Erro de sintaxe: número inválido de operandos"
        if vet[1][0] != "x" or vet[2][0] != "x" or vet[3][0] != "x":
            return "Erro de sintaxe: operandos inválidos"
        characters = ",x"
        linha = ''.join(i for i in linha if i not in characters)
        vet_aux = linha.split()
        rd = vet_aux[1]
        rs1 = vet_aux[2]
        rs2 = vet_aux[3]
        code = funct7(opr) + binario(rs2, 5) + binario(rs1, 5) + funct3(opr) + binario(rd, 5) + opcode(opr)
        return code

    elif opr == "addi":
        if len(vet) != 4:
            return "Erro de sintaxe: número inválido de operandos"
        if vet[1][0] != "x" or vet[2][0] != "x" or vet[3][0] == "x":
            return "Erro de sintaxe: operandos inválidos"
        characters = ",x"
        linha = ''.join(i for i in linha if i not in characters)
        vet_aux = linha.split()
        rd = vet_aux[1]
        rs1 = vet_aux[2]
        imed = vet_aux[3]
        code = binario(imed, 12) + binario(rs1, 5) + funct3(opr) + binario(rd, 5) + opcode(opr)
        return code

    elif opr =="lw":
        aux = sep_swlw(linha)
        rd = aux[1]
        rs1 = aux[3]
        imm = aux[2]
        immbin = binario(imm, 12)
        code = immbin + binario(rs1, 5) + funct3(opr) + binario(rd, 5) + opcode(opr)
        return code

    elif opr =="beq":
        if len(vet) != 4:
            return "Erro de sintaxe: número inválido de operandos"
        if vet[1][0] != "x" or vet[2][0] != "x" or vet[3][0] == "x":
            return "Erro de sintaxe: operandos inválidos"
        characters = ",x"
        linha = ''.join(i for i in linha if i not in characters)
        vet_aux = linha.split()
        rs2 = vet_aux[1]
        rs1 = vet_aux[2]
        immbin = binario(vet_aux[3], 12)
        code = immbin[11] + immbin[5:11] + binario(rs2, 5) + binario(rs1, 5) + funct3(opr) + immbin[1:5] + immbin[10] + opcode(opr)
        return code

    elif opr == "sw":
        aux = sep_swlw(linha)
        rs2 = aux[1]
        rs1 = aux[3]
        imm = aux[2]
        immbin = binario(imm, 12)
        code = immbin[5:] + binario(rs2, 5) + binario(rs1, 5) + funct3(opr) + immbin[0:5] + opcode(opr)
        return code

    # Pseudo Instruções
    elif opr == "sv":
        if len(vet) != 3 or vet[1][0] != "x" or vet[2][0] != "x":
            return "Erro de sintaxe: número inválido de operandos ou operandos inválidos"
        characters = ",x"
        linha = ''.join(i for i in linha if i not in characters)
        vet_aux = linha.split()
        rd = vet_aux[1]
        rs1 = vet_aux[2]
        imed = "0"
        code = binario(imed, 12) + binario(rs1, 5) + funct3("addi") + binario(rd, 5) + opcode("addi")
        return code

    elif opr == "neg":
        if len(vet) != 3 or vet[1][0] != "x" or vet[2][0] != "x":
            return "Erro de sintaxe: número inválido de operandos ou operandos inválidos"
        characters = ",x"
        linha = ''.join(i for i in linha if i not in characters)
        vet_aux = linha.split()
        rd = vet_aux[1]
        rs1 = "0"
        rs2 = vet_aux[2]
        code = funct7(opr) + binario(rs2, 5) + binario(rs1, 5) + funct3("sub") + binario(rd, 5) + opcode("sub")
        return code

    elif opr == "nop":
        # A instrução 'nop' não tem operandos
        if len(vet) != 1:
            return "Erro de sintaxe: número inválido de operandos"
        # 'nop' é geralmente implementado como um 'addi' com rd, rs1 e imed todos como '0'
        rd = "0"
        rs1 = "0"
        imed = "0"
        code = binario(imed, 12) + binario(rs1, 5) + funct3("addi") + binario(rd, 5) + opcode("addi")
        return code

    else:
        return "Erro de sintaxe: instrução não reconhecida"

# Leitura do Arquivo e chamada das funções
if len(sys.argv) == 1:
    Arq1 = input("Digite o nome do arquivo a ser traduzido:\n")
    Entrada = open(Arq1, "r")
    saida = open("saida.txt", "w")
    opcao = int(input("Deseja que o codigo seja mostrado na tela?\n1 - Sim\n0 - Nao.\n"))
    if not (opcao == 0 or opcao == 1):
        print("Opção inexistente. Favor escolher outra.")
else:
    Entrada = open(sys.argv[1], "r")
    saida = open(sys.argv[3], "w")
    opcao = 0

for linha in Entrada:
    code = gerar_codigo(linha)
    saida.write(str(code) + "\n")  # Convertendo para string antes de escrever no arquivo
    if opcao:
        print(code)

Entrada.close()
saida.close()