import magic


def get_extension_from_binary(file_obj):
    head = file_obj.read(2048)
    file_obj.seek(0)

    mime = magic.from_buffer(head, mime=True)

    extensions = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "application/pdf": ".pdf",
    }

    return extensions.get(mime, ".bin")
