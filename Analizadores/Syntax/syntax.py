# ------------------------------------------------------------ 
# parser.py
# Analizador Sintáctico usando PLY.Yacc
# Grupo 10
# ------------------------------------------------------------

import ply.yacc as yacc
import sys
import datetime
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Lexicon.lexer import tokens, get_git_user
# ------------------------------------------------------------
# Integrantes:
#   Derian Baque Choez (fernan0502)
#   Sebastian Holguin (Sebhvarg)
#   Carlos Ronquillo (carrbrus)
# ------------------------------------------------------------

mensajes = [] #Guarda los errores

# ------------------------------------------------------------   
def p_programa(p):
    '''programa : instrucciones
                | programa instrucciones
                '''
       
def p_instrucciones(p):
    '''instrucciones : asignacion
                 | imprimir
                 | funcion
                 | estructura_control
                 | bloque
                 | llamada_funcion
                 | expresion_sin_puntocoma
                 | clase
                 ''' 
#sombrado
def p_bloque(p):
    '''bloque : LLAVE_IZQ programa LLAVE_DER
    '''

def p_bloque_con_retorno(p):
    '''bloque_con_retorno : LLAVE_IZQ programa LLAVE_DER
    '''

def p_expresion_sin_puntocoma(p):
    '''expresion_sin_puntocoma : operacion_aritmetica
                               | valor_numerico
                               | IDENTIFICADOR
    '''
    
# ------------------------------------------------------------
# Reglas de la gramática (Derian + Sebastian)
def p_asignacion(p):
    '''asignacion : VARIABLE IDENTIFICADOR IGUAL valor PUNTOCOMA
                    | IDENTIFICADOR IGUAL valor PUNTOCOMA                    
    '''
def p_asignacion_mutable(p):
    '''asignacion : VARIABLE MUTABLE IDENTIFICADOR IGUAL valor PUNTOCOMA'''
def p_asignacion_constante(p):
    '''asignacion : CONSTANTE IDENTIFICADOR IGUAL valor PUNTOCOMA'''
def p_asignacion_explicita_valor(p):
    '''asignacion : VARIABLE IDENTIFICADOR DOSPUNTOS tipo_dato IGUAL valor PUNTOCOMA
    '''
    
def  p_valor(p):
    '''valor : CADENA
             | CARACTER
             | BOOLEANO
             | IDENTIFICADOR
             | asignacion 
             | valor_numerico
             | operacion_aritmetica
             | tupla
             | matriz
             | llamada_funcion_sin_puntocoma
             | bloque_con_retorno'''

def p_valor_booleano(p):
    '''valor : VERDAD
             | FALSO'''

def p_valor_numerico(p):
    '''valor_numerico : ENTERO
                      | FLOTANTE'''
    p[0] = p[1]

def p_tipo_dato(p):
    '''tipo_dato : ITIPO
                 | I8
                 | I16
                 | I32
                 | I64
                 | I128
                 | U8
                 | U16
                 | U32
                 | U64
                 | U128
                 | F32
                 | F64
                 | BOOLEANO_TIPO
                 | CARACTER_TIPO
                 | CADENA_TIPO
                 | UTIPO
                 | IDENTIFICADOR
                 
    '''


def p_valor_operacionAritmetica(p):
    '''operacion_aritmetica : valor operador_aritmetico valor
    | repite_operacion_aritmetica 
    
    
    '''
    
def p_operador_aritmetico(p):
    '''operador_aritmetico : SUMA
                           | RESTA
                           | MULT
                           | DIV
                           | MODULO'''

def p_repite_operacionAritmetica(p):
    '''repite_operacion_aritmetica : operacion_aritmetica 
                                    | operacion_aritmetica operador_aritmetico valor_numerico'''
def p_expresion_booleana(p):
    '''expresion_booleana : valor operador_relacional valor    
    '''

def p_operador_relacional(p):
    '''operador_relacional : MAYOR
                           | MENOR
                           | MAYOR_IGUAL
                           | MENOR_IGUAL
                           | IGUALDOBLE
                           | DIFERENTE'''
# ------------------ Funciones ------------------
def p_imprimir(p):
    '''imprimir : IMPRIMIR PAREN_IZQ repite_valores PAREN_DER PUNTOCOMA
    | IMPRIMIRLN PAREN_IZQ repite_valores PAREN_DER PUNTOCOMA
    '''

