const addToCart = (url, csrfToken) => {
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            productId: $('#add-button').val(),
            csrfmiddlewaretoken: csrfToken,
            action: 'post'
        },
        success: (json) => {
            $('#cart-qty').html('Cart ' + json.qty);
        },
        error: (xhr, errMsg, err) => {
           console.log(errMsg);
        }
    });
}

const removeFromCart = (btn, url, csrfToken) => {
    let productId = $(btn).data('index');
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            productId: $(btn).data('index'),
            csrfmiddlewaretoken: csrfToken,
            action: 'post'
        },
        success: (json) => {
            $('.product-item[data-index="' + productId + '"]').remove();
            $('#total-price').html(json.totalPrice + ' UC');
        },
        error: (xhr, errMsg, err) => {
           console.log(errMsg);
        }
    });
}