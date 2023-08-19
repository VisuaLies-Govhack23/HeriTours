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

// You can also add code here to embed Tableau dashboards using Tableau's JavaScript API.
