/**
 * Uploads images asynchronously. Displays temporary image renderings, shows
 * progress bars, and warns users against navigating away from the page while
 * the uploads are working.
 */

export default async function upload(file, name, uri) {
    const formData = new FormData();
    formData.append(name, file);
    let response = await fetch(uri, {
        method: "POST",
        body: formData
    });
    return response;
}
