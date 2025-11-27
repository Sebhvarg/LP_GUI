# ------------------------------------------------------------ 
# parser.py
# Analizador Semantico usando PLY.Yacc
# Grupo 10
# ------------------------------------------------------------
# Integrantes:
#   Derian Baque Choez (fernan0502)
#   Sebastian Holguin (Sebhvarg)
#   Carlos Ronquillo (carrbrus)
# ------------------------------------------------------------
import ply.yacc as yacc
import sys
import datetime
import os
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Lexicon.lexer import lexer, tokens, get_git_user
from Syntax.syntax import *

mensajes = []
# ------------------------------------------------------------
# Tabla de Símbolos
tabla_simbolos = {
    "variables": {},
    "funciones": {},
    "tipos": {
        "str-funciones": [
            "len", "push", "contains", "starts_with", 
            "ends_with", "index_of", "to_uppercase", 
            "to_lowercase", "replace", "substring",
            "split", "trim", "chars", "is_empty",
            "concat", "parse", "count"
        ],
        "num-funciones": [
            "to_string", "to_le", "to_be", "to_ne",
            "swap_bytes", "to_be_bytes", "to_le_bytes",
            "to_ne_bytes",
            "abs", "signum",
            "pow", "saturating_add", "saturating_sub",
            "saturating_mul",
            "max", "min", "clamp",
            "sqrt", "round", "floor", "ceil", "trunc",
            "fract", "abs", "powi", "powf",
            "sin", "cos", "tan", "log", "log10", "log2",
            "exp", "exp2"
        ],
        "tipos_numericos": [
            "i8", "i16", "i32", "i64", "i128",
            "u8", "u16", "u32", "u64", "u128",
            "f32", "f64", "isize", "usize"
        ],
        "tipos_primitivos": ["bool", "char", "str"],
    },
    "clases": {}, 
    "scope_actual": "global",
    "scopes": {"global": {}}
}

# Especificaciones de métodos de string: número de argumentos y tipo de retorno esperado
metodos_str_especificaciones = {
    "len": {"args": 0, "ret": "usize"},
    "push": {"args": 1, "ret": "str"},
    "contains": {"args": 1, "ret": "bool"},
    "starts_with": {"args": 1, "ret": "bool"},
    "ends_with": {"args": 1, "ret": "bool"},
    "index_of": {"args": 1, "ret": "isize"},
    "to_uppercase": {"args": 0, "ret": "str"},
    "to_lowercase": {"args": 0, "ret": "str"},
    "replace": {"args": 2, "ret": "str"},
    "substring": {"args": 2, "ret": "str"},
    "split": {"args": 1, "ret": "vector"},
    "trim": {"args": 0, "ret": "str"},
    "chars": {"args": 0, "ret": "vector"},
    "is_empty": {"args": 0, "ret": "bool"},
    "concat": {"args": 1, "ret": "str"},
    "parse": {"args": 0, "ret": "int"},  # simplificación
    "count": {"args": 1, "ret": "usize"},
}

