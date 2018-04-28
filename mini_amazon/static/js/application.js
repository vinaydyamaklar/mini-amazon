window.onload = function(){
    var hdn_uname = document.getElementById('hdn_uname').value;
    if(isEmpty(hdn_uname)){
        document.getElementById("btn_login").style.visibility='visible';
        document.getElementById("btn_logout").style.visibility='hidden';
    }else{
        document.getElementById("btn_login").style.visibility='hidden';
        document.getElementById("btn_logout").style.visibility='visible';
    }
};


var isEmpty = function(data) {
    if(typeof(data) === 'object'){
        if(JSON.stringify(data) === '{}' || JSON.stringify(data) === '[]'){
            return true;
        }else if(!data){
            return true;
        }
        return false;
    }else if(typeof(data) === 'string'){
        if(!data.trim()){
            return true;
        }
        return false;
    }else if(typeof(data) === 'undefined'){
        return true;
    }else{
        return false;
    }
}

function addProductToCart(){
    var userName = document.getElementById('hdn_uname');
    var productId = document.getElementById('');
}