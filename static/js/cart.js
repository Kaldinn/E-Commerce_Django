let updateBtns = document.getElementsByClassName('update-cart')

for (i=0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function() {
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productID: ',productId, "Action: ", action)
        console.log('User: ', user)
        if(user == 'AnonymousUser'){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log("User is authenticated, sendig data.  ...")

    const url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action })
    })
    .then((Response) => {
        return Response.json();
    })
    .then((data) => {
        console.log('Data:', data)
        location.reload()
    })
}