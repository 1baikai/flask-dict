function getXhr() {
        // {#如果浏览器支持XMLHttpRequest，则创建XMLHttpRequest的对象并返回#}
    if (window.XMLHttpRequest){
        return new XMLHttpRequest();
    } else {
        // {# 如果不支持则创建ActiveObject的对象并返回#}
            return new ActiveXObject("Microsoft.XMLHTTP")
        }
    }
