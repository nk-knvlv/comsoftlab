class ProgressBar {
    constructor(selector) {
        this.progressElement = document.querySelector(selector);
    }

    // Метод для обновления прогресса
    setProgress(value) {
        // Проверяем, чтобы значение было в пределах от 0 до 100
        if (value < 0 || value > 100) {
            console.warn('Значение должно быть в диапазоне от 0 до 100');
            return;
        }

        // Устанавливаем ширину прогресс-бара
        this.progressElement.style.width = value + '%';
    }
}

const progressBar = new ProgressBar('.progress-value');
const mail = document.querySelector(".mail");
const socket = new WebSocket('ws://127.0.0.1:8000/ws/some-url/');
message_count = 0
message_counter_el = document.querySelector(".message_count");

console.log('im ready');

socket.onmessage = function(event) {

    try {
        data = JSON.parse(event.data)
        console.log(data)
    } catch (e) {
        console.log('Error:', e.message);
    }

//    try {
//        progress_value = JSON.parse(event.data).message
//        progressBar.setProgress(progress_value);
//        message_counter_el.innerText = message_count
//        message_count++
//        console.log();
//    } catch (e) {
//        console.log('Error:', e.message);
//    }
};

// Закомментированный код
// document.addEventListener('DOMContentLoaded', () => {
// });

// socket.send(JSON.stringify({
//    messageType: 1,
// }));

 socket.onopen = function(e) {
     socket.send(JSON.stringify({
         messageType: 1,
         message: {'mail': mail.innerText}
     }));
 };