# Especificaciones de métodos numéricos: número de argumentos y tipo de retorno esperado
metodos_num_especificaciones = {
    "to_string": {"args": 0, "ret": "str"},
    "to_le": {"args": 0, "ret": "int"},
    "to_be": {"args": 0, "ret": "int"},
    "to_ne": {"args": 0, "ret": "int"},
    "swap_bytes": {"args": 0, "ret": "int"},
    "to_be_bytes": {"args": 0, "ret": "vector"},
    "to_le_bytes": {"args": 0, "ret": "vector"},
    "to_ne_bytes": {"args": 0, "ret": "vector"},
    "abs": {"args": 0, "ret": "int"},
    "signum": {"args": 0, "ret": "int"},
    "pow": {"args": 1, "ret": "int"},
    "saturating_add": {"args": 1, "ret": "int"},
    "saturating_sub": {"args": 1, "ret": "int"},
    "saturating_mul": {"args": 1, "ret": "int"},
    "max": {"args": 1, "ret": "int"},
    "min": {"args": 1, "ret": "int"},
    "clamp": {"args": 2, "ret": "int"},
    "sqrt": {"args": 0, "ret": "float"},
    "round": {"args": 0, "ret": "int"},
    "floor": {"args": 0, "ret": "float"},
    "ceil": {"args": 0, "ret": "float"},
    "trunc": {"args": 0, "ret": "float"},
    "fract": {"args": 0, "ret": "float"},
    "powi": {"args": 1, "ret": "float"},
    "powf": {"args": 1, "ret": "float"},
    "sin": {"args": 0, "ret": "float"},
    "cos": {"args": 0, "ret": "float"},
    "tan": {"args": 0, "ret": "float"},
    "log": {"args": 1, "ret": "float"},
    "log10": {"args": 0, "ret": "float"},
    "log2": {"args": 0, "ret": "float"},
    "exp": {"args": 0, "ret": "float"},
    "exp2": {"args": 0, "ret": "float"},
}

# Funciones auxiliares para validación semántica
def son_tipos_compatibles(tipo1, tipo2):
    """Verifica si dos tipos son compatibles para operaciones"""
    if tipo1 == tipo2:
        return True
    tipos_num = tabla_simbolos["tipos"]["tipos_numericos"]
    # Permitir operaciones entre tipos numéricos similares
    if tipo1 in tipos_num and tipo2 in tipos_num:
        # Enteros con enteros, flotantes con flotantes
        if (tipo1 in ["f32", "f64"]) == (tipo2 in ["f32", "f64"]):
            return True
    return False

def obtener_tipo_variable(nombre):
    """Obtiene el tipo de una variable declarada"""
    if nombre in tabla_simbolos["variables"]:
        info = tabla_simbolos["variables"][nombre]
        if isinstance(info, dict):
            return info.get("tipo")
        return info
    return None

def es_tipo_numerico(tipo):
    """Verifica si un tipo es numérico"""
    return tipo in tabla_simbolos["tipos"]["tipos_numericos"] or tipo in ["int", "float"]

def marcar_variable_usada(nombre):
    """Marca una variable como usada"""
    if nombre in tabla_simbolos["variables"]:
        info = tabla_simbolos["variables"][nombre]
        if isinstance(info, dict):
            info["usado"] = True

def p_asignacion(p):
    '''asignacion : VARIABLE IDENTIFICADOR IGUAL valor PUNTOCOMA
                    | IDENTIFICADOR IGUAL valor PUNTOCOMA'''
    # REGLA 1: Declaración de variable inmutable (let x = valor)
    if len(p) == 6 and p.slice[1].type == 'VARIABLE':
        nombre = p[2]
        tipo_var = p[4]
        
        # Verificar que no exista ya en el scope actual
        if nombre in tabla_simbolos["variables"]:
            mensaje = f"Error semántico: Variable '{nombre}' ya fue declarada previamente."
            print(mensaje)
            mensajes.append(mensaje)
        elif tipo_var is not None:
            tabla_simbolos["variables"][nombre] = {
                "tipo": tipo_var, 
                "const": False, 
                "mutable": False,
                "usado": False
            }
    
    # REGLA 2: Reasignación de variable existente
    elif len(p) == 5 and p.slice[1].type == 'IDENTIFICADOR':
        nombre = p[1]
        nuevo_tipo = p[3]
        
        if nombre not in tabla_simbolos["variables"]:
            mensaje = f"Error semántico: Variable '{nombre}' no ha sido declarada."
            print(mensaje)
            mensajes.append(mensaje)
        else:
            info = tabla_simbolos["variables"][nombre]
            
            # REGLA 3: No se puede reasignar constantes
            if isinstance(info, dict) and info.get("const", False):
                mensaje = f"Error semántico: No se puede modificar la constante '{nombre}'."
                print(mensaje)
                mensajes.append(mensaje)
            
            # REGLA 4: No se puede reasignar variables inmutables (let sin mut)
            elif isinstance(info, dict) and not info.get("mutable", False) and not info.get("const", False):
                mensaje = f"Error semántico: No se puede reasignar la variable inmutable '{nombre}'. Use 'let mut' para variables mutables."
                print(mensaje)
                mensajes.append(mensaje)
            
            # REGLA 5: Verificar compatibilidad de tipos en reasignación
            elif nuevo_tipo is not None and isinstance(info, dict):
                tipo_actual = info.get("tipo")
                if tipo_actual and not son_tipos_compatibles(tipo_actual, nuevo_tipo):
                    mensaje = f"Error semántico: Tipo incompatible en reasignación de '{nombre}'. Se esperaba '{tipo_actual}', se recibió '{nuevo_tipo}'."
                    print(mensaje)
                    mensajes.append(mensaje)

