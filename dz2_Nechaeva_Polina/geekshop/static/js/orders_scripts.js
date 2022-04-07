window.onload = function () {

    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];

    let TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;


    for (let i=0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($(`input[name="orderitems-${i}-quantity"]`).val());
        _price = parseFloat($(`input[name="orderitems-${i}-price"]`).val());
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
        price_arr[i] = 0;
        }
    }

    $('.order_form').on('click', 'input[type="number"]', function(){
        orderitem_num = parseInt($(this).attr('name').replace('orderitems-', '').replace('-quantity', ''));

        if (price_arr[orderitem_num]){
            orderitem_quantity = parseInt($(this).val());
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity)
        }
    })

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    $('.order_form select').change(function () {
        var target = event.target;
        console.log(target);
    });



    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());

        }

    function deleteOrderItem(row) {
        var target_name= row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }

}
