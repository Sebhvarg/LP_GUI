# ------------------------------------------------------------ 
# parser.py
# Analizador Semantico usando PLY.Yacc
# Grupo 10
# ------------------------------------------------------------
import ply.yacc as yacc
import sys
import datetime
import os
import sys, os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Lexicon.lexer import lexer, tokens, get_git_user
from Syntax.syntax import *

# ------------------------------------------------------------
# Integrantes:
#   Derian Baque Choez (fernan0502)
#   Sebastian Holguin (Sebhvarg)
#   Carlos Ronquillo (carrbrus)
# ------------------------------------------------------------
mensajes = []
errores_sintacticos = []
errores_semanticos = []
errores_lexicos = []

# Flag para controlar si se reportan errores sintácticos durante el análisis semántico
report_syntax_errors = True

def set_syntax_error_reporting(enabled: bool):
    """Permite activar/desactivar la emisión de mensajes de error sintáctico en fase semántica.
    Cuando está desactivado se sigue intentando 'salvage' para producir errores semánticos, pero
    los mensajes puramente sintácticos se omiten."""
    global report_syntax_errors
    report_syntax_errors = enabled

def add_mensaje(mensaje: str):
    """Registra y categoriza un mensaje de error/advertencia.
    Mantiene compatibilidad con lista 'mensajes' y salida estándar.
    """
    lower = mensaje.lower()
    if lower.startswith("error sintáctico") or lower.startswith("error sintactico"):
        errores_sintacticos.append(mensaje)
    elif lower.startswith("error semántico") or lower.startswith("error semantico"):
        errores_semanticos.append(mensaje)
    elif lower.startswith("error léxico") or lower.startswith("error lexico"):
        errores_lexicos.append(mensaje)
    mensajes.append(mensaje)
    # Imprimir para mantener comportamiento existente de captura por la GUI
    print(mensaje)
def _categorize_existing():
    """Llena las listas de errores a partir de 'mensajes' si aún no se categorizaron."""
    for m in mensajes:
        lower = m.lower()
        if (lower.startswith("error sintáctico") or lower.startswith("error sintactico")) and m not in errores_sintacticos:
            errores_sintacticos.append(m)
        elif (lower.startswith("error semántico") or lower.startswith("error semantico")) and m not in errores_semanticos:
            errores_semanticos.append(m)
        elif (lower.startswith("error léxico") or lower.startswith("error lexico")) and m not in errores_lexicos:
            errores_lexicos.append(m)
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

# Utilidades para posición (línea/columna) en mensajes
def _columna(p, idx):
    try:
        data = p.lexer.lexdata or ""
        lexpos = p.lexpos(idx)
        last_cr = data.rfind('\n', 0, lexpos)
        return (lexpos - last_cr) if last_cr != -1 else (lexpos + 1)
    except Exception:
        return 0

