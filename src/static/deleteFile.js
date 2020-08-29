"use strict";

/**
 * Deletes a file from the server's file uploads.
 * @param {!String} rel_path The relative path for the directory that contains
 *     the file, in relation to the server's uploads directory.
 * @param {!String} fname
 * @param {!Number} page The current pagination page.
 * TODO: Add support for deleting the last file on the current page.
 */
async function deleteFile(rel_path, fname, page) {
    let conf = confirm(`Are you sure you want to delete ${fname}? This operation cannot be undone.`);
    if (conf) {
        let response = await fetch(`/file/delete/${rel_path}/${fname}`, {
            method: "DELETE"
        });
        let message = await response.text();
        alert(message);
        if (response.ok) {
            window.location.replace(`/folder/${rel_path}?page=${page}`);
        }
    }
}
