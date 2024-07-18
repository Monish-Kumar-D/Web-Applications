let history = [];


function appendToResult(value) {
    const result = document.getElementById('result');
    result.value += value;
}

function clearResult() {
    document.getElementById('result').value = '';
}

function deleteLastChar() {
    const result = document.getElementById('result');
    result.value = result.value.slice(0, -1);
}

function updateHistoryDisplay() {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = '';
    history.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = `${item[0]} = ${item[1]}`;
        historyList.appendChild(listItem);
    });
}

function addToHistory(exp,entry) {
    let item = [exp,entry]
    history.push(item);
    updateHistoryDisplay();
}


function calculateResult() {
    const result = document.getElementById('result');
    try {
        let expression=result.value
        result.value = eval(result.value);
        addToHistory(expression,result.value);
    } catch (error) {
        result.value = 'Error';
    }
}


