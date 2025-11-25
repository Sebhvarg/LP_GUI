# ------------------------------------------------------------ 
# lexer.py
# Analizador Léxico usando PLY
# Grupo 10
# ------------------------------------------------------------
# Integrantes:
#   Derian Baque Choez (fernan0502)
#   Sebastian Holguin (Sebhvarg)
#   Carlos Ronquillo (carrbrus)
# ------------------------------------------------------------
import ply.lex as lex
import datetime
import os
import subprocess
import sys

# ------------------------------------------------------------
# Definición de los tokens 
# ------------------------------------------------------------
tokens = [
    # ---------------- Aporte Fernando, Sebastian ----------------
    'IDENTIFICADOR', 'ENTERO', 'CADENA', 'FLOTANTE',
    'IGUAL', 'SUMA', 'RESTA', 'MULT', 'DIV',
    'PAREN_IZQ', 'PAREN_DER', 'LLAVE_IZQ', 'LLAVE_DER',
    'PUNTOCOMA', 'PUNTO', 'POTENCIA',
    'MENOR', 'COMA', 'DOSPUNTOS', 'CARACTER', 'BOOLEANO',
    'IGUALDOBLE',
    # Comentarios
    'COMENTARIO_LINEA', 'COMENTARIO_BLOQUE',
    #Operadores Relacionales y Lógicos
    'MAYOR', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'DIFERENTE',
    'Y', 'O', 'NO', 
    #Otros simbolos
    'CORCHETE_IZQ', 'CORCHETE_DER',  'FLECHA', 'INTERROGACION',
    'RANGO', 'RANGO_INCLUIDO',

    # ---------------- Fin Fernando, Sebastian -------------------

    # ---------------- Aporte Carlos ----------------
    # Operadores bit a bit
    'BIT_Y',         # &
    'BIT_O',          # |
    'BIT_XO',         # ^
    'BIT_NO',         # ~
    'DESPLAZAR_IZQ',   # <<
    'DESPLAZAR_DER',   # >>

    # Asignación compuesta
    'MAS_IGUAL',       # +=
    'MENOS_IGUAL',     # -=
    'POR_IGUAL',       # *=
    'DIV_IGUAL',       # /=
    'MOD_IGUAL',       # %=
    'Y_IGUAL',       # &=
    'O_IGUAL',        # |=
    'XO_IGUAL',       # ^=
    'DESP_IZQ_IGUAL',  # <<=
    'DESP_DER_IGUAL',  # >>=
    'FLECHA_DOBLE',  # =>
    'GUION_BAJO',  # _
    # ---------------- Fin Carlos ----------------

    ]
    
reservadas = {
    # -------- Aporte Fernando, Sebastian --------
    'if': 'SI', 'else': 'SINO', 'for': 'POR', 'while': 'MIENTRAS',
    'fn': 'FUNCION', 'return': 'RETORNO', 'let': 'VARIABLE',
    'const': 'CONSTANTE', 'true': 'VERDAD', 'false': 'FALSO',
    'break': 'QUIEBRE', 'print!': 'IMPRIMIR', 'input': 'ENTRADA',
    'continue': 'CONTINUAR', 'println!': 'IMPRIMIRLN', 'new': 'NUEVO',
    'delete': 'ELIMINAR', 'switch': 'SWITCH', 'case': 'CASO',
    'default': 'DEFECTO', 'Vec': 'VECTOR', 'vec!': 'VECTOR_MACRO',
    

     # ---------------- Fin Fernando, Sebastian -------------------
    
     # ---------------- Aporte Carlos ----------------
    'mut': 'MUTABLE', 'struct': 'ESTRUCTURA', 'enum': 'ENUMERADO',
    'impl': 'IMPLEMENTACION', 'trait': 'RASGO', 'mod': 'MODULO', 'use': 'USO',
    'pub': 'PUBLICO', 'self': 'MISMO', 'super': 'SUPER', 'as': 'COMO',
    'static': 'ESTATICO', 'match': 'COINCIDIR', 'loop': 'LAZO', 'in': 'EN',
    'where': 'DONDE', 'move': 'MOVER', 'ref': 'REFERENCIA', 'type': 'TIPO',
    'crate': 'PAQUETE', 'unsafe': 'INSEGURO', 'async': 'ASINCRONO', 'await': 'ESPERAR',
    'dyn': 'DINAMICO', 'class': 'CLASE',
    
    #tipo de datos
    'i8': 'I8', 'i16': 'I16', 'i32': 'I32', 'i64': 'I64', 'i128': 'I128',
    'u8': 'U8', 'u16': 'U16', 'u32': 'U32', 'u64': 'U64', 'u128': 'U128',
    'f32': 'F32', 'f64': 'F64', 'bool': 'BOOLEANO_TIPO', 'char': 'CARACTER_TIPO',
    'str': 'CADENA_TIPO', 'usize': 'UTIPO', 'isize': 'ITIPO',
    }
    # ---------------- Fin Carlos ----------------

tokens = tokens + list(reservadas.values())

