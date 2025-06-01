document.addEventListener('DOMContentLoaded', function () {
    // Get the modal-content element
    var modalContent = document.getElementById('panoramaContainer');

    // Get the width and height of the modal-content element
    var width = modalContent.clientWidth;
    var height = modalContent.clientHeight;

    // Set the width and height of the panorama
    var panorama = document.getElementById('panorama');
    panorama.style.width = width + 'px';
    panorama.style.height = height + 'px';
});


function add_panorama() {
    var viewer = pannellum.viewer('panorama', {
        "default": {
            "firstScene": "scene1",
            "showLoading": false,
            "autoLoad": true
        },
        "scenes": {
            "scene1": {
                "type": "equirectangular",
                "panorama": "test13.jpg",
                "autoLoad": true,
                "showLoading": false
            },
            "scene2": {
                "type": "equirectangular",
                "panorama": "test14.jpg",
                "autoLoad": true,
                "showLoading": false
            }
        }
    });

    var scenes = ['scene1', 'scene2'];

    // Get the backward and forward buttons
    var backButton = document.getElementById('back');
    var forwardButton = document.getElementById('forward');

    // Add click event listeners to the buttons
    backButton.addEventListener('click', function() {

        console.log('back button clicked!');
        // Get the current scene index
        var currentSceneIndex = scenes.indexOf(viewer.getScene());

        // Calculate the index of the previous scene
        var prevSceneIndex = (currentSceneIndex - 1 + scenes.length) % scenes.length;

        // Switch to the previous scene
        viewer.loadScene(scenes[prevSceneIndex]);
    });

    forwardButton.addEventListener('click', function() {


        console.log('forward button clicked!');
        // Get the current scene index
        var currentSceneIndex = scenes.indexOf(viewer.getScene());

        // Calculate the index of the next scene
        var nextSceneIndex = (currentSceneIndex + 1) % scenes.length;

        // Switch to the next scene
        viewer.loadScene(scenes[nextSceneIndex]);
    });
}


document.addEventListener('DOMContentLoaded', function () {
    const runButton = document.getElementById('startVirtuallyWalk');
    const modal = document.getElementById("myModal");

    runButton.addEventListener('click', function () {
        console.log('start virtually walk clicked!');

        modal.style.display = "block";

        // Get the elements to hide
        const topInfoBar = document.querySelector(".top-info-bar");
        const sideUI = document.querySelector(".SideUI");
        const arrowButton = document.querySelector(".arrow-button");

        // Hide the elements
        topInfoBar.style.display = "none";
        sideUI.style.display = "none";
        arrowButton.style.display = "none";

        add_panorama();
    });
});