def p_imprimir_sin_puntocoma(p):
    '''imprimir_sin_puntocoma : IMPRIMIR PAREN_IZQ repite_valores PAREN_DER
                              | IMPRIMIRLN PAREN_IZQ repite_valores PAREN_DER
    '''
    
def p_repite_valores(p):
    '''repite_valores : valor
                      | valor COMA repite_valores'''
def p_funcion(p):
    '''funcion : FUNCION IDENTIFICADOR PAREN_IZQ PAREN_DER LLAVE_IZQ programa LLAVE_DER
               | FUNCION IDENTIFICADOR PAREN_IZQ PAREN_DER FLECHA tipo_dato LLAVE_IZQ programa LLAVE_DER
    '''

def p_funcion_parametros(p):
    '''funcion : FUNCION IDENTIFICADOR PAREN_IZQ parametros PAREN_DER LLAVE_IZQ programa LLAVE_DER
               | FUNCION IDENTIFICADOR PAREN_IZQ parametros PAREN_DER FLECHA tipo_dato LLAVE_IZQ programa LLAVE_DER
    '''

def p_parametros(p):
    '''parametros : IDENTIFICADOR
                  | IDENTIFICADOR COMA parametros
                  | IDENTIFICADOR DOSPUNTOS tipo_dato 
                  | IDENTIFICADOR DOSPUNTOS tipo_dato COMA parametros
    '''

def p_llamada_funcion(p):
    '''llamada_funcion : IDENTIFICADOR PAREN_IZQ PAREN_DER PUNTOCOMA
                       | IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER PUNTOCOMA
    '''

def p_llamada_funcion_sin_puntocoma(p):
    '''llamada_funcion_sin_puntocoma : IDENTIFICADOR PAREN_IZQ PAREN_DER
                                     | IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER
    '''
def p_retorno_funcion(p):
    '''instrucciones : RETORNO valor PUNTOCOMA
    '''
# -------- Estructuras de datos ----------------------

def p_estructura_datos(p):
    '''estructura_datos : tupla
                        | matriz
                        | vector
    '''
def p_tupla(p):
    '''tupla : PAREN_IZQ repite_valores PAREN_DER
            | PAREN_IZQ PAREN_DER
            | PAREN_IZQ repite_valores COMA tupla PAREN_DER
    '''
def p_tupla_acceso(p):
    '''valor : IDENTIFICADOR PUNTO ENTERO
    '''

def p_tupla_asignacion(p):
    '''asignacion : VARIABLE IDENTIFICADOR IGUAL tupla PUNTOCOMA
    | VARIABLE MUTABLE IDENTIFICADOR IGUAL tupla PUNTOCOMA
    | IDENTIFICADOR IGUAL tupla PUNTOCOMA
    '''
def p_matriz(p):
    '''matriz : CORCHETE_IZQ repite_valores CORCHETE_DER
              | CORCHETE_IZQ CORCHETE_DER
    '''

def p_matriz_asignacion(p):
    '''asignacion : VARIABLE IDENTIFICADOR IGUAL matriz PUNTOCOMA
                  | VARIABLE MUTABLE IDENTIFICADOR IGUAL matriz PUNTOCOMA
                  | IDENTIFICADOR IGUAL matriz PUNTOCOMA
    '''
def p_matriz_acceso(p):
    '''valor : IDENTIFICADOR CORCHETE_IZQ ENTERO CORCHETE_DER
    '''
def p_matriz_acceso_doble(p):
    '''valor : IDENTIFICADOR CORCHETE_IZQ ENTERO CORCHETE_DER CORCHETE_IZQ ENTERO CORCHETE_DER
    '''
def p_matriz_acceso_triple(p):
    '''valor : IDENTIFICADOR CORCHETE_IZQ ENTERO CORCHETE_DER CORCHETE_IZQ ENTERO CORCHETE_DER CORCHETE_IZQ ENTERO CORCHETE_DER
    '''
def p_clase(p):
    '''clase : ESTRUCTURA IDENTIFICADOR LLAVE_IZQ atributos_clase LLAVE_DER
    '''
def p_clase_con_metodos(p):
    '''clase : ESTRUCTURA IDENTIFICADOR LLAVE_IZQ atributos_clase metodo_clase LLAVE_DER PUNTOCOMA
    '''
