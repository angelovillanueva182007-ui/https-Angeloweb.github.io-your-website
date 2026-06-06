function updateStats() {
    const totalItems = inventory.length;

    const totalQty = inventory.reduce(
        (acc, item) => acc + parseInt(item.quantity),
        0
    );

    const totalCost = inventory.reduce(
        (acc, item) => acc + (item.price * item.quantity),
        0
    );

    const totalProfit = inventory.reduce(
        (acc, item) =>
            acc + ((item.sellingPrice - item.price) * item.quantity),
        0
    );

    document.getElementById('totalItems').innerText = totalItems;
    document.getElementById('totalQty').innerText = totalQty;
    document.getElementById('totalCost').innerText =
        '₱' + totalCost.toFixed(2);

    document.getElementById('totalProfit').innerText =
        '₱' + totalProfit.toFixed(2);
}