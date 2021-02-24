load_posts()
// Load all posts on page load
function load_posts() {
    $.ajax({
        url : "/api/category/", // the endpoint
        type : "GET", // http method
        // handle a successful response
        success : function(json) {
            for (var i = 0; i < json.length; i++) {
                // console.log(json[i])
                if (json[i].parent==null){
                    $("#categories").prepend("<ul>"+get_child(json, json[i])+"</ul>");}
                    // $(".navbar").after("<ul>"+get_child(json, json[i])+"</ul>");}
                    // $("#categories").prepend("<li id='post-"+json[i].id+"'><strong>"+json[i].name+"</strong>"+
                    // "<ul>"+get_child(json, json[i])+"</ul>"+"</li>");}
            }
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function sub_child(json,parent_id) {
    var childs = []
    for (var item in json){
        if (json[item].parent==parent_id){
            childs.push(json[item])
        }
    }
    return childs
};

function get_child(json,parent) {
    res = '<li><a href="category/'+parent.id+'/" class="text-decoration-none">'+parent.name+'</a></li>'
    var ch = sub_child(json, parent.id)
    if (ch){res += '<ul>'} 
    for (var x in ch){
        res += get_child(json,ch[x])
    }
    if (ch){res += '</ul>'} 
    return res
};


var emptyRow=$("#tag").clone()

function newrow() {
    console.log('clicked')
    // console.log(emptyRow)
    cloneRow(emptyRow)
}

function cloneRow($input){
    // console.log($input)
    var $newRow=$input.clone().appendTo(".all-tags")}


// set like for posts
function like(post_id,value) {
    $.ajax({
        url: "/api/like-by-post/"+post_id,
        type: "GET",
        success : function(json) {
            var csrf = $('input[name ="csrfmiddlewaretoken"]')[0].value
            json = json[0]
            if (json){
                if (json.value == value){
                    console.log('must delete')
                    console.log(csrf)
                    $.ajax({
                        url:'/api/like-post/'+json.id,
                        headers: {
                            "X-CSRFTOKEN":csrf,
                        },
                        type: "DELETE",
                        success : function() {
                            console.log("success delete");
                            if (value){
                                $('#like-btn').toggleClass('btn-danger btn-outline-danger')
                                $('#like_quantity').text((+$('#like_quantity').text()-1))
                            }else{
                                $('#dislike-btn').toggleClass('btn-secondary btn-outline-secondary')
                                $('#dislike_quantity').text((+$('#dislike_quantity').text()-1))
                            }
                        },
                    })
                }else{
                    console.log('most update')
                    $.ajax({
                        url:'/api/like-post/'+json.id,
                        headers: {
                            "X-CSRFTOKEN":csrf,
                        },
                        type: "PUT",
                        data: {
                            'post' : post_id,
                            'value' : value,
                        },
                        success : function() {
                            if (value){
                                $('#like-btn').toggleClass('btn-danger btn-outline-danger')
                                $('#dislike-btn').toggleClass('btn-secondary btn-outline-secondary')
                                $('#like_quantity').text((+$('#like_quantity').text()+1))
                                $('#dislike_quantity').text((+$('#dislike_quantity').text()-1))
                            }else{
                                $('#like-btn').toggleClass('btn-danger btn-outline-danger')
                                $('#dislike-btn').toggleClass('btn-secondary btn-outline-secondary')
                                $('#like_quantity').text((+$('#like_quantity').text()-1))
                                $('#dislike_quantity').text((+$('#dislike_quantity').text()+1))
                            }
                        },
                    })
                }
            }else{
                console.log('postt')
                $.ajax({
                    url:'/api/like-post/',
                    type: "POST",
                    headers: {
                        "X-CSRFTOKEN":csrf,
                    },
                    data: {
                        'post' : post_id,
                        'value' : value,
                    },
                    success : function(json) {
                        if (json.value){
                            $('#like-btn').toggleClass('btn-danger btn-outline-danger')
                            $('#like_quantity').text((+$('#like_quantity').text()+1))
                        }else{
                            $('#dislike-btn').toggleClass('btn-secondary btn-outline-secondary')
                            $('#dislike_quantity').text((+$('#dislike_quantity').text()+1))
                        }
                    },
                })
            }
        },
    })
}

// set comment of posts
$('#successMessage').hide();
function commentsend(post_id) {
    var csrf_token = $('input[name ="csrfmiddlewaretoken"]')[0]
    var textarea = $('#id_text')
    $.ajax({
        url: "/api/comment/creata/",
        type: "POST",
        data: {
            "csrfmiddlewaretoken":csrf_token.value,
            'text' : textarea[0].value,
            'comment' : comment_id,
        },
        success : function() {
            console.log("success"); 
            $('.btn-outline-primary').click()
            textarea.val("")
            $('#successMessage').show(500);
        },
    })
}

function like_comment(my,comment_id,value) {
    var like_btn = $(my).parent().children('#like')
    var dislike_btn = $(my).parent().children('#dislike')
    var like_quantity = $(my).parent().children('small').children('#like_quantity')
    var dislike_quantity = $(my).parent().children('small').children("#dislike_quantity")
    $.ajax({
        url: "/api/like-by-comment/"+comment_id,
        type: "GET",
        success : function(json) {
            var csrf = $('input[name ="csrfmiddlewaretoken"]')[0].value
            json = json[0]
            if (json){
                if (json.value == value){
                    console.log('must delete')
                    console.log(csrf)
                    $.ajax({
                        url:'/api/like-comment/'+json.id,
                        headers: {
                            "X-CSRFTOKEN":csrf,
                        },
                        type: "DELETE",
                        success : function() {
                            console.log("success delete");
                            if (value){
                                like_btn.toggleClass('btn-danger btn-outline-danger')
                                like_quantity.text((+like_quantity.text()-1))
                            }else{
                                dislike_btn.toggleClass('btn-secondary btn-outline-secondary')
                                dislike_quantity.text((+dislike_quantity.text()-1))
                            }
                        },
                    })
                }else{
                    console.log('most update')
                    $.ajax({
                        url:'/api/like-comment/'+json.id,
                        headers: {
                            "X-CSRFTOKEN":csrf,
                        },
                        type: "PUT",
                        data: {
                            'comment' : comment_id,
                            'value' : value,
                        },
                        success : function() {
                            if (value){
                                like_btn.toggleClass('btn-danger btn-outline-danger')
                                dislike_btn.toggleClass('btn-secondary btn-outline-secondary')
                                like_quantity.text((+like_quantity.text()+1))
                                dislike_quantity.text((+dislike_quantity.text()-1))
                            }else{
                                like_btn.toggleClass('btn-danger btn-outline-danger')
                                dislike_btn.toggleClass('btn-secondary btn-outline-secondary')
                                like_quantity.text((+like_quantity.text()-1))
                                dislike_quantity.text((+dislike_quantity.text()+1))
                            }
                        },
                    })
                }
            }else{
                console.log('postt')
                $.ajax({
                    url:'/api/like-comment/',
                    type: "POST",
                    headers: {
                        "X-CSRFTOKEN":csrf,
                    },
                    data: {
                        'comment' : comment_id,
                        'value' : value,
                    },
                    success : function(json) {
                        if (json.value){
                            like_btn.toggleClass('btn-danger btn-outline-danger')
                            like_quantity.text((+like_quantity.text()+1))
                        }else{
                            dislike_btn.toggleClass('btn-secondary btn-outline-secondary')
                            dislike_quantity.text((+dislike_quantity.text()+1))
                        }
                    },
                })
            }
        },
    })
}