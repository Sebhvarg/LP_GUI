
// ========== ERRORES LÉXICOS ==========

// ERROR LÉXICO: Comentario de bloque sin cerrar


// ERROR LÉXICO: Identificador con tilde (carácter inválido)
let función = 5;

// ERROR LÉXICO: Identificador con ñ
let año = 2024;

// ERROR LÉXICO: Número flotante mal formado (dos puntos decimales)
let precio = 19.99.5;

let mensaje = "Hola mundo";

// ERROR LÉXICO: Carácter con escape inválido
let escape_invalido = "texto qerror";

// ERROR LÉXICO: Carácter especial no válido §
let operacion = 10 § 5;

// ERROR LÉXICO: Carácter especial € en código
let costo = 100 € ;

// ERROR LÉXICO: Identificador que comienza con número
let 123variable = 10;

// ERROR LÉXICO: Operador no válido <>
let comparacion = 5 <> 3;

// ERROR LÉXICO: Palabra reservada como identificador
let struct = 10;
let fn = 20;
let while = 30;

// ERROR LÉXICO: Número con underscore al final sin dígito
let valor = 100_;

// ERROR LÉXICO: Lifetime mal formado
fn vida<'a'b>(x: &'a'b str) {
    println!("Error");
}

// ========== ERRORES SINTÁCTICOS ==========

// ERROR SINTÁCTICO: struct sin punto y coma al final
struct Book {
    id: u32,
    title: str,
    author: str
}  // Falta punto y coma aquí

// ERROR SINTÁCTICO: función sin palabra clave fn
nueva_funcion() {
    println!("Error sintáctico");
}

// ERROR SINTÁCTICO: función sin tipo de retorno pero con return
fn obtener_dato() {
    return "texto";  // Falta especificar -> str
}

// ERROR SINTÁCTICO: parámetros sin coma separadora
fn sumar(a: i32 b: i32) -> i32 {
    a + b
}

// ERROR SINTÁCTICO: falta -> en tipo de retorno
fn contar() i32 {
    42
}

// ERROR SINTÁCTICO: if sin condición
fn revisar() {
    if {
        println!("Sin condición");
    }
}

// ERROR SINTÁCTICO: for sin paréntesis correctos
fn ciclo_mal() {
    for i in 1..10
        println!("{}", i);
    }
}

// ERROR SINTÁCTICO: while sin llaves
fn mientras_error() {
    while (true)
        break;
}

// ERROR SINTÁCTICO: match sin brazos
fn patron_vacio(x: i32) -> str {
    match x {
    }
}

// ERROR SINTÁCTICO: match con coma en lugar de =>
fn patron_incorrecto(num: i32) -> str {
    match num {
        1, "uno",
        2, "dos",
        _, "otro",
    }
}

// ERROR SINTÁCTICO: vector sin comas
fn vector_mal() {
    let nums = vec![1 2 3 4 5];
}

// ERROR SINTÁCTICO: llamada a función sin comas
fn llamada_error() {
    alguna_funcion(1 2 3);
}

// ERROR SINTÁCTICO: declaración sin let/const
fn asignacion_invalida() {
    variable = 100;
}

// ERROR SINTÁCTICO: punto y coma faltante
fn falta_puntoycoma() {
    let x = 10
    let y = 20;
}

// ERROR SINTÁCTICO: paréntesis sin cerrar
fn parentesis_abierto() {
    let resultado = (10 + 20;
}

// ERROR SINTÁCTICO: llave sin cerrar
fn llave_abierta() {
    if (true) {
        println!("Test");
    // Falta llave de cierre
}

// ERROR SINTÁCTICO: loop sin cuerpo
fn bucle_vacio() {
    loop
}

// ERROR SINTÁCTICO: enum sin variantes
enum EstadoVacio {
}

// ERROR SINTÁCTICO: trait sin llaves correctas
trait MiRasgo
    fn metodo(&self);
}

// ERROR SINTÁCTICO: impl sin llave de apertura
impl MiRasgo for Book
    fn metodo(&self) {
        println!("Impl incorrecto");
    }
}

// ERROR SINTÁCTICO: operador ++ no válido
fn incremento_invalido() {
    let x = 5 ++ 3;
}

// ERROR SINTÁCTICO: struct con = en lugar de :
fn inicializar_mal() {
    let libro = Book {
        id = 1,
        title = "Título",
    };
}

// ========== ERRORES SEMÁNTICOS ==========

// ERROR SEMÁNTICO: Redeclaración de variable
fn redeclaracion() {
    let contador = 0;
    let contador = 10;  // Ya declarada
}

// ERROR SEMÁNTICO: Redeclaración de constante
fn constante_duplicada() {
    const MAX = 100;
    const MAX = 200;  // Ya declarada
}

// ERROR SEMÁNTICO: Uso de variable no declarada
fn variable_no_declarada() {
    let resultado = no_existe + 10;
}

// ERROR SEMÁNTICO: Modificar variable inmutable
fn inmutable_modificacion() {
    let valor = 50;
    valor = 60;  // No se puede modificar sin mut
}

