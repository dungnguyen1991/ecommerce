$(document).ready(function(){
    // Contact Form Handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")
    
    function displaySubmitting(submitBtn, defaultText, doSubmit){

        if (doSubmit){
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fas fa-spin fa-spinner'></i> Sending...")
        } else {
            submitBtn.removeClass("disabled")
            submitBtn.html(defaultText)
        }
    }

    contactForm.submit(function(event){
        event.preventDefault()

        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()

        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmitting(contactFormSubmitBtn, "", true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success:function(data){
                thisForm[0].reset()
                $.alert({
                    title: "Oops!",
                    content: "Thank you for your submission",
                    theme: "modern"
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            },
            error: function(error){
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg = ""

                $.each(jsonData, function(key, value){
                    msg += key + ": " + value[0].message + "<br />"
                })

                $.alert({
                    title: "Oops!",
                    content: msg,
                    theme: "modern"
                })

                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            }
        })
    })

    // auto search
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']") // input name='q'
    var typingTimer;
    var typingInterval = 500; // 1.5 seconds
    var searchBtn = searchForm.find("[type='submit']")
    var redirectTimer;

    searchInput.keyup(function(event){
        // key released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })

    searchInput.keydown(function(event){
        // key pressed
        clearTimeout(typingTimer)
        clearTimeout(redirectTimer)
    })

    function displaySearching(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fas fa-spin fa-spinner'></i> Searching...")
    }

    function performSearch(){
        displaySearching()
        var query = searchInput.val()
        redirectTimer = setTimeout(function(){
            window.location.href = '/search/?q=' + query
        }, 1000)
    }

    // Cart + add products
    var productForm = $(".form-product-ajax");

    function getOwnedProduct(productId, submitSpan){
        var actionEndpoint = '/orders/endpoint/verify/ownership/'
        var httpMethod = 'GET'
        var data = {
            product_id: productId
        }
        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: data,
            success: function(data){
                if (data.owner){
                    submitSpan.html('<a href="/library/">In Library</a>');
                }
            },
            error: function(err){
                console.log(err)
            }
        })
    }

    $.each(productForm, function(index, object){
        var $this = $(this);
        var isUser = $this.attr("data-user")
        var submitSpan = $this.find(".submit-span");
        var productInput = $this.find('[name="product_id"]');
        var productId = productInput.attr("value")
        var productIsDigital = productInput.attr("data-is-digital")
        
        if (productIsDigital && isUser){
            getOwnedProduct(productId, submitSpan)
        }   
    })

    productForm.submit(function(event){
        event.preventDefault();
        // console.log("Form is not sending")
        var thisForm = $(this);
        // var actionEndpoint = thisForm.attr("action");
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                var submitSpan = thisForm.find(".submit-span");
                if (data.added) {
                    submitSpan.html("<div class='btn-group'> <a class='btn btn-link' href='/cart/'>In cart</a> <button type='submit' class='btn btn-link'>Remove?</button></div>");
                } else {
                    submitSpan.html('<button type="submit" class="btn btn-success">Add to cart</button>');
                }

                var navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.cartItemCount)

                var currentPath = window.location.href
                if (currentPath.indexOf("cart") != -1) {
                    refreshCart()
                }
            },
            error: function(errorData){
                $.alert({
                    title: "Oops!",
                    content: "An error occurred",
                    theme: "modern"
                })
            }
        })
    });

    function refreshCart(){
        console.log("in current cart")
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        // cartBody.html("<h1>Changed</h1>")
        var productRows = cartBody.find(".cart-product")
        var currentUrl = window.location.href


        var refreshCartUrl = '/api/cart/';
        var refreshCartMethod = "GET";
        var data = {};
        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function(data){
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                if (data.products.length > 0){
                    productRows.html("")
                    i = data.products.length
                    $.each(data.products, function(index, value){
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display", "block")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend('<tr><th scope="row">'+ i +'</th><td><a href="'+value.url+'">'+ value.name +'</a>' + newCartItemRemove.html() + '</td><td>'+ value.price +'</td></tr>')
                        i --
                    })
                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                } else {
                    window.location.href = currentUrl
                }
                
            },
            error: function(errorData){
                $.alert({
                    title: "Oops!",
                    content: "An error occurred",
                    theme: "modern"
                })
            }
        })
    }
})