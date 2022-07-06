$(document).ready(function () {
    console.log('hello')
    console.log($("header"))
  $("header ul li").hover(function (e) {
    e.preventDefault()
    $(this).find("ul").css("display", "block")
  }, function (e) {
    e.preventDefault()
    $(this).find("ul").css("display", "none")
  });
});