# REGLA 6: Declaración de variable mutable (let mut)
def p_asignacion_mutable(p):
    'asignacion : VARIABLE MUTABLE IDENTIFICADOR IGUAL valor PUNTOCOMA'
    nombre = p[3]
    tipo_var = p[5]
    
    if nombre in tabla_simbolos["variables"]:
        mensaje = f"Error semántico: Variable '{nombre}' ya fue declarada previamente."
        print(mensaje)
        mensajes.append(mensaje)
    elif tipo_var is not None:
        tabla_simbolos["variables"][nombre] = {
            "tipo": tipo_var,
            "const": False,
            "mutable": True,
            "usado": False
        }

# REGLA 7: Declaración de constante
def p_asignacion_constante(p):
    'asignacion : CONSTANTE IDENTIFICADOR IGUAL valor PUNTOCOMA'
    nombre = p[2]
    tipo_var = p[4]
    
    if nombre in tabla_simbolos["variables"]:
        mensaje = f"Error semántico: Constante '{nombre}' ya fue declarada previamente."
        print(mensaje)
        mensajes.append(mensaje)
    elif tipo_var is not None:
        tabla_simbolos["variables"][nombre] = {
            "tipo": tipo_var,
            "const": True,
            "mutable": False,
            "usado": False
        }

# REGLA 8: Declaración explícita con tipo (hook semántico, no redefinir gramática)
def p_asignacion_explicita_valor(p):
    'asignacion : VARIABLE IDENTIFICADOR DOSPUNTOS tipo_dato IGUAL valor PUNTOCOMA'
    nombre = p[2]
    tipo_declarado = p[4]
    tipo_valor = p[6]
    
    if nombre in tabla_simbolos["variables"]:
        mensaje = f"Error semántico: Variable '{nombre}' ya fue declarada previamente."
        print(mensaje)
        mensajes.append(mensaje)
    elif tipo_valor is not None and not son_tipos_compatibles(tipo_declarado, tipo_valor):
        mensaje = f"Error semántico: Tipo incompatible. Variable '{nombre}' declarada como '{tipo_declarado}' pero recibe '{tipo_valor}'."
        print(mensaje)
        mensajes.append(mensaje)
    else:
        tabla_simbolos["variables"][nombre] = {
            "tipo": tipo_declarado,
            "const": False,
            "mutable": False,
            "usado": False
        }
            
def p_valor(p):
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
     if isinstance(p[1], str) and p.slice[1].type == 'CADENA':
         p[0] = "str"
     elif isinstance(p[1], bool) and p.slice[1].type == 'BOOLEANO':
            p[0] = "bool"
     elif p.slice[1].type == 'CARACTER':
         p[0] = "char"
     elif isinstance(p[1], int):
         p[0] = "int"
     elif isinstance(p[1], float):
            p[0] = "float"
     elif p.slice[1].type == 'IDENTIFICADOR':
         nombre = p[1]
         if nombre in tabla_simbolos["variables"]:
             # Marcar variable como usada
             marcar_variable_usada(nombre)
             tipo = obtener_tipo_variable(nombre)
             p[0] = tipo
         else:
             # REGLA 9: Verificar uso de variables no declaradas
             mensaje = f"Error semántico: Variable '{nombre}' no ha sido declarada."
             print(mensaje)
             mensajes.append(mensaje)
             p[0] = None
     else:
         # Propagar tipo de operaciones complejas
         p[0] = p[1]