// ERROR SEMÁNTICO: Modificar constante
fn modificar_constante() {
    const LIMITE = 1000;
    LIMITE = 2000;  // No se puede modificar constante
}

// ERROR SEMÁNTICO: Operación entre tipos incompatibles
fn tipos_incompatibles() {
    let texto = "100";
    let numero = 50;
    let resultado = texto + numero;  // str + i32
}

// ERROR SEMÁNTICO: Comparación entre tipos incompatibles
fn comparacion_invalida() {
    let cadena = "abc";
    let entero = 123;
    if (cadena == entero) {  // str == i32
        println!("Incompatible");
    }
}

// ERROR SEMÁNTICO: Operación aritmética con tipo no numérico
fn aritmetica_invalida() {
    let palabra = "texto";
    let suma = palabra + 5;  // str no es numérico
}

// ERROR SEMÁNTICO: Multiplicación de strings
fn multiplicar_strings() {
    let str1 = "hola";
    let str2 = "mundo";
    let prod = str1 * str2;  // No se puede multiplicar strings
}

// ERROR SEMÁNTICO: División de booleanos
fn division_bool() {
    let a = true;
    let b = false;
    let c = a / b;  // bool no es numérico
}

// ERROR SEMÁNTICO: Llamada a función no declarada
fn funcion_inexistente() {
    let resultado = funcion_que_no_existe();
}

// ERROR SEMÁNTICO: Redeclaración de función
fn calcular() -> i32 {
    42
}
fn calcular() -> i32 {  // Ya declarada
    50
}

// ERROR SEMÁNTICO: Tipo incompatible en declaración explícita
fn tipo_explicito_incorrecto() {
    let numero: i32 = "texto";  // i32 != str
}

// ERROR SEMÁNTICO: Constante con tipo incompatible
fn constante_tipo_mal() {
    const VALOR: u32 = "cadena";  // u32 != str
}

// ERROR SEMÁNTICO: Variable con tipo explícito incompatible con asignación
fn declaracion_tipo_incompatible() {
    let edad: u32 = 25.5;  // u32 != f64
}

// ERROR SEMÁNTICO: Acceso a variable no declarada en tupla
fn tupla_variable_inexistente() {
    let valor = tupla_no_existe.0;
}

// ERROR SEMÁNTICO: Acceso a índice de variable no declarada
fn array_no_declarado() {
    let elemento = arreglo_inexistente[0];
}

// ERROR SEMÁNTICO: Mezcla de enteros y flotantes sin conversión
fn mezcla_numerica() {
    let entero: i32 = 10;
    let flotante: f64 = 20.5;
    let mezcla = entero + flotante;  // Tipos incompatibles
}

// ERROR SEMÁNTICO: Operación módulo con flotantes
fn modulo_flotante() {
    let a: f32 = 10.5;
    let b: f32 = 3.2;
    let mod_val = a % b;  // % no es compatible con f32
}

// ERROR SEMÁNTICO: Llamada a método en tipo string con nombre incorrecto
fn metodo_string_invalido() {
    let texto = "hola mundo";
    let longitud = texto.length();  // Debe ser len(), no length()
}

// ERROR SEMÁNTICO: Llamada a método numérico en string
fn metodo_tipo_incorrecto() {
    let cadena = "123";
    let valor = cadena.abs();  // abs() es para números, no strings
}

// ERROR SEMÁNTICO: Método string con argumentos incorrectos
fn args_incorrectos() {
    let texto = "ejemplo";
    let resultado = texto.len(5);  // len() no acepta argumentos
}

// ERROR SEMÁNTICO: Método numérico sin argumentos cuando los necesita
fn metodo_sin_args() {
    let numero = 16;
    let potencia = numero.pow();  // pow() requiere un argumento
}

// ERROR SEMÁNTICO: Variable mutable reasignada con tipo incompatible
fn reasignacion_tipo_mal() {
    let mut valor = 100;  // i32
    valor = "texto";  // Intenta asignar str a i32
}

// ERROR SEMÁNTICO: Uso de += en variable no mutable
fn incremento_inmutable() {
    let contador = 0;
    contador += 1;  // contador no es mut
}

// ERROR SEMÁNTICO: Uso de -= en constante
fn decremento_constante() {
    const TOTAL = 100;
    TOTAL -= 10;  // No se puede modificar constante
}

// ERROR SEMÁNTICO: Operador compuesto en tipo no numérico
fn compuesto_no_numerico() {
    let texto = "hola";
    texto += " mundo";  // str no soporta +=
}

// ERROR SEMÁNTICO: Incremento ++ en Rust (no existe)
fn doble_incremento() {
    let mut i = 0;
    i++;  // Rust no tiene ++
}

// ERROR SEMÁNTICO: Decremento -- en Rust (no existe)
fn doble_decremento() {
    let mut j = 10;
    j--;  // Rust no tiene --
}

// ERROR SEMÁNTICO: Comparación de Option con valor directo
fn option_comparacion() {
    let maybe: Option<i32> = Some(5);
    if (maybe == 5) {  // Debe ser Some(5) o unwrap
        println!("Incorrecto");
    }
}

