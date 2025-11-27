// Programa con errores léxicos, sintácticos y semánticos

fn calcular(a: i32, b: i32) -> i32 {
    let resultado = a + b;
    resultado
}

fn main() {
    // Error léxico: caracteres no reconocidos
    let x @ = 10;  // @ no es válido
    let y$ = 20;   // $ no es válido
    
    // Error semántico: variable no declarada
    let suma = x + z;  // z no existe
    
    // Error sintáctico: falta punto y coma
    let mut contador = 0
    
    // Error semántico: reasignar variable inmutable
    let valor = 100
    valor = 200;  // valor no es mutable
    
    // Error semántico: tipos incompatibles
    let texto: str = "hola";
    let numero = texto + 5;  // no se puede sumar str con número
    
    // Error sintáctico: llave faltante en if
    if contador > 0 {
        println!("Mayor que cero")
    // Falta llave de cierre
    
    // Error semántico: variable no usada
    const PI = 3.14159;
    
    // Error sintáctico: paréntesis mal balanceados
    let resultado = calcular(10, 20;
    
    // Error léxico: número mal formado
    let decimal = 45..67;  // dos puntos consecutivos incorrectos
    
    // Error semántico: intentar modificar constante
    const MAX: i32 = 100;
    MAX = 200;
    
    // Error sintáctico: falta operador
    let calculo = 5 5;  // falta operador entre números
    
    // Error semántico: llamada a función inexistente
    let valor_func = funcionInexistente();
    
    // Error sintáctico: punto y coma doble
    let final = 42;;
    
    // Error semántico: uso de variable antes de declaración
    println!("{}", temprana);
    let temprana = 99;
}