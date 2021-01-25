const taskInput = document.querySelector('.input')
const dateInput = document.querySelector('.date-input')
const buttonInput = document.querySelector(".submit")

buttonInput.addEventListener('click', resetFields)

function resetFields() {
    taskInput.value = "";
    dateInput.value = "";
}