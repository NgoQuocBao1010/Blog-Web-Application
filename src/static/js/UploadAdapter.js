class MyUploadAdapter {
    constructor(loader) {
        // CKEditor 5's FileLoader instance.
        this.loader = loader;

        // URL where to send files.
        this.url = `http://127.0.0.1:8000/post/ckeditor/image/`;
    }

    // Starts the upload process.
    upload() {
        return new Promise((resolve, reject) => {
            this._initRequest();
            this._initListeners(resolve, reject);
            this._sendRequest();
        });
    }

    // Aborts the upload process.
    abort() {
        if (this.xhr) {
            this.xhr.abort();
        }
    }

    // Example implementation using XMLHttpRequest.
    _initRequest() {
        const xhr = (this.xhr = new XMLHttpRequest());

        xhr.open("POST", this.url, true);
        xhr.responseType = "json";
    }

    // Initializes XMLHttpRequest listeners.
    _initListeners(resolve, reject) {
        const xhr = this.xhr;
        const loader = this.loader;
        const genericErrorText = "Couldn't upload file:";

        xhr.addEventListener("error", () => reject(genericErrorText));
        xhr.addEventListener("abort", () => reject());
        xhr.addEventListener("load", () => {
            const response = xhr.response;
            console.log(response);

            if (!response || response.error) {
                return reject(
                    response && response.error
                        ? response.error.message
                        : genericErrorText
                );
            }

            // If the upload is successful, resolve the upload promise with an object containing
            // at least the "default" URL, pointing to the image on the server.
            resolve({
                default: response.url,
            });
        });

        if (xhr.upload) {
            xhr.upload.addEventListener("progress", (evt) => {
                if (evt.lengthComputable) {
                    loader.uploadTotal = evt.total;
                    loader.uploaded = evt.loaded;
                }
            });
        }
    }

    // Prepares the data and sends the request.
    async _sendRequest() {
        const data = new FormData();
        const file = await this.loader.file;

        data.append("upload", file);

        this.xhr.send(data);
    }
}