def p_metodo_clase(p):
    '''metodo_clase : FUNCION IDENTIFICADOR PAREN_IZQ PAREN_DER LLAVE_IZQ programa LLAVE_DER
                   | FUNCION IDENTIFICADOR PAREN_IZQ PAREN_DER FLECHA tipo_dato LLAVE_IZQ programa LLAVE_DER
                   | FUNCION IDENTIFICADOR PAREN_IZQ parametros PAREN_DER LLAVE_IZQ programa LLAVE_DER
                   | FUNCION IDENTIFICADOR PAREN_IZQ parametros PAREN_DER FLECHA tipo_dato LLAVE_IZQ programa LLAVE_DER
    '''
def p_atributos_clase(p):
    '''atributos_clase : IDENTIFICADOR DOSPUNTOS tipo_dato COMA
                      | MUTABLE IDENTIFICADOR DOSPUNTOS tipo_dato COMA
                      | atributos_clase IDENTIFICADOR DOSPUNTOS tipo_dato COMA
                      | atributos_clase MUTABLE IDENTIFICADOR DOSPUNTOS tipo_dato COMA
    '''
def p_instanciar_clase(p):
    '''valor : IDENTIFICADOR DOSPUNTOS DOSPUNTOS NUEVO PAREN_IZQ PAREN_DER
    '''
def p_eliminar_clase(p):
    '''instrucciones : ELIMINAR IDENTIFICADOR PUNTOCOMA
    '''
def p_acceso_atributo_clase(p):
    '''valor : IDENTIFICADOR PUNTO IDENTIFICADOR
    '''
def p_asignacion_atributo_clase(p):
    '''asignacion : IDENTIFICADOR PUNTO IDENTIFICADOR IGUAL valor PUNTOCOMA
    '''
def p_llamada_metodo_clase(p):
    '''valor : IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ PAREN_DER
             | IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER
    '''
def p_asignacion_metodo_clase(p):
    '''asignacion : IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ PAREN_DER PUNTOCOMA
                  | IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER PUNTOCOMA
    '''
def p_vector(p):
    '''vector : VECTOR_MACRO CORCHETE_IZQ repite_valores CORCHETE_DER 
                | vectorvacio
                
    '''
def p_vector_vacio(p):
    '''vectorvacio : VECTOR MENOR tipo_dato MAYOR IGUAL VECTOR DOSPUNTOS DOSPUNTOS NUEVO PAREN_IZQ PAREN_DER 
    '''
def p_asignacion_vector_vacio(p):
    '''asignacion : VARIABLE IDENTIFICADOR DOSPUNTOS vectorvacio PUNTOCOMA
    '''
    
    
def p_vector_valor_repetido(p):
    '''vector : VECTOR_MACRO CORCHETE_IZQ ENTERO PUNTOCOMA valor CORCHETE_DER 
    '''

def p_asignacion_vector(p):
    '''asignacion : VARIABLE IDENTIFICADOR IGUAL vector PUNTOCOMA
    '''
    
# ------------------------------------------------------------

# ------- Estructuras de control ----------------------
def p_estructura_control(p):
    '''estructura_control : condicional_if
                         | ciclo_while
                         | ciclo_for
                         | match_case
    '''

def p_condicional_if(p):
    '''condicional_if : SI PAREN_IZQ expresion_booleana PAREN_DER LLAVE_IZQ programa LLAVE_DER
                        | SI PAREN_IZQ expresion_booleana PAREN_DER LLAVE_IZQ programa LLAVE_DER SINO LLAVE_IZQ programa LLAVE_DER
                        | SI PAREN_IZQ expresion_booleana PAREN_DER LLAVE_IZQ programa LLAVE_DER condicional_elif
    '''
def p_condicional_elif(p):
    '''condicional_elif : SINO SI PAREN_IZQ expresion_booleana PAREN_DER LLAVE_IZQ programa LLAVE_DER
                        | SINO SI PAREN_IZQ expresion_booleana PAREN_DER LLAVE_IZQ programa LLAVE_DER condicional_elif
                        | SINO SI PAREN_IZQ expresion_booleana PAREN_DER LLAVE_IZQ programa LLAVE_DER SINO LLAVE_IZQ programa LLAVE_DER
    '''
