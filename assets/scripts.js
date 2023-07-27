var editor = CodeMirror.fromTextArea(document.getElementById("input_text_area"), {
         mode: "python",
         theme: "darcula",
         lineNumbers: true,
         autofocus: true
         });


// all imported modes from CodeMirror
var highlightModes = {
	'py': 'python',
	'js': 'javascript',
  	'java': 'text/x-java',
  	'c': 'text/x-csrc',
  	'cpp': 'text/x-c++src',
  	'dart': 'dart',
  	'go': 'go',
  	'swift': 'swift'
	};

function updateHighlightMode() {
        var selectedLanguage = document.getElementById('lang_menu').value;
	var mode = highlightModes[selectedLanguage];
	editor.setOption('mode', mode);
	}


// changes default "main.py" to "main...." onchange of lang list
document.getElementById("file_name").value = "main";
function updateFileName() {
      var fileNameInput = document.getElementById("file_name");
      var selectedLanguage = document.getElementById("lang_menu").value;
      var fileName = fileNameInput.value.split(".")[0];
      fileNameInput.value = fileName + "." + selectedLanguage;
    }

// returns "true" if "Use tests:" is checked on
function updateCheckboxState() {
      var checkbox = document.getElementById("checkbox");
      var isChecked = checkbox.checked;
      return isChecked;
}


// copies "caseBlock" and appends it to "<div class=UNIX-output...>"
let indexes_of_failed_cases;
function updateUnixOutput() {
	const outputBlock = document.getElementById('UNIX-output');
    	const caseBlock = document.getElementById('unix-output-block');
	
	outputBlock.innerHTML = '';

	for (let i = 0; i < numberOfCases; i++) {
		const clonedCaseBlock = caseBlock.cloneNode(true);
		clonedCaseBlock.style.display = 'block';
		const caseTitle = clonedCaseBlock.querySelector('#case_text');
		caseTitle.textContent = listOfCases[i];
		if (indexes_of_failed_cases.includes(i) || i === numberOfCases) {
			clonedCaseBlock.style.border = 'solid red';
		} else if (!indexes_of_failed_cases.includes(i)) {
			clonedCaseBlock.style.border = 'solid green';
		}
		outputBlock.appendChild(clonedCaseBlock);
		}
	}


let processedText;
let numberOfCases;
let listOfCases;
// Is called when play button is pressed
// creates request, apppend data to it, and sends on handler.py or tester.py (depends on checkboxState)
function sendData() {
         const xhttp = new XMLHttpRequest();
         const userText = editor.getValue();
         const language = document.getElementById('lang_menu').value;
         /*const fileName = document.getElementById('file_name').value;*/
	 const isChecked = updateCheckboxState();
         let url = 'cgi-bin/handler.py';

	if (isChecked) {
		url = 'cgi-bin/tester.py';
	}

         document.getElementById('output_text_area').value = '\u231B Loading...';
         const formData = new FormData();
         formData.append('user_text', userText);
         formData.append('progr_lang', language);
         /*formData.append('file_name', fileName);*/
	 formData.append('checkboxState', isChecked);

	// gets processed data back
         xhttp.onreadystatechange = function() {
               if (this.readyState == 4 && this.status == 200) {
                 const response = JSON.parse(this.responseText);
                 processedText = response.text;
		 numberOfCases = response.number_of_cases;
		 indexes_of_failed_cases = response.indexes_of_failed_cases;
		 listOfCases = processedText.split('%%%');
		 if (isChecked) {
			 document.getElementById('output_text_area').value = "";
			 updateUnixOutput();
		 } else {
                 	document.getElementById('output_text_area').value = processedText;
                 	}
		}
                };

                 xhttp.open('POST', url, true);
                 xhttp.send(formData);
                }



const toggleButton = document.getElementById('checkbox');
const column2 = document.getElementById('UNIX-output');

toggleButton.addEventListener('click', function() {
  column2.classList.toggle('hide');
});



// Attaches file
const attachButton = document.querySelector('.attach_button');
attachButton.addEventListener('click', () => {
         const input = document.createElement('input');
         input.type = 'file';

         input.addEventListener('change', () => {
           const file = input.files[0];
           const reader = new FileReader();

         reader.addEventListener('load', () => {
         editor.setValue(reader.result);
         });

         reader.readAsText(file);
         });

         input.click();
         });
