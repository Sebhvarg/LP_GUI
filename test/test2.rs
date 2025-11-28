// Algoritmo para sumar pares y probar errores
fn main() {
    let mut limite: i32 = 10;
    let mut suma: i32 = 0;
    let mut contador: i32 = 0;

    println!("Iniciando suma de pares");

    // Ciclo para sumar solo números pares
    while (contador <= limite) {
        if (contador % 2 == 0) {
            suma = suma + contador;
            println!("Sumando: ", contador);
        } else {
            // No es par, continuamos
            let mut temporal: i32 = 1;
        }
        contador = contador + 1;
    }

    println!("La suma total es: ", suma);

    // Estructura if final
    if (suma > 20) {
        println!("Suma grande");
    }

    // ---------------------------------------------
    // ZONA DE ERRORES LÉXICOS SOLICITADOS
    // Estos caracteres causarán los errores en el log
    // ---------------------------------------------
    
    let dinero = 100$;   // Provoca error con $
    let codigo# = 50;    // Provoca error con #
    let correo@ = "abc"; // Provoca error con @
    let grados° = 35;    // Provoca error con °
}