def _pos(p, idx):
    try:
        data = p.lexer.lexdata or ""
        lexpos = p.lexpos(idx)
        # Intentar usar la línea del token; si es 0/None, calcular desde el buffer
        line = getattr(p, 'lineno', lambda i: 0)(idx) or (data.count('\n', 0, lexpos) + 1)
        col = _columna(p, idx)
        return f"en la línea {line}, columna {col}"
    except Exception:
        # Fallback burdo
        return f"en la línea 0, columna 0"

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
                    | IDENTIFICADOR IGUAL valor PUNTOCOMA                    
    '''
    # REGLA 1: Declaración de variable inmutable (let x = valor)
    if len(p) == 6 and p.slice[1].type == 'VARIABLE':
        nombre = p[2]
        tipo_var = p[4]
        
        # Verificar que no exista ya en el scope actual
        if nombre in tabla_simbolos["variables"]:
            mensaje = f"Error semántico: {_pos(p,1)}: Variable '{nombre}' ya fue declarada previamente."
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
            mensaje = f"Error semántico: {_pos(p,1)}: Variable '{nombre}' no ha sido declarada."
            print(mensaje)
            mensajes.append(mensaje)
        else:
            info = tabla_simbolos["variables"][nombre]
            
            # REGLA 3: No se puede reasignar constantes
            if isinstance(info, dict) and info.get("const", False):
                mensaje = f"Error semántico: {_pos(p,1)}: No se puede modificar la constante '{nombre}'."
                print(mensaje)
                mensajes.append(mensaje)
            
            # REGLA 4: No se puede reasignar variables inmutables (let sin mut)
            elif isinstance(info, dict) and not info.get("mutable", False) and not info.get("const", False):
                mensaje = f"Error semántico: {_pos(p,1)}: No se puede reasignar la variable inmutable '{nombre}'. Use 'let mut' para variables mutables."
                print(mensaje)
                mensajes.append(mensaje)
            
            # REGLA 5: Verificar compatibilidad de tipos en reasignación
            elif nuevo_tipo is not None and isinstance(info, dict):
                tipo_actual = info.get("tipo")
                if tipo_actual and not son_tipos_compatibles(tipo_actual, nuevo_tipo):
                    mensaje = f"Error semántico {_pos(p,1)}: Tipo incompatible en reasignación de '{nombre}'. Se esperaba '{tipo_actual}', se recibió '{nuevo_tipo}'."
                    print(mensaje)
                    mensajes.append(mensaje)

# REGLA 6: Declaración de variable mutable (let mut)
def p_asignacion_mutable(p):
    'asignacion : VARIABLE MUTABLE IDENTIFICADOR IGUAL valor PUNTOCOMA'
    nombre = p[3]
    tipo_var = p[5]
    
    if nombre in tabla_simbolos["variables"]:
        mensaje = f"Error semántico {_pos(p,1)}: Variable '{nombre}' ya fue declarada previamente."
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
        mensaje = f"Error semántico {_pos(p,1)}: Constante '{nombre}' ya fue declarada previamente."
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
        mensaje = f"Error semántico {_pos(p,1)}: Variable '{nombre}' ya fue declarada previamente."
        print(mensaje)
        mensajes.append(mensaje)
    elif tipo_valor is not None and not son_tipos_compatibles(tipo_declarado, tipo_valor):
        mensaje = f"Error semántico {_pos(p,1)}: Tipo incompatible. Variable '{nombre}' declarada como '{tipo_declarado}' pero recibe '{tipo_valor}'."
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
             | bloque
             | acceso_complejo
             | instanciar_clase'''
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
             mensaje = f"Error semántico {_pos(p,1)}: Variable '{nombre}' no ha sido declarada."
             print(mensaje)
             mensajes.append(mensaje)
             p[0] = None
     elif p.slice[1].type == 'matriz':
         p[0] = p[1]  # tipo inferido por p_matriz
     elif p.slice[1].type == 'vector':
         p[0] = p[1]  # tipo inferido por p_vector
     elif p.slice[1].type == 'tupla':
         p[0] = p[1]  # tipo inferido por p_tupla
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
            mensaje = f"Error semántico {_pos(p,2)}: Operación aritmética no válida. '{tipo1}' no es un tipo numérico."
            print(mensaje)
            mensajes.append(mensaje)
            p[0] = None
            return
        
        if not es_tipo_numerico(tipo2):
            mensaje = f"Error semántico {_pos(p,2)}: Operación aritmética no válida. '{tipo2}' no es un tipo numérico."
            print(mensaje)
            mensajes.append(mensaje)
            p[0] = None
            return
        
        # REGLA 12: Verificar compatibilidad de tipos en operaciones
        if not son_tipos_compatibles(tipo1, tipo2):
            mensaje = f"Error semántico {_pos(p,2)}: Tipos incompatibles en operación aritmética. No se puede operar '{tipo1}' con '{tipo2}'."
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

