var unames=[];
function login(){
    var uname="";
    var password=0;
    users=localStorage.getItem('userslist').split(",");
    pass=localStorage.getItem('passlist').split(",");
    emails=localStorage.getItem('emailslist').split(",");
    color=localStorage.getItem('colorlist').split(",");
    types=localStorage.getItem('typlist').split(",");
    userpass={};
    useremail={};
    usercol={};
    usertyp={};
    for(var k=0;k<users.length;k++)
    {
        userpass[users[k]]=pass[k];
        useremail[users[k]]=emails[k];
        usercol[users[k]]=color[k];
        usertyp[users[k]]=types[k];
    }
    uname=document.getElementById('name').value;
    password=document.getElementById('password').value;
    
    /* check valid login*/
    if(password==userpass[uname])
    {
        localStorage.setItem('signedin',true);
        localStorage.setItem('uname',uname);
        localStorage.setItem('upass',userpass[uname]);
        localStorage.setItem('uemail',useremail[uname]);
        localStorage.setItem('usercolor',usercol[uname]);
        localStorage.setItem('utype',usertyp[uname]);
        window.open("incomeanalyzer",target="_self");
    }
    else
    {
        window.alert("Incorrect username or password");
    }
}

function connectdb()
{
    /* code to connect to db and fetch password from database*/
    var st="https://script.google.com/macros/s/AKfycbwAzWCtTdEaYe40BLhPsApuy_3EIvw_sPCi_CW-q-AlNcnMR0dL4B9icK_JJiYFq24/exec";
    fetch(st)
    .then(res => res.text())
    .then(rep=>{
        
        var uemails=[]
        var upasses=[]
        var ucolors=[]
        var utypes=[]
        data = JSON.parse(rep);
        for(var i in data.content)
        {
            uname=String(data.content[i][0]);
            uemail=String(data.content[i][1]);
            upass=data.content[i][2];
            ucolor=data.content[i][3];
            utype=String(data.content[i][4]);
            unames.push(uname);
            uemails.push(uemail);
            upasses.push(upass);
            ucolors.push(ucolor);
            utypes.push(utype);
        }
        
        localStorage.setItem('userslist',unames);
        localStorage.setItem('emailslist',uemails);
        localStorage.setItem('passlist',upasses);
        localStorage.setItem('colorlist',ucolors);
        localStorage.setItem('typlist',utypes);
        
    });
    
}
window.onload=()=>{
    var signedin=localStorage.getItem('signedin');
    
    if(signedin==="true")
    {
        window.open("incomeanalyzer",target="_self");
    }
    connectdb();
    
}


$(function() {
    var availableTags =unames;
    $( "#name" ).autocomplete({
      source: availableTags
    });
  } );




