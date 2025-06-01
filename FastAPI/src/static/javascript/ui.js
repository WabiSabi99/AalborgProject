function toggleSideUI() {
    var sideUI = document.querySelector('.SideUI');
    var arrowButton = document.querySelector('.arrow-button');

    // If the arrow button is hidden, return immediately
    if (arrowButton.style.display === 'none') {
        return;
    }

    // we need to find the <i> under the .arrow-button
    var arrowIcon = arrowButton.querySelector('i');
    if (parseInt(sideUI.style.right) === 0) {
        sideUI.style.right = '-300px'; // Hide the side UI
        arrowButton.style.right = '0px'; // Move the arrow button to the edge

        // Remove the right arrow icon class and add the left arrow icon class
        arrowIcon.classList.remove('fas', 'fa-chevron-right');
        arrowIcon.classList.add('fas', 'fa-chevron-left');
        arrowButton.style.backgroundColor = 'rgba(44 44 46, 0.9)';
    } else {
        sideUI.style.right = '0px'; // Show the side UI
        arrowButton.style.right = '295px'; // Move the arrow button closer to the side UI

        // Remove the left arrow icon class and add the right arrow icon class
        arrowIcon.classList.remove('fas', 'fa-chevron-left');
        arrowIcon.classList.add('fas', 'fa-chevron-right');

        // change .arror-button css  background-color: rgba(35 55 75 / 90%); to background-color: rgba(35 55 75 / 100%);
        arrowButton.style.backgroundColor = 'rgba(44 44 46, 1)';

    }
}

function toggleClick(element) {
    if (element.classList.contains('click')) {
        element.classList.remove('click');
        element.style.backgroundColor = ""; // Reset to original color
    } else {
        element.classList.add('click');
        setTimeout(function () {
            element.style.backgroundColor = "gainsboro"; // Set to clicked color after animation
        }, 500); // After the animation duration
    }
}


document.addEventListener('DOMContentLoaded', function () {
    // Get the close button
    const closeButton = document.querySelector('.close');

    // Add click event listener
    closeButton.addEventListener('click', function() {
        // Get the modal
        const modal = document.getElementById('myModal');

        // Hide the modal
        modal.style.display = 'none';

        // Get the elements to show
        const topInfoBar = document.querySelector(".top-info-bar");
        const sideUI = document.querySelector(".SideUI");
        const arrowButton = document.querySelector(".arrow-button");

        // Show the elements
        topInfoBar.style.display = "flex";
        sideUI.style.display = "block";
        arrowButton.style.display = "flex";
    });
});