def p_ciclo_while(p):
    'ciclo_while : MIENTRAS PAREN_IZQ expresion_booleana PAREN_DER LLAVE_IZQ programa LLAVE_DER'
def p_ciclo_for(p):
    'ciclo_for : POR PAREN_IZQ asignacion expresion_booleana PUNTOCOMA asignacion_incremento PAREN_DER LLAVE_IZQ programa LLAVE_DER'
def p_asignacion_incremento(p):
    '''asignacion_incremento : IDENTIFICADOR MAS_IGUAL ENTERO
                                | IDENTIFICADOR MENOS_IGUAL ENTERO
                                | IDENTIFICADOR SUMA SUMA
                                | IDENTIFICADOR RESTA RESTA
                                | IDENTIFICADOR IGUAL IDENTIFICADOR SUMA ENTERO
                
    '''
def p_continue_break(p):
    '''instrucciones : CONTINUAR PUNTOCOMA
                    | QUIEBRE PUNTOCOMA
    '''

def p_match_case(p):
    '''match_case : COINCIDIR IDENTIFICADOR LLAVE_IZQ brazos_match LLAVE_DER
                  | COINCIDIR IDENTIFICADOR LLAVE_IZQ brazos_match COMA LLAVE_DER
    '''

def p_brazos_match(p):
    '''brazos_match : brazo_match
                    | brazos_match COMA brazo_match
    '''

def p_brazo_match(p):
    '''brazo_match : patron FLECHA_DOBLE expresion_match
                   | patron FLECHA_DOBLE bloque_match
    '''

def p_bloque_match(p):
    '''bloque_match : LLAVE_IZQ programa LLAVE_DER
    '''

def p_patron(p):
    '''patron : valor
              | GUION_BAJO
    '''

def p_expresion_match(p):
    '''expresion_match : llamada_funcion_sin_puntocoma
                       | imprimir_sin_puntocoma
                       | valor
    '''



# ------------------------------------------------------------
    
