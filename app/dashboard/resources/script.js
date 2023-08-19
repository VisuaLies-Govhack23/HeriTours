function openTab(evt, tabName) {
    var i, tabContent, tabButtons;

    tabContent = document.getElementsByClassName('tab-pane');
    for (i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = 'none';
    }

    tabButtons = document.getElementsByClassName('tab-button');
    for (i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }

    document.getElementById(tabName).style.display = 'block';
    evt.currentTarget.classList.add('active');
}

function showPopup() {
    var popup = document.getElementById("quizPopup");
    popup.style.display = "flex";
}

// Function to show the answers
function showAnswers() {
    var answersDiv = document.getElementById("answers");
    answersDiv.style.display = "block";
}

function hidePopup() {
    var popup = document.getElementById("quizPopup");
    popup.style.display = "none";
}

// Automatically show the pop-up when the page loads
document.addEventListener("DOMContentLoaded", function () {
    showPopup();});

// You can also add code here to embed Tableau dashboards using Tableau's JavaScript API.