# REGLA 10, 11, 12: Validar tipos en operaciones aritméticas (hook en valor_operacionAritmetica)
def p_valor_operacionAritmetica(p):
    '''operacion_aritmetica : valor operador_aritmetico valor
    | repite_operacion_aritmetica'''
    
    if len(p) == 4:  # valor operador valor
        tipo1 = p[1]
        tipo2 = p[3]
        
        if tipo1 is None or tipo2 is None:
            p[0] = None
            return
        
        # REGLA 11: Operaciones aritméticas solo entre tipos numéricos
        if not es_tipo_numerico(tipo1):
            mensaje = f"Error semántico: Operación aritmética no válida. '{tipo1}' no es un tipo numérico."
            print(mensaje)
            mensajes.append(mensaje)
            p[0] = None
            return
        
        if not es_tipo_numerico(tipo2):
            mensaje = f"Error semántico: Operación aritmética no válida. '{tipo2}' no es un tipo numérico."
            print(mensaje)
            mensajes.append(mensaje)
            p[0] = None
            return
        
        # REGLA 12: Verificar compatibilidad de tipos en operaciones
        if not son_tipos_compatibles(tipo1, tipo2):
            mensaje = f"Error semántico: Tipos incompatibles en operación aritmética. No se puede operar '{tipo1}' con '{tipo2}'."
            print(mensaje)
            mensajes.append(mensaje)
            p[0] = None
            return
        
        # Retornar el tipo resultante
        if tipo1 == "float" or tipo2 == "float":
            p[0] = "float"
        else:
            p[0] = tipo1
    else:
        p[0] = p[1]

def p_operador_aritmetico(p):
    '''operador_aritmetico : SUMA
                           | RESTA
                           | MULT
                           | DIV
                           | MODULO'''
    p[0] = p[1]

def p_repite_operacionAritmetica(p):
    '''repite_operacion_aritmetica : operacion_aritmetica 
                                    | operacion_aritmetica operador_aritmetico valor_numerico'''
    p[0] = p[1] if len(p) == 2 else "int"

# REGLA 13: Validar tipos en expresiones booleanas
def p_expresion_booleana(p):
    '''expresion_booleana : valor operador_relacional valor'''
    tipo1 = p[1]
    tipo2 = p[3]
    
    if tipo1 is not None and tipo2 is not None:
        if not son_tipos_compatibles(tipo1, tipo2):
            mensaje = f"Error semántico: Comparación entre tipos incompatibles '{tipo1}' y '{tipo2}'."
            print(mensaje)
            mensajes.append(mensaje)
    p[0] = "bool"

def p_operador_relacional(p):
    '''operador_relacional : MAYOR
                           | MENOR
                           | MAYOR_IGUAL
                           | MENOR_IGUAL
                           | IGUALDOBLE
                           | DIFERENTE'''
    p[0] = p[1]

# REGLA 14: Declaración de funciones
def p_funcion(p):
    '''funcion : FUNCION IDENTIFICADOR PAREN_IZQ PAREN_DER LLAVE_IZQ programa LLAVE_DER
               | FUNCION IDENTIFICADOR PAREN_IZQ PAREN_DER FLECHA tipo_dato LLAVE_IZQ programa LLAVE_DER'''
    nombre = p[2]
    tipo_retorno = p[6] if len(p) == 10 else None
    
    # REGLA 15: No redeclarar funciones
    if nombre in tabla_simbolos["funciones"]:
        mensaje = f"Error semántico: Función '{nombre}' ya fue declarada previamente."
        print(mensaje)
        mensajes.append(mensaje)
    else:
        tabla_simbolos["funciones"][nombre] = {
            "params": [],
            "retorno": tipo_retorno,
            "definida": True
        }