# ------------------------------------------------------------
# Expresiones regulares para tokens simples
# ------------------------------------------------------------
# -------- Aporte Fernando --------
t_IGUAL = r'='
t_SUMA       = r'\+'
t_RESTA      = r'-'
t_MULT       = r'\*'
t_DIV        = r'/'
t_PAREN_IZQ  = r'\('
t_PAREN_DER  = r'\)'
t_LLAVE_IZQ  = r'\{'
t_LLAVE_DER  = r'\}'
t_PUNTOCOMA  = r';'
t_PUNTO      = r'\.'
t_MODULO     = r'%'
t_POTENCIA   = r'\^'
t_MENOR      = r'<'
t_COMA       = r','
t_DOSPUNTOS  = r':'

# -------- Fin Fernando --------


#--------- Aporte Sebastian --------
t_MAYOR      = r'>'
t_MAYOR_IGUAL  = r'>='
t_MENOR_IGUAL  = r'<='
t_IGUALDOBLE   = r'=='
t_DIFERENTE    = r'!='
t_Y          = r'&&'
t_O           = r'\|\|'
t_NO          = r'!'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_FLECHA       = r'->'
t_INTERROGACION= r'\?'
t_RANGO        = r'\.\.'
t_RANGO_INCLUIDO = r'\.\.='
t_FLECHA_DOBLE = r'=>'
t_GUION_BAJO = r'_'
#--------- Fin Sebastian --------

# Reglas especiales para macros de impresión (antes de t_IDENTIFICADOR y t_NO)
def t_IMPRIMIRLN(t):
    r'println!'
    return t

def t_IMPRIMIR(t):
    r'print!'
    return t

# -------- Aporte Carlos --------
# Asignación compuesta (más largos primero)
t_MAS_IGUAL      = r'\+='
t_MENOS_IGUAL    = r'-='
t_POR_IGUAL      = r'\*='
t_DIV_IGUAL      = r'/='
t_MOD_IGUAL      = r'%='
t_Y_IGUAL      = r'&='
t_O_IGUAL       = r'\|='
t_XO_IGUAL      = r'\^='
t_DESP_IZQ_IGUAL = r'<<='
t_DESP_DER_IGUAL = r'>>='

# Operadores bit a bit
t_DESPLAZAR_IZQ  = r'<<'
t_DESPLAZAR_DER  = r'>>'
t_BIT_Y        = r'&'
t_BIT_O         = r'\|'
t_BIT_XO        = r'\^'
t_BIT_NO        = r'~'
# -------- Fin Carlos --------


# ------------------------------------------------------------
# Reglas con acciones
# ------------------------------------------------------------
# -------- Aporte Fernando --------
def t_COMENTARIO_LINEA(t):
    r'//.*'
    pass  # Ignorar comentarios de línea
def t_COMENTARIO_BLOQUE(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass  # Ignorar comentarios de bloque
def t_IDENTIFICADOR(t):
    r'[a-zA-ZáéíóúÁÉÍÓÚñÑ_][a-zA-Z0-9áéíóúÁÉÍÓÚñÑ_]*'
    t.type = reservadas.get(t.value, 'IDENTIFICADOR')
    return t
def t_FLOTANTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

t_ignore = ' \t'

def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



def t_error(t):
    mensaje = f"❌ Error léxico: carácter no reconocido '{t.value[0]}' en línea {t.lineno}"
    print(mensaje)
    log_token(mensaje)
    t.lexer.skip(1)

# -------- Fin Fernando --------
# ------------------------------------------------------------
def t_CARACTER(t):
    r"\'([^\\\n]|\\.)?\'"
    return t

def t_BOOLEANO(t):
    r'\b(true|false)\b'
    return t
# -------- Fin Aporte -------------

# ------------------------------------------------------------
#  Función para obtener el usuario de Git automáticamente
# ------------------------------------------------------------
def get_git_user():
    try:
        name = subprocess.check_output(["git", "config", "user.name"], encoding="utf-8").strip()
        if name:
            return name
    except:
        pass
    # fallback si no hay user.name configurado
    return os.getenv("USER") or os.getenv("USERNAME") or "usuarioGit"

# ------------------------------------------------------------
#  Función para guardar logs
# ------------------------------------------------------------
def log_token(mensaje):
    usuario = get_git_user()  # obtiene automáticamente el usuario de Git
    fecha_hora = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"lexico-{usuario}-{fecha_hora}.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(mensaje + "\n")

# ------------------------------------------------------------
#  Construcción del lexer
# ------------------------------------------------------------
lexer = lex.lex()

# ------------------------------------------------------------
#  Ejecución manual del analizador
# ------------------------------------------------------------
if __name__ == "__main__":
    print("Analizador léxico iniciado.\n")
    # Permite pasar el archivo por argumento o pedirlo por consola
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
    else:
        archivo = input("Ingrese la ruta del archivo a analizar: ").strip()

    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            data = f.read()
            lexer.input(data)

            while True:
                tok = lexer.token()
                if not tok:
                    break
                mensaje = f"Línea {tok.lineno}: {tok.type} -> {tok.value}"
                print(mensaje)
                log_token(mensaje)

        print("\n✅ Análisis léxico completado. Revise la carpeta 'logs' para ver el resultado.")

    except FileNotFoundError:
        print("❌ Archivo no encontrado. Verifique la ruta e intente nuevamente.")