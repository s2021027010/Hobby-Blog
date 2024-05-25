function myFunction() {
	let text = document.getElementById("myInput").value;
	document.getElementById("demo").value += text + " ";  
	$('select option:not(:selected)').each(function(){
		$("."+text).attr('disabled', 'disabled');
	   });

  }
function yourFunction() {
  document.getElementById("myInput").style.display = "block";
  }
  
function weFunction() {
	document.getElementById("myInput").style.display = "none";
	}