// ERROR SEMÁNTICO: Asignación de None a tipo no Option
fn none_a_tipo_normal() {
    let valor: i32 = None;  // i32 no puede ser None
}

// ERROR SEMÁNTICO: Variable usada antes de inicialización
fn variable_sin_inicializar() {
    let x;
    println!("{}", x);  // x no está inicializada
}

// ERROR SEMÁNTICO: Función que retorna valor pero no todas las ramas
fn retorno_incompleto(condicion: bool) -> i32 {
    if (condicion) {
        42
    }
    // Falta else con return
}

// ERROR SEMÁNTICO: División por cero literal
fn division_cero() {
    let resultado = 100.0 / 0.0;
}

// ERROR SEMÁNTICO: Intentar indexar String directamente
fn indexar_string() {
    let texto = "hola";
    let caracter = texto[0];  // No se puede indexar String así
}

// ERROR SEMÁNTICO: Uso de self fuera de impl
fn usar_self() {
    self.hacer_algo();  // self solo existe en métodos
}

// ERROR SEMÁNTICO: Retornar valor en función que no especifica retorno
fn retorno_inesperado() {
    if (true) {
        return 42;  // Función no especifica tipo de retorno
    }
}

// ERROR SEMÁNTICO: Llamada a método con número incorrecto de parámetros
fn parametros_incorrectos(a: i32, b: i32) -> i32 {
    a + b
}

fn llamada_mal_parametros() {
    let resultado = parametros_incorrectos(5);  // Faltan parámetros
}

// ERROR SEMÁNTICO: Método push en entero (no existe)
fn push_en_numero() {
    let numero = 42;
    numero.push(5);  // i32 no tiene método push
}

// ERROR SEMÁNTICO: Variable declarada pero nunca usada
fn variable_sin_usar() {
    let dato_sin_uso = 100;
    let otro_dato = 200;
    // Advertencia: dato_sin_uso no se usa
}

// ERROR SEMÁNTICO: Constante declarada pero nunca usada
fn constante_sin_usar() {
    const CONFIGURACION = 500;
    // Advertencia: CONFIGURACION no se usa
}

// ERROR SEMÁNTICO: Parámetro de función nunca usado
fn parametro_sin_usar(valor: i32, otro: i32) -> i32 {
    valor  // otro nunca se usa
}

// ERROR SEMÁNTICO: Ciclo infinito de tipos en struct
struct Nodo {
    valor: i32,
    siguiente: Nodo,  // Debería ser Box<Nodo> u Option<Box<Nodo>>
}

// ERROR SEMÁNTICO: Intentar usar tipo no declarado
fn tipo_inexistente() {
    let obj: TipoQueNoExiste = 10;
}

// ERROR SEMÁNTICO: Acceso a campo inexistente en struct
fn campo_inexistente() {
    let libro = Book {
        id: 1,
        title: "Título",
        author: "Autor",
    };
    let paginas = libro.pages;  // Campo 'pages' no existe
}

// ERROR SEMÁNTICO: Modificar campo de struct inmutable
fn struct_inmutable() {
    let libro = Book {
        id: 1,
        title: "Título",
        author: "Autor",
    };
    libro.id = 2;  // libro no es mut
}

// ERROR SEMÁNTICO: Operación lógica con tipos no booleanos
fn logica_no_bool() {
    let a = 10;
    let b = 20;
    if (a && b) {  // a y b son i32, no bool
        println!("Error");
    }
}

// ERROR SEMÁNTICO: Negación lógica en tipo no booleano
fn negacion_no_bool() {
    let numero = 5;
    let resultado = !numero;  // ! requiere bool, no i32
}

// ERROR SEMÁNTICO: OR lógico con números
fn or_con_numeros() {
    let x = 1;
    let y = 0;
    if (x || y) {  // || requiere bool
        println!("Error");
    }
}

// Función main con múltiples errores
fn main() {
    // ERROR SEMÁNTICO: Variable ya declarada
    let total = 0;
    let total = 100;
    
    // ERROR SEMÁNTICO: Constante modificada
    const MAXIMO = 1000;
    MAXIMO = 2000;
    
    // ERROR SEMÁNTICO: Suma de tipos incompatibles
    let texto = "valor";
    let numero = 50;
    let mezcla = texto + numero;
    
    // ERROR SINTÁCTICO: Falta punto y coma
    let x = 10
    let y = 20;
    
    // ERROR LÉXICO: Carácter inválido
    let precio = 100 € ;
    
    // ERROR SEMÁNTICO: Función no declarada
    let resultado = funcion_desconocida();
    
    // ERROR SEMÁNTICO: Variable no declarada
    let final_val = variable_fantasma + 10;
    
    // ERROR SEMÁNTICO: Modificar inmutable
    let inmutable = 5;
    inmutable = 10;
    
    // ERROR SINTÁCTICO: Vector sin comas
    let valores = vec![1 2 3];
    
    // ERROR SEMÁNTICO: Método inexistente
    let palabra = "test";
    palabra.metodo_inventado();
    
    println!("Programa con errores para pruebas");
}

