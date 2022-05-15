// If browser has user preference this will try pick it up
let userPreference = window.matchMedia("(prefers-color-scheme: dark)"); 
// If user has visited before retrieve value
let themeStored = localStorage.getItem('theme') === "true";

// First time user comes to site theme is not set, default to preference
if (themeStored === null) {
	if (userPreference.matches) 
		setDarkMode();
	else
		setLightMode();
} else {
	if (themeStored)
		setDarkMode();
	else 
		setLightMode();
}

function setDarkMode() {
	document.documentElement.setAttribute('theme', 'dark');
	localStorage.setItem('theme', true);
	$("#darkModeSwitch")[0].checked = true;
}

function setLightMode() {
	document.documentElement.setAttribute('theme', 'light');
	localStorage.setItem('theme', false);
	$("#darkModeSwitch")[0].checked = false;
}

function darkModeSwitch() {
    var mode = localStorage.getItem('theme') === "true";
    if (mode) 
        setLightMode();
    else
        setDarkMode();
}

// add event handler for change
$("#darkModeSwitch").change(darkModeSwitch);