# --- Nuevas reglas para inferencia de colecciones ---
def p_repite_valores(p):
    '''repite_valores : valor
                      | valor COMA repite_valores'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def _infer_collection_element_type(element_types):
    # Filtrar None y tomar prioridad: float > int > str > char > bool > otro
    tipos = [t for t in element_types if t is not None]
    if not tipos:
        return 'unknown'
    # Si todos iguales, devolver ese
    if all(t == tipos[0] for t in tipos):
        return tipos[0]
    # Mezcla numérica -> float si alguno float, sino int
    if all(t in ('int','float') for t in tipos):
        return 'float' if 'float' in tipos else 'int'
    # Caso mixto devolver 'mixed'
    return 'mixed'

def p_matriz(p):
    '''matriz : CORCHETE_IZQ repite_valores CORCHETE_DER
              | CORCHETE_IZQ CORCHETE_DER'''
    if len(p) == 4:
        elem_tipo = _infer_collection_element_type(p[2])
        p[0] = f"matriz<{elem_tipo}>"
    else:
        p[0] = "matriz<vacía>"

def p_vector(p):
    '''vector : VECTOR_MACRO CORCHETE_IZQ repite_valores CORCHETE_DER
              | VECTOR_MACRO CORCHETE_IZQ CORCHETE_DER'''  # vector vacío
    if len(p) == 5:
        elem_tipo = _infer_collection_element_type(p[3])
        p[0] = f"vector<{elem_tipo}>"
    else:
        p[0] = "vector<vacío>"

def p_tupla(p):
    '''tupla : PAREN_IZQ repite_valores PAREN_DER
             | PAREN_IZQ PAREN_DER'''
    if len(p) == 4:
        elem_tipo = _infer_collection_element_type(p[2])
        p[0] = f"tupla<{elem_tipo}>"
    else:
        p[0] = "tupla<vacía>"

# REGLA 13: Validar tipos en expresiones booleanas
def p_expresion_booleana(p):
    '''expresion_booleana : valor operador_relacional valor'''
    tipo1 = p[1]
    tipo2 = p[3]
    
    if tipo1 is not None and tipo2 is not None:
        if not son_tipos_compatibles(tipo1, tipo2):
            mensaje = f"Error semántico {_pos(p,2)}: Comparación entre tipos incompatibles '{tipo1}' y '{tipo2}'."
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
        mensaje = f"Error semántico en la línea {p.lineno(1)}, columna {p.lexpos(1)}: Función '{nombre}' ya fue declarada previamente."
        print(mensaje)
        mensajes.append(mensaje)
    else:
        tabla_simbolos["funciones"][nombre] = {
            "params": [],
            "retorno": tipo_retorno,
            "definida": True
        }

# Declaración de funciones con parámetros
def p_funcion_parametros(p):
    '''funcion : FUNCION IDENTIFICADOR PAREN_IZQ parametros PAREN_DER LLAVE_IZQ programa LLAVE_DER
               | FUNCION IDENTIFICADOR PAREN_IZQ parametros PAREN_DER FLECHA tipo_dato LLAVE_IZQ programa LLAVE_DER'''
    nombre = p[2]
    # Para la regla con flecha (9 elementos): FUNCION ID ( params ) -> tipo { programa }
    # len(p) = 10, tipo_retorno está en p[7]
    tipo_retorno = p[7] if len(p) == 10 else None
    
    if nombre in tabla_simbolos["funciones"]:
        mensaje = f"Error semántico en la línea {p.lineno(1)}, columna {p.lexpos(1)}: Función '{nombre}' ya fue declarada previamente."
        print(mensaje)
        mensajes.append(mensaje)
    else:
        # Extraer información de parámetros
        params_info = p[4] if p[4] else []
        num_params = len(params_info) if isinstance(params_info, list) else 1
        tabla_simbolos["funciones"][nombre] = {
            "params": params_info if isinstance(params_info, list) else [params_info],
            "retorno": tipo_retorno,
            "definida": True
        }

def p_parametros(p):
    '''parametros : IDENTIFICADOR
                  | IDENTIFICADOR COMA parametros
                  | IDENTIFICADOR DOSPUNTOS tipo_dato 
                  | IDENTIFICADOR DOSPUNTOS tipo_dato COMA parametros
    '''
    # Retornar la estructura de parámetros para que p_funcion_parametros pueda contarlos
    if len(p) == 2:  # Solo IDENTIFICADOR
        p[0] = [p[1]]
    elif len(p) == 4 and p[2] == ',':  # IDENTIFICADOR COMA parametros
        p[0] = [p[1]] + (p[3] if isinstance(p[3], list) else [p[3]])
    elif len(p) == 4:  # IDENTIFICADOR DOSPUNTOS tipo_dato
        p[0] = [(p[1], p[3])]
    elif len(p) == 6:  # IDENTIFICADOR DOSPUNTOS tipo_dato COMA parametros
        p[0] = [(p[1], p[3])] + (p[5] if isinstance(p[5], list) else [p[5]])

# REGLA 16: Validar llamadas a funciones
def p_llamada_funcion(p):
    '''llamada_funcion : IDENTIFICADOR PAREN_IZQ PAREN_DER PUNTOCOMA
                       | IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER PUNTOCOMA'''
    nombre = p[1]
    
    if nombre not in tabla_simbolos["funciones"]:
        mensaje = f"Error semántico {_pos(p,1)}: Función '{nombre}' no ha sido declarada."
        print(mensaje)
        mensajes.append(mensaje)

def p_asignacion_metodo_clase(p):
    '''asignacion : IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ PAREN_DER PUNTOCOMA
                  | IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER PUNTOCOMA'''
    nombre = p[1]
    metodo = p[3]

    if nombre not in tabla_simbolos["variables"]:
        mensaje = f"Error semántico {_pos(p,1)}: la variable '{nombre}' no ha sido definida."
        print(mensaje)
        mensajes.append(mensaje)
        return

    tipo_var = obtener_tipo_variable(nombre)
    
    # Verificar si es string
    if tipo_var == "str":
        if metodo not in tabla_simbolos["tipos"]["str-funciones"]:
            mensaje = f"Error semántico en la línea {p.lineno(1)}, columna {p.lexpos(1)}: el método '{metodo}' no es parte de las funciones de string."
            print(mensaje)
            mensajes.append(mensaje)
            return

        # Validar número de argumentos (aproximado: 0 vs al menos 1)
        especificacion = metodos_str_especificaciones.get(metodo)
        if especificacion:
            args_requeridos = especificacion["args"]
            tiene_args = (len(p) == 8)  # con repite_valores
            if args_requeridos == 0 and tiene_args:
                mensaje = f"Error semántico {_pos(p,1)}: el método '{metodo}' no acepta argumentos."
                print(mensaje)
                mensajes.append(mensaje)
            if args_requeridos > 0 and not tiene_args:
                mensaje = f"Error semántico {_pos(p,1)}: el método '{metodo}' requiere al menos {args_requeridos} argumento(s)."
                print(mensaje)
                mensajes.append(mensaje)
    
    # Verificar si es numérico
    elif es_tipo_numerico(tipo_var):
        if metodo not in tabla_simbolos["tipos"]["num-funciones"]:
            mensaje = f"Error semántico {_pos(p,1)}: el método '{metodo}' no es parte de las funciones numéricas."
            print(mensaje)
            mensajes.append(mensaje)
            return

        # Validar número de argumentos
        especificacion = metodos_num_especificaciones.get(metodo)
        if especificacion:
            args_requeridos = especificacion["args"]
            tiene_args = (len(p) == 8)  # con repite_valores
            if args_requeridos == 0 and tiene_args:
                mensaje = f"Error semántico {_pos(p,1)}: el método '{metodo}' no acepta argumentos."
                print(mensaje)
                mensajes.append(mensaje)
            if args_requeridos > 0 and not tiene_args:
                mensaje = f"Error semántico {_pos(p,1)}: el método '{metodo}' requiere al menos {args_requeridos} argumento(s)."
                print(mensaje)
                mensajes.append(mensaje)
    
    else:
        mensaje = f"Error semántico {_pos(p,1)}: la variable '{nombre}' de tipo '{tipo_var}' no soporta métodos."
        print(mensaje)
        mensajes.append(mensaje)

def p_llamada_funcion_sin_puntocoma(p):
    '''llamada_funcion_sin_puntocoma : IDENTIFICADOR PAREN_IZQ PAREN_DER
                                     | IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER'''
    nombre = p[1]
    
    if nombre not in tabla_simbolos["funciones"]:
        mensaje = f"Error semántico {_pos(p,1)}: Función '{nombre}' no ha sido declarada."
        print(mensaje)
        mensajes.append(mensaje)
        p[0] = None
    else:
        # Retornar el tipo de retorno de la función
        p[0] = tabla_simbolos["funciones"][nombre].get("retorno")

# REGLA: Incrementos y asignaciones compuestas (validar const/mut y tipos)
def p_asignacion_incremento(p):
    '''asignacion_incremento : IDENTIFICADOR MAS_IGUAL ENTERO
                              | IDENTIFICADOR MENOS_IGUAL ENTERO
                              | IDENTIFICADOR SUMA SUMA
                              | IDENTIFICADOR RESTA RESTA
                              | IDENTIFICADOR IGUAL IDENTIFICADOR SUMA ENTERO
    '''
    # Caso base: objetivo a modificar siempre es el primer identificador
    objetivo = p[1]

    # Verificar existencia de la variable objetivo
    if objetivo not in tabla_simbolos["variables"]:
        mensaje = f"Error semántico: {_pos(p,1)}: Variable '{objetivo}' no ha sido declarada."
        print(mensaje)
        mensajes.append(mensaje)
        return

    info_obj = tabla_simbolos["variables"][objetivo]

    # No permitir modificar constantes
    if isinstance(info_obj, dict) and info_obj.get("const", False):
        mensaje = f"Error semántico: {_pos(p,1)}: No se puede modificar la constante '{objetivo}'."
        print(mensaje)
        mensajes.append(mensaje)
        return

    # No permitir modificar variables inmutables (let sin mut)
    if isinstance(info_obj, dict) and not info_obj.get("mutable", False):
        mensaje = f"Error semántico: {_pos(p,1)}: No se puede reasignar la variable inmutable '{objetivo}'. Use 'let mut' para variables mutables."
        print(mensaje)
        mensajes.append(mensaje)
        return

    # Validaciones de tipo (todas estas operaciones son numéricas)
    tipo_obj = info_obj.get("tipo") if isinstance(info_obj, dict) else info_obj
    if not es_tipo_numerico(tipo_obj):
        mensaje = f"Error semántico {_pos(p,1)}: Operación no válida. '{objetivo}' de tipo '{tipo_obj}' no es numérico."
        print(mensaje)
        mensajes.append(mensaje)
        return

    # Caso especial: a = b + 1
    if len(p) == 6 and p.slice[2].type == 'IGUAL':
        fuente = p[3]
        # Verificar que la fuente exista
        if fuente not in tabla_simbolos["variables"]:
            mensaje = f"Error semántico: {_pos(p,3)}: Variable '{fuente}' no ha sido declarada."
            print(mensaje)
            mensajes.append(mensaje)
            return
        info_fuente = tabla_simbolos["variables"][fuente]
        tipo_fuente = info_fuente.get("tipo") if isinstance(info_fuente, dict) else info_fuente
        if not es_tipo_numerico(tipo_fuente):
            mensaje = f"Error semántico {_pos(p,3)}: Operación no válida. '{fuente}' de tipo '{tipo_fuente}' no es numérico."
            print(mensaje)
            mensajes.append(mensaje)
            return
        # Compatibilidad de tipos objetivo y fuente
        if not son_tipos_compatibles(tipo_obj, tipo_fuente):
            mensaje = f"Error semántico {_pos(p,1)}: Tipos incompatibles en asignación. '{objetivo}' es '{tipo_obj}' y '{fuente}' es '{tipo_fuente}'."
            print(mensaje)
            mensajes.append(mensaje)
            return

# REGLA: Métodos sobre strings y números (acceso con punto)
def p_llamada_metodo_clase(p):
    '''llamada_metodo_clase : IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ PAREN_DER
             | IDENTIFICADOR PUNTO IDENTIFICADOR PAREN_IZQ repite_valores PAREN_DER'''
    nombre = p[1]
    metodo = p[3]

    if nombre not in tabla_simbolos["variables"]:
        mensaje = f"Error semántico {_pos(p,1)}: la variable '{nombre}' no ha sido definida."
        print(mensaje)
        mensajes.append(mensaje)
        p[0] = None
        return

    # Obtener tipo declarado de la variable
    tipo_var = obtener_tipo_variable(nombre)
    
    # Verificar si es string
    if tipo_var == "str":
        if metodo not in tabla_simbolos["tipos"]["str-funciones"]:
            mensaje = f"Error semántico en la línea {p.lineno(1)}, columna {p.lexpos(1)}: el método '{metodo}' no es parte de las funciones de string."
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
                mensaje = f"Error semántico {_pos(p,1)}: el método '{metodo}' no acepta argumentos."
                print(mensaje)
                mensajes.append(mensaje)
            if args_requeridos > 0 and not tiene_args:
                mensaje = f"Error semántico {_pos(p,1)}: el método '{metodo}' requiere al menos {args_requeridos} argumento(s)."
                print(mensaje)
                mensajes.append(mensaje)

        # Asignar tipo de retorno según especificación
        p[0] = especificacion["ret"] if especificacion else "str"
    
    # Verificar si es numérico
    elif es_tipo_numerico(tipo_var):
        if metodo not in tabla_simbolos["tipos"]["num-funciones"]:
            mensaje = f"Error semántico {_pos(p,1)}: el método '{metodo}' no es parte de las funciones numéricas."
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
                mensaje = f"Error semántico {_pos(p,1)}: el método '{metodo}' no acepta argumentos."
                print(mensaje)
                mensajes.append(mensaje)
            if args_requeridos > 0 and not tiene_args:
                mensaje = f"Error semántico {_pos(p,1)}: el método '{metodo}' requiere al menos {args_requeridos} argumento(s)."
                print(mensaje)
                mensajes.append(mensaje)

        # Asignar tipo de retorno según especificación
        p[0] = especificacion["ret"] if especificacion else tipo_var
    
    else:
        mensaje = f"Error semántico {_pos(p,1)}: la variable '{nombre}' de tipo '{tipo_var}' no soporta métodos."
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
    '''tupla_acceso : IDENTIFICADOR PUNTO ENTERO'''
    nombre = p[1]
    indice = p[3]
    
    if nombre not in tabla_simbolos["variables"]:
        mensaje = f"Error semántico {_pos(p,1)}: Variable '{nombre}' no ha sido declarada."
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
    '''matriz_acceso : IDENTIFICADOR CORCHETE_IZQ ENTERO CORCHETE_DER'''
    nombre = p[1]
    
    if nombre not in tabla_simbolos["variables"]:
        mensaje = f"Error semántico {_pos(p,1)}: Variable '{nombre}' no ha sido declarada."
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

# REGLA: Constante con tipo explícito
def p_asignacion_constante_explicita(p):
    'asignacion : CONSTANTE IDENTIFICADOR DOSPUNTOS tipo_dato IGUAL valor PUNTOCOMA'
    nombre = p[2]
    tipo_declarado = p[4]
    tipo_valor = p[6]

    if nombre in tabla_simbolos["variables"]:
        mensaje = f"Error semántico {_pos(p,1)}: Constante '{nombre}' ya fue declarada previamente."
        print(mensaje)
        mensajes.append(mensaje)
    # Registrar igualmente la constante para permitir diagnosticar modificaciones posteriores,
    # pero reportar incompatibilidad de tipos si aplica.
    tabla_simbolos["variables"][nombre] = {
        "tipo": tipo_declarado,
        "const": True,
        "mutable": False,
        "usado": False
    }
    if tipo_valor is not None and not son_tipos_compatibles(tipo_declarado, tipo_valor):
        mensaje = f"Error semántico {_pos(p,1)}: Tipo incompatible. Constante '{nombre}' declarada como '{tipo_declarado}' pero recibe '{tipo_valor}'."
        print(mensaje)
        mensajes.append(mensaje)

    
# Error rule for syntax errors
def p_error(p):
    """Manejo de errores sintácticos.
    Cambiado para:
      - Etiquetar correctamente como 'Error sintáctico'.
      - Calcular columna real (no usar lexpos directo).
      - Intentar una recuperación mínima descartando el token problemático
        para reducir la cascada de errores.
    """
    def _calc_col(token):
        try:
            data = token.lexer.lexdata or ""
            last_cr = data.rfind('\n', 0, token.lexpos)
            return (token.lexpos - last_cr) if last_cr != -1 else (token.lexpos + 1)
        except Exception:
            return token.lexpos

    def _salvage_constante(tok_const):
        """Intenta reconocer una declaración de constante tras un error sintáctico
        para poder emitir errores semánticos (redeclaración) y registrar la constante.
        Forma esperada (simplificada):
          const IDENTIFICADOR [ ':' tipo ] '=' valor ';'
        Devuelve True si se realizó el salvage.
        """
        nombre = None
        tipo_explicito = None
        valor_visto = False
        valor_tokens = []
        tokens_consumidos = [tok_const]
        missing_semicolon = False
        start_new_stmt_tokens = {'VARIABLE','CONSTANTE','FUNCION','SI','SINO','MIENTRAS','POR','COINCIDIR'}
        # Leer siguientes tokens hasta ';' o fin
        start_line = tok_const.lineno
        while True:
            tk = parser.token()
            if not tk:
                missing_semicolon = True
                break
            tokens_consumidos.append(tk)
            # Si avanzamos de línea y vemos inicio de nueva sentencia antes de ';', cortar
            if tk.lineno > start_line and tk.type in start_new_stmt_tokens and not valor_visto:
                missing_semicolon = True
                break
            if tk.type == 'IDENTIFICADOR' and nombre is None:
                nombre = tk.value
                continue
            if tk.type == 'DOSPUNTOS' and tipo_explicito is None:
                tipo_tok = parser.token()
                if tipo_tok:
                    tokens_consumidos.append(tipo_tok)
                    tipo_explicito = tipo_tok.value
                continue
            if tk.type == 'IGUAL' and not valor_visto:
                valor_visto = True
                continue
            if valor_visto and tk.type != 'PUNTOCOMA':
                if tk.type in start_new_stmt_tokens:
                    missing_semicolon = True
                    break
                valor_tokens.append(tk)
            if tk.type == 'PUNTOCOMA':
                break
        if nombre is None:
            return False  # no pudimos rescatar estructura

        # Registrar o reportar redeclaración
        if nombre in tabla_simbolos["variables"]:
            mensaje_sem = f"Error semántico en la línea {tok_const.lineno}, columna {_calc_col(tok_const)}: Constante '{nombre}' ya fue declarada previamente."
            add_mensaje(mensaje_sem)
            log_token(mensaje_sem)
        else:
            tipo_inferido = tipo_explicito or _infer_type_from_tokens(valor_tokens)
            tabla_simbolos["variables"][nombre] = {
                "tipo": tipo_inferido,
                "const": True,
                "mutable": False,
                "usado": False
            }
        if missing_semicolon and report_syntax_errors:
            msg = f"Error sintáctico en la línea {tok_const.lineno}: falta punto y coma al final de la declaración de la constante '{nombre}' (análisis parcial)."
            add_mensaje(msg)
            log_token(msg)
        return True

    def _salvage_modificacion_constante(tok_ident):
        """Intenta detectar modificación de una constante tras perder la gramática.
        Forma: IDENTIFICADOR '=' valor ';'
        """
        nombre = tok_ident.value
        eq = parser.token()
        if not eq or eq.type != 'IGUAL':
            # devolver tokens consumidos al flujo no es trivial; abortamos
            return False
        # Consumir hasta ';'
        while True:
            tk = parser.token()
            if not tk or tk.type == 'PUNTOCOMA':
                break
        if nombre in tabla_simbolos["variables"]:
            info = tabla_simbolos["variables"][nombre]
            if isinstance(info, dict) and info.get("const", False):
                mensaje_sem = f"Error semántico en la línea {tok_ident.lineno}, columna {_calc_col(tok_ident)}: No se puede modificar la constante '{nombre}'."
                add_mensaje(mensaje_sem)
                log_token(mensaje_sem)
                return True
            elif isinstance(info, dict) and not info.get("mutable", False):
                # Variable inmutable (let) no puede ser reasignada
                mensaje_sem = f"Error semántico en la línea {tok_ident.lineno}, columna {_calc_col(tok_ident)}: No se puede reasignar la variable inmutable '{nombre}'. Use 'let mut' para variables mutables."
                add_mensaje(mensaje_sem)
                log_token(mensaje_sem)
                return True
        return False

    def _salvage_variable(tok_let):
        """Recupera declaración de variable tras error sintáctico.
        Patrón simplificado:
          let [mut] IDENT [ ':' tipo ] '=' valor ';'
        Registra la variable y reporta redeclaración si existe.
        """
        mutable_flag = False
        nombre = None
        tipo_explicito = None
        eq_visto = False
        valor_tokens = []  # tokens después de '=' para diagnóstico sencillo
        missing_semicolon = False
        start_new_stmt_tokens = {'VARIABLE','CONSTANTE','FUNCION','SI','SINO','MIENTRAS','POR','COINCIDIR'}
        # Consumir tokens hasta ';' o EOF
        start_line = tok_let.lineno
        while True:
            tk = parser.token()
            if not tk:
                missing_semicolon = True
                break
            # Si avanzamos a nueva línea y aparece inicio de sentencia antes de ';', cortar
            if tk.lineno > start_line and tk.type in start_new_stmt_tokens and not eq_visto:
                missing_semicolon = True
                break
            if tk.type == 'MUTABLE' and nombre is None and not mutable_flag:
                mutable_flag = True
                continue
            if tk.type == 'IDENTIFICADOR' and nombre is None:
                nombre = tk.value
                continue
            if tk.type == 'DOSPUNTOS' and tipo_explicito is None:
                tipo_tok = parser.token()
                if tipo_tok:
                    tipo_explicito = tipo_tok.value
                continue
            if tk.type == 'IGUAL' and not eq_visto:
                eq_visto = True
                continue
            if eq_visto and tk.type != 'PUNTOCOMA':
                if tk.type in start_new_stmt_tokens:
                    missing_semicolon = True
                    break
                valor_tokens.append(tk)
            if tk.type == 'PUNTOCOMA':
                break
        if nombre is None:
            return False
        if nombre in tabla_simbolos['variables']:
            mensaje_sem = f"Error semántico en la línea {tok_let.lineno}, columna {_calc_col(tok_let)}: Variable '{nombre}' ya fue declarada previamente."
            add_mensaje(mensaje_sem)
            log_token(mensaje_sem)
        else:
            tipo_inferido = tipo_explicito or _infer_type_from_tokens(valor_tokens)
            tabla_simbolos['variables'][nombre] = {
                'tipo': tipo_inferido,
                'const': False,
                'mutable': mutable_flag,
                'usado': False
            }
        if missing_semicolon and report_syntax_errors:
            mensaje_pyc = f"Error sintáctico en la línea {tok_let.lineno}: falta punto y coma al final de la declaración de '{nombre}' (análisis parcial)."
            add_mensaje(mensaje_pyc)
            log_token(mensaje_pyc)
        # Diagnóstico adicional: llamada a función inexistente dentro del valor recuperado
        if valor_tokens:
            # Patrón simple IDENTIFICADOR PAREN_IZQ ... PAREN_DER
            if (len(valor_tokens) >= 2 and valor_tokens[0].type == 'IDENTIFICADOR' and valor_tokens[1].type == 'PAREN_IZQ'):
                func_name = valor_tokens[0].value
                if func_name not in tabla_simbolos['funciones']:
                    mensaje_fn = f"Error semántico en la línea {valor_tokens[0].lineno}, columna {_calc_col(valor_tokens[0])}: Función '{func_name}' no ha sido declarada."
                    add_mensaje(mensaje_fn)
                    log_token(mensaje_fn)
        return True

    def _infer_type_from_tokens(tokens_seq):
        """Heurística simple para inferir tipo a partir de los tokens del valor.
        - ENTERO -> int
        - FLOTANTE -> float
        - CADENA -> str
        - CARACTER -> char
        - VERDAD / FALSO -> bool
        - IDENTIFICADOR -> tipo de variable previamente declarada o retorno de función conocida
        - Operación aritmética simple -> tipo numérico dominante (int/float)
        - Si no se puede inferir, None.
        """
        if not tokens_seq:
            return None
        first = tokens_seq[0]
        ttype = first.type
        if ttype == 'ENTERO':
            return 'int'
        if ttype == 'FLOTANTE':
            return 'float'
        if ttype == 'CADENA':
            return 'str'
        if ttype == 'CARACTER':
            return 'char'
        if ttype in ('VERDAD','FALSO'):
            return 'bool'
        if ttype == 'IDENTIFICADOR':
            nombre = first.value
            # Variable conocida
            if nombre in tabla_simbolos['variables']:
                info = tabla_simbolos['variables'][nombre]
                if isinstance(info, dict):
                    return info.get('tipo')
                return info
            # Función conocida (patrón IDENT '(' ... ')')
            if len(tokens_seq) > 1 and tokens_seq[1].type == 'PAREN_IZQ' and nombre in tabla_simbolos['funciones']:
                retorno = tabla_simbolos['funciones'][nombre].get('retorno')
                return retorno or None
        # Chequeo operación numérica ENTERO/ FLOTANTE con operadores
        numeric = {'ENTERO','FLOTANTE'}
        operadores = {'SUMA','RESTA','MULT','DIV','MODULO'}
        if any(tok.type in numeric for tok in tokens_seq) and any(tok.type in operadores for tok in tokens_seq):
            return 'float' if any(tok.type == 'FLOTANTE' for tok in tokens_seq) else 'int'
        return None

    if p:
        salvage_done = False
        # Intentos de salvage específicos antes de registrar error sintáctico genérico
        if p.type == 'CONSTANTE':
            salvage_done = _salvage_constante(p)
        elif p.type == 'VARIABLE':
            salvage_done = _salvage_variable(p)
        elif p.type == 'IDENTIFICADOR':
            salvage_done = _salvage_modificacion_constante(p)

        if not salvage_done and report_syntax_errors:
            col = _calc_col(p)
            mensaje = f"Error sintáctico en la línea {p.lineno}, columna {col}: Token inesperado '{p.value}'"
            add_mensaje(mensaje)
            log_token(mensaje)

        # Recuperación: consumir hasta un delimitador seguro solo si no hicimos salvage
        if not salvage_done:
            try:
                while True:
                    tok = parser.token()
                    if not tok or tok.type in ('PUNTOCOMA','LLAVE_DER'):
                        break
                parser.errok()
            except Exception:
                pass
        else:
            # Marcamos recuperación exitosa
            try:
                parser.errok()
            except Exception:
                pass
    else:
        if report_syntax_errors:
            mensaje = "Error sintáctico: Fin de archivo inesperado"
            add_mensaje(mensaje)
            log_token(mensaje)
    _categorize_existing()
parser = yacc.yacc(module=sys.modules[__name__], write_tables=False, debug=False)

def post_semantic_scan(source: str):
    """Post-procesa el código fuente para detectar reasignaciones a variables
    inmutables y modificaciones de constantes que el parser pudo saltar debido
    a recuperación de errores/salvage.

    Patrón: IDENT (op) ... ; donde op es '=' o asignación compuesta.
    Ignora líneas que comienzan con 'let' o 'const'. Evita duplicados si ya hay
    mensajes sobre esa variable en errores_semanticos.
    """
    if not source:
        return
    asign_op_regex = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(=|\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=)\b")
    existing_errors = "\n".join(errores_semanticos)
    lines = source.splitlines()
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith('//'):
            continue
        # Evitar declaraciones
        if stripped.startswith('let ') or stripped.startswith('const '):
            continue
        m = asign_op_regex.match(stripped)
        if not m:
            continue
        nombre, operador = m.group(1), m.group(2)
        if nombre not in tabla_simbolos['variables']:
            # Ya se debería haber reportado como variable no declarada en fase normal
            continue
        info = tabla_simbolos['variables'][nombre]
        # Evitar duplicado si ya existe mensaje con esa variable y palabra clave
        if f"'{nombre}'" in existing_errors and ('inmutable' in existing_errors or 'constante' in existing_errors):
            continue
        col = line.find(nombre) + 1  # columna aproximada 1-based
        if isinstance(info, dict):
            if info.get('const', False):
                mensaje = f"Error semántico en la línea {idx}, columna {col}: No se puede modificar la constante '{nombre}'."
                add_mensaje(mensaje)
                log_token(mensaje)
            elif not info.get('mutable', False):
                mensaje = f"Error semántico en la línea {idx}, columna {col}: No se puede reasignar la variable inmutable '{nombre}'. Use 'let mut' para variables mutables."
                add_mensaje(mensaje)
                log_token(mensaje)
        existing_errors += "\n" + mensaje if 'mensaje' in locals() else ''

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
            mensaje_func = f"  {func}({params} params) -> {retorno}"
            print(mensaje_func)
            log_token(mensaje_func)
        
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