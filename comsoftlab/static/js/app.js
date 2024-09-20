class ProgressBar {
    constructor() {
        this.mainElement = document.querySelector('.progress-bar-middle-path');
        this.beginPath = document.querySelector('.progress-bar-begin-path');
        this.endPath = document.querySelector('.progress-bar-end-path');
        this.progressBarPercentValue = false
        this.search_area = false
        this.blinkInterval = null
    }

    // Метод для обновления прогресса
    setProgress(value) {
        // Проверяем, чтобы значение было в пределах от 0 до 100
        if (value < 0 || value > 100) {
            console.warn('Значение должно быть в диапазоне от 0 до 100');
            return;
        }

        // Устанавливаем ширину прогресс-бара
        this.mainElement.style.width = value + '%';
    }
    // Метод для обновления прогресса
    changeSearchArea(searchArea) {
        if(this.search_area[0] != searchArea[0]){
            let diff = searchArea[0] - this.search_area[0]
            console.log(diff)
            this.mainElement.style.flexGrow = (Number(window.getComputedStyle(this.mainElement).flexGrow) - diff) + ""
            this.beginPath.style.flexGrow = (searchArea[0]/this.progressBarPercentValue) + ""
            this.search_area[0] = searchArea[0]
        }
        if(this.search_area[1] != searchArea[1]){
            let diff = this.search_area[1] - searchArea[1]
            console.log(diff)
            this.mainElement.style.flexGrow = (Number(window.getComputedStyle(this.mainElement).flexGrow) - diff) + ""
            this.endPath.style.flexGrow = ((search_area[1] - searchArea[1])/this.progressBarPercentValue) + ""
        }
    }

     startBlinking() {
        if (!this.blinkInterval) {
            this.blinkInterval = setInterval(() => {
                this.mainElement.style.visibility = (window.getComputedStyle(this.mainElement).visibility === 'hidden' ? 'visible' : 'hidden');
            }, 100); // Меняет видимость каждые 200 мс
        }
                // Остановка моргания через 60 секунд (60000 мс)
        setTimeout(() => {
            this.stopBlinking();
        }, 3000); // Задержка в 60000 мс (60 секунд) // Задержка в 2000 мс
    }

    stopBlinking() {
        clearInterval(this.blinkInterval)
        this.blinkInterval = null;
        this.mainElement.style.visibility = 'visible'; // Убедимся, что элемент видим
    }

}

let progressBar = new ProgressBar()
const mail = document.querySelector(".mail");
const socket = new WebSocket('ws://127.0.0.1:8000/ws/some-url/');
let message_count = 0
let message_counter_el = document.querySelector(".message_count");
let progressBarPercentValue = 0
console.log('im ready');
let search_area = [0,0]
socket.onmessage = function(event) {
  let data = JSON.parse(event.data)
        let messageType = data.message_type
        if(messageType == 3){
            progressBar.progressBarPercentValue = data.search_area[1]/100
            progressBar.search_area = data.search_area
        }

        if(messageType == 4){
            progressBar.changeSearchArea(data.search_area)
        }

        if(messageType == 5){
            let result_uid = data.result_uid
            progressBar.startBlinking()
        }

        console.log(data)
//    try {
//
//    } catch (e) {
//        console.log('Error:', e.message);
//    }
};

 socket.onopen = function(e) {
     socket.send(JSON.stringify({
         messageType: 1,
         message: {'mail': mail.innerText}
     }));
 };
