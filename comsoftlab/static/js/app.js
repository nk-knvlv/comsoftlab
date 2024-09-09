document.addEventListener('DOMContentLoaded', () => {

const socket = new WebSocket('ws://127.0.0.1:8000/ws');

const btn = document.querySelector(".btn");
const mailInput = document.querySelector("#mail");
const passInput = document.querySelector("#password");


btn.addEventListener('click', () => {
    console.log('Меня нажали')
    console.log(mailInput.value)
    console.log(passInput.value)
  });

socket.onopen = function(e) {
  socket.send(JSON.stringify({
    messageType: 1,
    message: 'Hello from Js client'
  }));
};

socket.onmessage = function(event) {
  try {
    console.log(event);
  } catch (e) {
    console.log('Error:', e.message);
  }
};
});
