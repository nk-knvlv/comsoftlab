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
    getMessage(){
        this.beginPath.style.flexGrow = (Number(window.getComputedStyle(this.beginPath).flexGrow) + 1/this.progressBarPercentValue) + ""
        this.endPath.style.flexGrow = (Number(window.getComputedStyle(this.endPath).flexGrow) - 1/this.progressBarPercentValue) + ""
    }
    // Метод для обновления прогресса
    changeSearchArea(searchArea) {
        if(this.search_area[0] != searchArea[0]){
            let diff = searchArea[0] - this.search_area[0]
            this.beginPath.style.flexGrow = Math.floor(searchArea[0]/this.progressBarPercentValue) + ""
            let endPathFlexGrow = Number(window.getComputedStyle(this.endPath).flexGrow)
            let beginPathFlexGrow = Number(window.getComputedStyle(this.beginPath).flexGrow)
            this.mainElement.style.flexGrow = (100 - Math.round(beginPathFlexGrow + endPathFlexGrow)) + ""
            this.search_area[0] = searchArea[0]
        }
        else {
            let diff = this.search_area[1] - searchArea[1]
            let currentEndPath = this.endPath.style.flexGrow
            this.endPath.style.flexGrow = Math.floor((this.search_area[1] - searchArea[1])/this.progressBarPercentValue) + ""

            let endPathFlexGrow = Number(window.getComputedStyle(this.endPath).flexGrow)
            if(endPathFlexGrow < 1){
                this.endPath.style.flexGrow = 0 + ""
            }
            let beginPathFlexGrow = Number(window.getComputedStyle(this.beginPath).flexGrow)
            this.mainElement.style.flexGrow = (100 - Math.round(beginPathFlexGrow + endPathFlexGrow)) + ""
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

    convertDate(dateStr){
            // Преобразуем строку в массив чисел
        const parts = dateStr.split(',').map(Number);

        // Создаем объект Date с использованием необходимых элементов массива
        const date = new Date(Date.UTC(parts[0], parts[1] - 1, parts[2]));

        // Форматируем дату в YY-MM-DD
        const year = date.getUTCFullYear();
        const month = String(date.getUTCMonth() + 1).padStart(2, '0'); // +1, т.к. месяцы начинаются с 0
        const day = String(date.getUTCDate()).padStart(2, '0');

        return `${year}-${month}-${day}`;
    }
    addMessage(table, message) {

//
//        // Проверяем, есть ли строка с сообщением "Нет объектов для отображения."
//        const noDataRow = table.querySelector('tr:first-child');
//        if (noDataRow) {
//            noDataRow.remove(); // Удаляем строку если она есть
//        }

        // Создаем новую строку
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${message.subject}</td>
            <td>${message.content}</td>
            <td>${this.convertDate(String(message.sent_date))}</td>
            <td>${this.convertDate(String(message.receive_date))}</td>
            <td>${message.attached_file_link_list}</td>

        `;
        // Добавляем строку в тело таблицы
        table.insertBefore(newRow, table.firstChild);
        this.getMessage()
    }
}



let table = document.querySelector('.table-wrapper')

let progressBar = new ProgressBar()
const mail = document.querySelector(".mail");
const socket = new WebSocket('ws://127.0.0.1:8000/ws/some-url/');
let message_count = 0
let message_counter_el = document.querySelector(".message_count");
let progressBarPercentValue = 0
table = document.querySelector(".message-table");
console.log('im ready');
socket.onmessage = function(event) {
  let data = JSON.parse(event.data)
        let messageType = data.message_type
        if(messageType == 2){
            progressBar.progressBarPercentValue = data.search_area[1]/100
            progressBar.search_area = data.search_area
            progressBar.mainElement.style.flexGrow = 0 + ""
            progressBar.beginPath.style.flexGrow = 0 + ""
            progressBar.endPath.style.flexGrow = 100 + ""
            const noDataElement = table.querySelector('.no-objects');
            if (noDataElement) {
                noDataElement.remove();
            }
        }
        if(messageType == 3){
            progressBar.progressBarPercentValue = data.search_area[1]/100
            progressBar.search_area = data.search_area
        }

        if(messageType == 4){
            message_count++
            message_counter_el.innerText = message_count
            progressBar.changeSearchArea(data.search_area)
        }

        if(messageType == 5){
            let result_uid = data.result_uid
            progressBar.startBlinking()
        }

        if(messageType == 6){
            progressBar.addMessage(table, data.message)
        }

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