# REGLA 16: Validar llamadas a funciones
def p_llamada_funcion(p):
    '''llamada_funcion : IDENTIFICADOR PAREN_IZQ PAREN_DER PUNTOCOMA
                       | IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER PUNTOCOMA'''
    nombre = p[1]
    
    if nombre not in tabla_simbolos["funciones"]:
        mensaje = f"Error semántico: Función '{nombre}' no ha sido declarada."
        print(mensaje)
        mensajes.append(mensaje)

def p_asignacion_metodo_clase(p):
    '''asignacion : IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ PAREN_DER PUNTOCOMA
                  | IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER PUNTOCOMA'''
    nombre = p[1]
    metodo = p[3]

    if nombre not in tabla_simbolos["variables"]:
        mensaje = f"Error semántico: la variable '{nombre}' no ha sido definida."
        print(mensaje)
        mensajes.append(mensaje)
        return

    tipo_var = obtener_tipo_variable(nombre)
    
    # Verificar si es string
    if tipo_var == "str":
        if metodo not in tabla_simbolos["tipos"]["str-funciones"]:
            mensaje = f"Error semántico: el método '{metodo}' no es parte de las funciones de string."
            print(mensaje)
            mensajes.append(mensaje)
            return

        # Validar número de argumentos (aproximado: 0 vs al menos 1)
        especificacion = metodos_str_especificaciones.get(metodo)
        if especificacion:
            args_requeridos = especificacion["args"]
            tiene_args = (len(p) == 8)  # con repite_valores
            if args_requeridos == 0 and tiene_args:
                mensaje = f"Error semántico: el método '{metodo}' no acepta argumentos."
                print(mensaje)
                mensajes.append(mensaje)
            if args_requeridos > 0 and not tiene_args:
                mensaje = f"Error semántico: el método '{metodo}' requiere al menos {args_requeridos} argumento(s)."
                print(mensaje)
                mensajes.append(mensaje)
    
    # Verificar si es numérico
    elif es_tipo_numerico(tipo_var):
        if metodo not in tabla_simbolos["tipos"]["num-funciones"]:
            mensaje = f"Error semántico: el método '{metodo}' no es parte de las funciones numéricas."
            print(mensaje)
            mensajes.append(mensaje)
            return

        # Validar número de argumentos
        especificacion = metodos_num_especificaciones.get(metodo)
        if especificacion:
            args_requeridos = especificacion["args"]
            tiene_args = (len(p) == 8)  # con repite_valores
            if args_requeridos == 0 and tiene_args:
                mensaje = f"Error semántico: el método '{metodo}' no acepta argumentos."
                print(mensaje)
                mensajes.append(mensaje)
            if args_requeridos > 0 and not tiene_args:
                mensaje = f"Error semántico: el método '{metodo}' requiere al menos {args_requeridos} argumento(s)."
                print(mensaje)
                mensajes.append(mensaje)
    
    else:
        mensaje = f"Error semántico: la variable '{nombre}' de tipo '{tipo_var}' no soporta métodos."
        print(mensaje)
        mensajes.append(mensaje)

def p_llamada_funcion_sin_puntocoma(p):
    '''llamada_funcion_sin_puntocoma : IDENTIFICADOR PAREN_IZQ PAREN_DER
                                     | IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER'''
    nombre = p[1]
    
    if nombre not in tabla_simbolos["funciones"]:
        mensaje = f"Error semántico: Función '{nombre}' no ha sido declarada."
        print(mensaje)
        mensajes.append(mensaje)
        p[0] = None
    else:
        # Retornar el tipo de retorno de la función
        p[0] = tabla_simbolos["funciones"][nombre].get("retorno")

