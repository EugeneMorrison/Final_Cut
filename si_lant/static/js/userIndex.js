// При первой загрузке сортируем по дате отгрузки, если order_by не задан
if (!localStorage.getItem('pageLoaded')) {
    if (typeof location.search.split('order_by=')[1] == "undefined") {
        reload();
    }
}

// Сортировка
function setOrder_by(name) {
    let params = new URLSearchParams(window.location.search);
    params.set('order_by', name);
    window.location.search = params.toString();
}

// Универсальный фильтр для всех полей
function setFilter(field, value) {
    let params = new URLSearchParams(window.location.search);
    if (value) {
        params.set(field, value);
    } else {
        params.delete(field);
    }
    window.location.search = params.toString();
}

// Сброс всех фильтров
function reset() {
    window.location.href = "?order_by=shipment_date";
}

// Перезагрузка с актуальными параметрами
function reload() {
    let params = new URLSearchParams(window.location.search);
    if (!params.has('order_by')) {
        params.set('order_by', 'shipment_date');
    }
    window.location.search = params.toString();
}