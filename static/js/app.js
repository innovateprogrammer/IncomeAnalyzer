
function logout()
{
    localStorage.removeItem('signedin');
    window.open('/',target="_self");
}

var uname=localStorage.getItem('uname');
var upass=localStorage.getItem('upass');
var uemail=localStorage.getItem('uemail');
var usercolor=localStorage.getItem('usercolor');
var utype=localStorage.getItem('utype');
document.getElementById('user').value=uname;
document.getElementById('cu').innerHTML=uname;
var app = angular.module('myApp', []);
    app.controller('myCtrl', function($scope) {
        $scope.user=uname[0].toUpperCase();
    });

window.onload=()=>{
    
    
    var signin=localStorage.getItem('signedin');
    if(signin=="true")
    {
        document.getElementById('usercir').style.backgroundColor=usercolor;
    }
    else
    {
        window.open('/',target="_self");
    }

}


