// test_matriz.rs
fn main() {
    // Matriz 2D (sin anotación de tipo para ajustarse a la gramática soportada)
    let matriz = [[1, 2], [3, 4]];
    println!("matriz[0][1] = {}", matriz[0][1]); // Esperado: 2
    println!("matriz[1][0] = {}", matriz[1][0]); // Esperado: 3

    // Matriz 3D (anidada)
    let matriz3d = [
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]]
    ];
    println!("matriz3d[1][0][1] = {}", matriz3d[1][0][1]); // Esperado: 6

    // Lista simple
    let lista = [1, 2, 3];
    println!("lista[2] = {}", lista[2]); // Esperado: 3

    // Acceso fuera de rango (comentado para evitar detener análisis)
    // let error = matriz[2][0];
}
