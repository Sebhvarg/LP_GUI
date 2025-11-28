// -----------------------------------------------------
//     ALGORITMO DE PRUEBA AVANZADO (SIN COSAS RARAS)
// -----------------------------------------------------

fn main() {
    // ---------------- Declaraciones ----------------
    let mut a: i32 = 5;
    let mut b: i32 = 12;
    let mut suma: i32 = 0;
    let limite: i32 = 8;
    let activo: bool = true;

    // ---------------- Operaciones básicas ----------------
    suma = a + b;
    b = b - 3;
    a = a * 2;

    // ---------------- For simple ----------------
    for i in 0..limite {
        suma = suma + i;
    }

    // ---------------- If/else anidado ----------------
    if suma > 20 {
        println!("Suma mayor a 20");
    } else if suma == 20 {
        println!("Suma igual a 20");
    } else {
        println!("Suma menor a 20");
    }

    // ---------------- Loop con break ----------------
    let mut contador: i32 = 4;
    loop {
        suma = suma + contador;
        contador = contador - 1;
        if contador == 0 {
            break;
        }
    }

    // ---------------- Sombras de variable ----------------
    let suma: i32 = suma + 10;

    // ---------------- Expresión combinada ----------------
    let resultado: i32 = (a + b) * 2 - suma / 3;

    // ---------------- Mostrar resultado ----------------
    println!("Resultado final: {}", resultado);


    // -----------------------------------------------------
    //       ERRORES PARA PROBAR LOS 3 NIVELES
    // -----------------------------------------------------

    // ❌ Error léxico: símbolo inválido
    let dinero$ = 500;

    // ❌ Error sintáctico: falta '='
    let x: i32  10;

    // ❌ Error semántico: tipo incompatible
    let bandera: bool = 5;

    // ❌ Error semántico: operación inválida
    let mezclar: i32 = activo + 3;

    // -----------------------------------------------------
    // ERRORES ADICIONALES PARA GENERAR MÁS LOGS
    // -----------------------------------------------------

    // ❌ Error léxico: carácter ilegal
    let valor# = 10;

    // ❌ Error léxico: número mal formado
    let raro: i32 = 12a3;

    // ❌ Error sintáctico: falta ';'
    let p: i32 = 9

    // ❌ Error sintáctico: llave de más
    if a > 3 {{
        println!("error");
    }

    // ❌ Error sintáctico: operador mal puesto
    let s: i32 = + 5;

    // ❌ Error semántico: tipo incompatible
    let bandera2: bool = a + b;

    // ❌ Error semántico: variable usada sin declarar
    let h: i32 = variable_que_no_existe + 1;

    // ❌ Error semántico: reasignar tipo diferente
    let t: i32 = 5;
    t = false;
}
