function SearchKeyword(){
  var param = document.getElementById('form_kw').value;
  location.href = location.protocol + '/search_keyword?keyword=' + param + '&page=1';
}