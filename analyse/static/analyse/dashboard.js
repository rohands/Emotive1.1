var firstMessage;
var positiveMessage;
var negativeMessage;
var userName;
var phoneNumber;
var radioForm;
var sendMessage;
var btnFirst;
var btnPos;
var btnNeg;

function init()
{
	firstMessage = document.getElementById("first_message");
	positiveMessage = document.getElementById("positive_message");
	negativeMessage = document.getElementById("negative_message");
	userName = document.getElementById("name");
	phoneNumber = document.getElementById("phone");
	radioForm = document.getElementById("radio_buttons");
	sendMessage = document.getElementById("send_sms");
	btnFirst = document.getElementById("btn_first");
	btnPos = document.getElementById("btn_pos");
	btnNeg = document.getElementById("btn_neg");
}

function updateEntries()
{
	if(userName.value.trim() === "" || phoneNumber.value.trim() === "" || getRadioVal(radioForm,"product_type") === "NA")
		alert("Make sure to enter all the fields before clicking on update button!");
	else
	{
		var product_type = getRadioVal(radioForm,"product_type");
		firstMessage.value = `Hi ${userName.value}, I saw that your ${product_type} was delivered. How are you enjoying it so far?`;
		positiveMessage.value = `Great, can you describe what you love most about your ${product_type}?`;
		negativeMessage.value = `I am sorry to hear that! What do you dislike about ${product_type}?`;

		//Activate Send Button

		sendMessage.disabled = false;
		btnFirst.disabled = false;
		btnPos.disabled = false;
		btnNeg.disabled = false;
	}
	
}

function getRadioVal(form, name) {
    var val = "NA";
    var radios = form.elements[name];
    for (var i=0, len=radios.length; i<len; i++) {
        if (radios[i].checked) 
        {
            val = radios[i].value;
            break;
        }
    }
    return val;
}

function enable(element)
{
	element.readOnly = false;
}

function clearAll()
{
	sendMessage.disabled = true;
	btnFirst.disabled = true;
	btnPos.disabled = true;
	btnNeg.disabled = true;

	firstMessage.readOnly = true;
	positiveMessage.readOnly = true;
	negativeMessage.readOnly = true;

	firstMessage.value = "";
	positiveMessage.value = "";
	negativeMessage.value = "";
}

function textHim()
{	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() 
	{
	    if (this.readyState == 4 && this.status == 200) 
	    {
	      alert(this.responseText);
	    }
	    else if (this.readyState == 4 && this.status != 200)
	    {
	    	alert("Check your entries and try again!")
	    }
  	};
	xhttp.open("POST", "/analyse/send_sms/", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(`name=${userName.value}&phone=${phoneNumber.value}&pos=${positiveMessage.value}&neg=${negativeMessage.value}&first=${firstMessage.value}`);
}