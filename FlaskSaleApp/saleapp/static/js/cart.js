function addToCart(id, name, price) {
    fetch("/api/carts", {
        method: "post",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        })
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName("cart-counter");
        for (let e of d)
            e.innerText = data.total_quantity;
    })
}

function updateCart(productId, obj) {
    fetch(`/api/cart/${productId}`, {
        method: "put",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "quantity": parseInt(obj.value)
        })
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName("cart-counter");
        for (let e of d)
            e.innerText = data.total_quantity;

        let d2 = document.getElementsByClassName("cart-amount");
        for (let e of d2)
            e.innerText = data.total_amount.toLocaleString("en");
    })
}

function deleteCart(productId) {
    if (confirm("Chắc chắn xóa sản phẩm khỏi giỏ?") === true) {
        fetch(`/api/cart/${productId}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            let d = document.getElementsByClassName("cart-counter");
            for (let e of d)
                e.innerText = data.total_quantity;

            let d2 = document.getElementsByClassName("cart-amount");
            for (let e of d2)
                e.innerText = data.total_amount.toLocaleString("en");

            let e = document.getElementById(`product${productId}`);
            e.style.display = "none";
        });
    }
}