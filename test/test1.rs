// -------------------------
//    ALGORITMO DE PRUEBA
// -------------------------

fn main() {

    let mut a: i32 = 10;
    let mut b: i32 = 4;
    let activo: bool = true;

    let lista: [i32; 5] = [3, 6, 1, 8, 2];

    let mut acc: i32 = 0;

    // BUCLE CORRECTO
    for i in 0..5 {
        acc = acc + lista[i];
    }

    if acc > 10 {
        a = a + acc;
    } else {
        a = a - acc;
    }

    // WHILE CORRECTO
    let mut k: i32 = 0;
    while k < 3 {
        b = b * 2;
        k = k + 1;
    }

    let resultado: i32 = (a + b) * acc / 2;
    println!("Resultado inicial: {}", resultado);

    // -------------------------
    //    ERRORES SEMÁNTICOS
    // -------------------------

    let acc: i32 = acc + 10;     
    let activo = true;            
    activo = false;              

    // -------------------------
    // ERRORES SINTÁCTICOS
    // -------------------------

    if (a > 5) {{}}
    if a > 5 ) {                     
        println!("error sintaxis");
    }

    for j in 1..(5 {                 
        println!("mal for");
    }

    while (a < 200 {                 
        a = a + 1;
    }

    if a > 10 {
        println!("ok")                
    else {                            
        println!("mal")
    }

    let p: i32 = 9                    
    let x: i32 = ;                  

    fn funcion() {                  
        let interno: i32 = 9;
    }
    };                                 


    let dinero$ = 40;     
    let valor# = 10;     
    let cont@dor = 33;   
    let mal° = 5;        
    println!(Hola);

    let acc = 2;        
    let acc = 3;          

    let activo = true;    
    activo = 5;           

    total = acc + 10;    
}