# Error rule for syntax errors
def p_error(p):
    if not p:
        mensaje_error = "Error sintáctico: fin de archivo inesperado. Puede faltar cerrar un bloque o una declaración"
        print(mensaje_error)
        mensajes.append(mensaje_error)
        return
    
    # Obtener información del token
    token_value = p.value
    token_type = p.type
    lineno = p.lineno
    
    # Generar mensajes de error específicos según el tipo de token
    mensaje_error = f"Error sintáctico en la línea {lineno}: "
    
    # Errores comunes de puntuación
    if token_type == 'PUNTOCOMA':
        mensaje_error += f"punto y coma inesperado '{token_value}'"
    elif token_type == 'LLAVE_DER':
        mensaje_error += f"llave de cierre '}}' inesperada. Posible llave de apertura faltante o estructura mal formada"
    elif token_type == 'LLAVE_IZQ':
        mensaje_error += f"llave de apertura '{{' inesperada. Revise la sintaxis de la declaración anterior"
    elif token_type == 'PAREN_DER':
        mensaje_error += f"paréntesis de cierre ')' inesperado. Posible paréntesis de apertura faltante"
    elif token_type == 'PAREN_IZQ':
        mensaje_error += f"paréntesis de apertura '(' inesperado. Revise la sintaxis"
    elif token_type == 'CORCHETE_DER':
        mensaje_error += f"corchete de cierre ']' inesperado. Posible corchete de apertura faltante"
    elif token_type == 'CORCHETE_IZQ':
        mensaje_error += f"corchete de apertura '[' inesperado. Revise la sintaxis del array o vector"
    
    # Errores de operadores
    elif token_type in ['SUMA', 'RESTA', 'MULT', 'DIV', 'MODULO']:
        mensaje_error += f"operador aritmético '{token_value}' inesperado. Revise la expresión"
    elif token_type in ['IGUAL', 'MAS_IGUAL', 'MENOS_IGUAL']:
        mensaje_error += f"operador de asignación '{token_value}' inesperado. Posible falta de identificador o valor"
    elif token_type in ['MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'IGUALDOBLE', 'DIFERENTE']:
        mensaje_error += f"operador relacional '{token_value}' inesperado. Revise la expresión booleana"
    
    # Errores de palabras reservadas
    elif token_type in ['VARIABLE', 'MUTABLE', 'CONSTANTE']:
        mensaje_error += f"palabra reservada '{token_value}' en posición incorrecta. Revise la sintaxis de declaración"
    elif token_type == 'FUNCION':
        mensaje_error += f"palabra reservada 'fn' inesperada. Revise la sintaxis de la función"
    elif token_type in ['SI', 'SINO', 'MIENTRAS', 'POR']:
        mensaje_error += f"palabra reservada '{token_value}' en posición incorrecta. Revise la estructura de control"
    elif token_type == 'COINCIDIR':
        mensaje_error += f"palabra reservada 'match' inesperada. Revise la sintaxis del match"
    elif token_type == 'FLECHA_DOBLE':
        mensaje_error += f"operador '=>' inesperado. Solo puede usarse dentro de expresiones match"
    elif token_type == 'RETORNO':
        mensaje_error += f"palabra reservada 'return' inesperada. Solo puede usarse dentro de funciones"
    elif token_type in ['CONTINUAR', 'QUIEBRE']:
        mensaje_error += f"palabra reservada '{token_value}' inesperada. Solo puede usarse dentro de ciclos"
    elif token_type == 'ESTRUCTURA':
        mensaje_error += f"palabra reservada 'struct' inesperada. Revise la sintaxis de la clase"
    
    # Errores de identificadores y valores
    elif token_type == 'IDENTIFICADOR':
        mensaje_error += f"identificador '{token_value}' inesperado. Puede faltar un operador o declaración"
    elif token_type == 'ENTERO':
        mensaje_error += f"valor entero '{token_value}' inesperado. Revise la expresión o asignación"
    elif token_type == 'FLOTANTE':
        mensaje_error += f"valor flotante '{token_value}' inesperado. Revise la expresión o asignación"
    elif token_type == 'CADENA':
        mensaje_error += f"cadena '{token_value}' inesperada. Revise el contexto de uso"
    elif token_type == 'CARACTER':
        mensaje_error += f"carácter '{token_value}' inesperado. Revise el contexto de uso"
    
    # Errores de tipos de datos
    elif token_type in ['I8', 'I16', 'I32', 'I64', 'I128', 'U8', 'U16', 'U32', 'U64', 'U128', 'F32', 'F64', 
                        'BOOLEANO_TIPO', 'CARACTER_TIPO', 'CADENA_TIPO', 'ITIPO', 'UTIPO']:
        mensaje_error += f"tipo de dato '{token_value}' inesperado. Revise la declaración de variable o función"
    
    # Otros símbolos
    elif token_type == 'COMA':
        mensaje_error += f"coma ',' inesperada. Revise la lista de parámetros o valores"
    elif token_type == 'DOSPUNTOS':
        mensaje_error += f"dos puntos ':' inesperados. Revise la sintaxis de declaración de tipo"
    elif token_type == 'PUNTO':
        mensaje_error += f"punto '.' inesperado. Revise el acceso a atributos o métodos"
    elif token_type == 'FLECHA':
        mensaje_error += f"flecha '->' inesperada. Revise la sintaxis de retorno de función"
    
    # Error genérico
    else:
        mensaje_error += f"token inesperado '{token_value}' de tipo {token_type}"
    
    print(mensaje_error)
    print(f"  Token completo: {p}")
    mensajes.append(mensaje_error)
        
# ------------------------------------------------------------
# Función para registrar los tokens en un archivo de log
def log_token(mensaje):
    usuario = get_git_user()
    fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, f"sintactico-{usuario}-{fecha_hora}.txt")
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(mensaje + "\n")
    

# Build the parser
parser = yacc.yacc()

if __name__ == "__main__":
    print("Analizador sintáctico ARust \n")
    if len(sys.argv) > 1:
        archivo_entrada = sys.argv[1]
    else:
        archivo_entrada = input("Ingrese el nombre del archivo de entrada: ").strip()
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
            datos = archivo.read()

        # Crear el archivo de log desde el inicio
        log_token("Inicio análisis sintáctico del archivo: " + archivo_entrada)

        # Ejecutar análisis sintáctico
        parser.parse(datos)
        

        while True:
            if not mensajes:
                print("Análisis sintáctico completado sin errores.")
                log_token("Análisis sintáctico completado sin errores.")
                break
            else:
                for mensaje in mensajes:
                    log_token(mensaje)
                break

        print("\nTokens registrados en archivo de log.")
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no fue encontrado.")

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no fue encontrado.")
        
        