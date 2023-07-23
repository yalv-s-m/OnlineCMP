import Foundation

if let input = readLine(), let number = Double(input) {
    let result = number * 4
    
    print("Результат умножения: \(result)")
} else {
    print("Ошибка ввода. Пожалуйста, введите число.")
}
