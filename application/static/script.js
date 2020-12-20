// Toggling the sidebar, triggered by the buttnon in class 'toolbar'
function toggleSidebar() {
	let sidebar = document.getElementById("Sidebar");
	let logo = document.getElementById("Logo");
	let content = document.getElementById("Content");
	sidebar.classList.toggle("closedSidebar");
	logo.classList.toggle("closedLogo");
	content.classList.toggle("openContent");
}

// Toggling Edit Table Name Button
function toggleEditButtonVis(id){
	let editButton = document.getElementById(id);
	console.log(editButton);
	editButton.hidden = false; 
}
function toggleEditButtonHid(id){
	let editButton = document.getElementById(id);
	console.log(editButton);
	editButton.hidden = true; 
}

let dropbox;

dropbox = document.getElementById("dropbox");
dropbox.addEventListener("dragenter", dragenter, false);
dropbox.addEventListener("dragover", dragover, false);
dropbox.addEventListener("drop", drop, false);

function dragenter(e) {
  e.stopPropagation();
  e.preventDefault();
}

function dragover(e) {
  e.stopPropagation();
  e.preventDefault();
}

function drop(e) {
  e.stopPropagation();
  e.preventDefault();

  const dt = e.dataTransfer;
  const files = dt.files;

  handleFiles(files);
}