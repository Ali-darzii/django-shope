

function filterProducts(){
    // debugger;
    const filterPrice = $('#sl2').val();
    const startPrice = filterPrice.split(',')[0];
    const endPrice = filterPrice.split(',')[1];
    $('#start_price').val(startPrice);
    $('#end_price').val(endPrice);
    $('#filter_form').submit();


}

function fillPage(page){
    $('#page').val(page);
    $('#filter_form').submit();
}

function ShowLargeImage(imageSrc){
    $('#main_image').attr('src', imageSrc);
    $('#show_large_image_modal').attr('href', imageSrc);
}



function AddProductToOrder(productId){
    // console.log(productId)
    const productCount = $('#product-count').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count= ' + productCount ).then(res => {
        if (res.status === 'invalid_count'){
            Swal.fire(
              '',
              'تعداد سفارش شما کمتر از ۱ است',
              'question'
            )
        }

        if (res.status === 'product_not_fount'){
            Swal.fire(
              '',
              'محصول شماپیدا نشد',
              'question'
            )
        }

        if (res.status === 'not_auth'){
            Swal.fire({
                  title: '<strong>شما باید ثبت نام یا ورود کنید</strong>',
                  icon: 'info',
                  html:
                    'می توانید برای <b>ورود</b>, ' +
                    '<a href="/login">کیلیک</a> ' +
                    'کنید',

                })
        }
        if (res.status === 'success'){
            Swal.fire({
                  position: 'top-end',
                  icon: 'success',
                  title: 'محصول شما به سبد خرید اضافه شد',
                  showConfirmButton: false,
                  timer: 2000
            })
        }

    });
}



function removeOrderDetail(detailId){
    $.get('/user/remove-order-detail?detail_id=' + detailId ).then(res => {
        if (res.status === 'success'){
            $('#order-detail-content').html(res.body);
        }
        // console.log(res);
    });
}


function changeOrderDetailCount(detailId,state){
    $.get('/user/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success'){
            $('#order-detail-content').html(res.body);
        }
        console.log(res);
    });
}