# REGLA: Métodos sobre strings y números (acceso con punto)
def p_llamada_metodo_clase(p):
    '''valor : IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ PAREN_DER
             | IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER'''
    nombre = p[1]
    metodo = p[3]

    if nombre not in tabla_simbolos["variables"]:
        mensaje = f"Error semántico: la variable '{nombre}' no ha sido definida."
        print(mensaje)
        mensajes.append(mensaje)
        p[0] = None
        return

    # Obtener tipo declarado de la variable
    tipo_var = obtener_tipo_variable(nombre)
    
    # Verificar si es string
    if tipo_var == "str":
        if metodo not in tabla_simbolos["tipos"]["str-funciones"]:
            mensaje = f"Error semántico: el método '{metodo}' no es parte de las funciones de string."
            print(mensaje)
            mensajes.append(mensaje)
            p[0] = None
            return

        # Validación de número de argumentos (aproximado: 0 vs al menos 1)
        especificacion = metodos_str_especificaciones.get(metodo)
        if especificacion:
            args_requeridos = especificacion["args"]
            tiene_args = (len(p) == 7)  # con repite_valores
            if args_requeridos == 0 and tiene_args:
                mensaje = f"Error semántico: el método '{metodo}' no acepta argumentos."
                print(mensaje)
                mensajes.append(mensaje)
            if args_requeridos > 0 and not tiene_args:
                mensaje = f"Error semántico: el método '{metodo}' requiere al menos {args_requeridos} argumento(s)."
                print(mensaje)
                mensajes.append(mensaje)

        # Asignar tipo de retorno según especificación
        p[0] = especificacion["ret"] if especificacion else "str"
    
    # Verificar si es numérico
    elif es_tipo_numerico(tipo_var):
        if metodo not in tabla_simbolos["tipos"]["num-funciones"]:
            mensaje = f"Error semántico: el método '{metodo}' no es parte de las funciones numéricas."
            print(mensaje)
            mensajes.append(mensaje)
            p[0] = None
            return

        # Validación de número de argumentos
        especificacion = metodos_num_especificaciones.get(metodo)
        if especificacion:
            args_requeridos = especificacion["args"]
            tiene_args = (len(p) == 7)  # con repite_valores
            if args_requeridos == 0 and tiene_args:
                mensaje = f"Error semántico: el método '{metodo}' no acepta argumentos."
                print(mensaje)
                mensajes.append(mensaje)
            if args_requeridos > 0 and not tiene_args:
                mensaje = f"Error semántico: el método '{metodo}' requiere al menos {args_requeridos} argumento(s)."
                print(mensaje)
                mensajes.append(mensaje)

        # Asignar tipo de retorno según especificación
        p[0] = especificacion["ret"] if especificacion else tipo_var
    
    else:
        mensaje = f"Error semántico: la variable '{nombre}' de tipo '{tipo_var}' no soporta métodos."
        print(mensaje)
        mensajes.append(mensaje)
        p[0] = None

def p_argumentos_string_methods(p):
    '''argumentos : valor
                  | valor COMA argumentos

    '''

