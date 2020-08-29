"use strict";

/**
 * 
 */

async function startSlideshow(rel_path) {
    let response = await fetch(`/slideshow/start/${rel_path}`);
    let message = await response.text();
    alert(message);
}

async function stopSlideshow() {
    let response = await fetch('/slideshow/stop');
    let message = await response.text();
    alert(message);
}
