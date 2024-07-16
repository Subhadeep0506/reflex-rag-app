import reflex as rx
import os
import time

import requests


class UploadExample(rx.State):
    uploading: bool = False
    ingesting: bool = False
    progress: int = 0
    total_bytes: int = 0
    ingestion_url = "http://127.0.0.1:8089/ingest"

    async def handle_upload(self, files: list[rx.UploadFile]):
        self.ingesting = True
        yield
        for file in files:
            file_bytes = await file.read()
            file_name = file.filename
            files = {
                "file": (os.path.basename(file_name), file_bytes, "multipart/form-data")
            }
            response = requests.post(self.ingestion_url, files=files)
            self.ingesting = False
            yield
            if response.status_code == 200:
                # yield rx.redirect("/chat")
                self.show_redirect_popup()

    def handle_upload_progress(self, progress: dict):
        self.uploading = True
        self.progress = round(progress["progress"] * 100)
        if self.progress >= 100:
            self.uploading = False

    def cancel_upload(self):
        self.uploading = False
        return rx.cancel_upload("upload3")

    def show_redirect_popup(self):
        rx.alert_dialog.root(
            rx.alert_dialog.trigger(
                rx.button("Revoke access", color_scheme="red"),
            ),
            rx.alert_dialog.content(
                rx.alert_dialog.title("Redirect to Chat Interface?"),
                rx.alert_dialog.description(
                    "You will be redirected to the Chat Interface.",
                    size="2",
                ),
                rx.flex(
                    rx.alert_dialog.cancel(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                        ),
                    ),
                    rx.alert_dialog.action(
                        rx.button(
                            "Continue",
                            color_scheme="green",
                            variant="solid",
                            on_click=rx.redirect("/chat"),
                        ),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                style={"max_width": 450},
            ),
        )


def upload_form():
    return rx.vstack(
        rx.upload(
            rx.flex(
                rx.text(
                    "Drag and drop file here or click to select file",
                    font_family="Ubuntu",
                ),
                rx.icon("upload", size=30),
                direction="column",
                align="center",
            ),
            id="upload3",
            border="1px solid rgb(233, 233,233, 0.4)",
            margin="5em 0 10px 0",
            background_color="rgb(107,99,246)",
            border_radius="8px",
            padding="1em",
        ),
        rx.vstack(rx.foreach(rx.selected_files("upload3"), rx.text)),
        rx.cond(
            ~UploadExample.ingesting,
            rx.button(
                "Upload",
                on_click=UploadExample.handle_upload(
                    rx.upload_files(
                        upload_id="upload3",
                        on_upload_progress=UploadExample.handle_upload_progress,
                    ),
                ),
            ),
            rx.flex(
                rx.spinner(size="3", loading=UploadExample.ingesting),
                rx.button(
                    "Cancel",
                    on_click=UploadExample.cancel_upload,
                ),
                align="center",
                spacing="3",
            ),
        ),
        align="center",
    )