# REGLA 17: Mapeo de tipo de dato (hook semántico)
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
                 | IDENTIFICADOR'''
    # Mapear tokens a nombres de tipos
    tipo_map = {
        'ITIPO': 'isize', 'I8': 'i8', 'I16': 'i16', 'I32': 'i32', 'I64': 'i64', 'I128': 'i128',
        'U8': 'u8', 'U16': 'u16', 'U32': 'u32', 'U64': 'u64', 'U128': 'u128', 'UTIPO': 'usize',
        'F32': 'f32', 'F64': 'f64',
        'BOOLEANO_TIPO': 'bool', 'CARACTER_TIPO': 'char', 'CADENA_TIPO': 'str'
    }
    token_type = p.slice[1].type
    p[0] = tipo_map.get(token_type, p[1])

# REGLA 18: Validar acceso a tuplas
def p_tupla_acceso(p):
    '''valor : IDENTIFICADOR PUNTO ENTERO'''
    nombre = p[1]
    indice = p[3]
    
    if nombre not in tabla_simbolos["variables"]:
        mensaje = f"Error semántico: Variable '{nombre}' no ha sido declarada."
        print(mensaje)
        mensajes.append(mensaje)
        p[0] = None
    else:
        marcar_variable_usada(nombre)
        tipo = obtener_tipo_variable(nombre)
        # Nota: En un analizador completo, verificaríamos que sea una tupla
        p[0] = tipo  # Simplificado

# REGLA 19: Validar acceso a matrices
def p_matriz_acceso(p):
    '''valor : IDENTIFICADOR CORCHETE_IZQ ENTERO CORCHETE_DER'''
    nombre = p[1]
    
    if nombre not in tabla_simbolos["variables"]:
        mensaje = f"Error semántico: Variable '{nombre}' no ha sido declarada."
        print(mensaje)
        mensajes.append(mensaje)
        p[0] = None
    else:
        marcar_variable_usada(nombre)
        tipo = obtener_tipo_variable(nombre)
        p[0] = tipo  # Simplificado

# REGLA 20: Validar valores booleanos
def p_valor_booleano(p):
    '''valor : VERDAD
             | FALSO'''
    p[0] = "bool"

def p_valor_numerico(p):
    '''valor_numerico : ENTERO
                      | FLOTANTE'''
    if isinstance(p[1], int):
        p[0] = "int"
    elif isinstance(p[1], float):
        p[0] = "float"

    
# Error rule for syntax errors
def p_error(p):
    print("Error semántico")
    if p:
        mensaje = f"Error semántico en la línea {p.lineno}, columna {p.lexpos}: Token inesperado '{p.value}'"
        log_token(mensaje)
    else:
        mensaje = "Error semántico: Fin de archivo inesperado"
        log_token(mensaje)
parser = yacc.yacc(module=sys.modules[__name__])

def log_token(mensaje):
    usuario_git = get_git_user()
    fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, f"semántico-{usuario_git}-{fecha_hora}.txt")
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(mensaje + "\n")

if __name__ == "__main__":
    print("Analizador Semántico: ")
    if len(sys.argv) > 1:
        archivo_entrada = sys.argv[1]
    else:
        archivo_entrada = input("Ingrese el nombre del archivo de entrada: ")
        
    try:
        with open(archivo_entrada, 'r') as file:
            data = file.read()
        
        parser.parse(data)
        
        while True:
            if not mensajes:
                
                log_token(str(tabla_simbolos))
                break
            else:
                mensaje = mensajes.pop(0)
                log_token(mensaje)
        print("\n=== TABLA DE SÍMBOLOS ===")
        print("\n--- Variables ---")
        for var, info in tabla_simbolos["variables"].items():
            if isinstance(info, dict):
                tipo = info.get("tipo", "unknown")
                const = "const" if info.get("const") else ("mut" if info.get("mutable") else "let")
                usado = "✓" if info.get("usado") else "✗ (no usada)"
                print(f"  {var}: {const} {tipo} - Usado: {usado}")
            else:
                print(f"  {var}: {info}")
        
        print("\n--- Funciones ---")
        for func, info in tabla_simbolos["funciones"].items():
            retorno = info.get("retorno", "void")
            params = len(info.get("params", []))
            print(f"  {func}({params} params) -> {retorno}")
        
        # REGLA 21: Advertencia sobre variables no usadas
        print("\n--- Advertencias ---")
        for var, info in tabla_simbolos["variables"].items():
            if isinstance(info, dict) and not info.get("usado", False):
                mensaje = f"Advertencia: Variable '{var}' declarada pero no usada."
                print(f"  ⚠ {mensaje}")
                log_token(mensaje)
            
    except FileNotFoundError:
        print(f"Archivo no encontrado: {archivo_entrada}")
        log_token(f"Archivo no encontrado: {archivo_entrada}")
    