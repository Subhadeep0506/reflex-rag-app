"""The main Chat app."""

import reflex as rx
from reflex_demo.components import chat, navbar, upload_form


@rx.page(route="/chat", title="RAG Chatbot")
def chat_interface() -> rx.Component:
    return rx.chakra.vstack(
        navbar(),
        chat.chat(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )


@rx.page(route="/", title="RAG Chatbot")
def index() -> rx.Component:
    return rx.chakra.vstack(
        navbar(),
        upload_form(),
        chat.action_bar(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )


# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="jade",
    ),
)
app.add_page(chat_interface)
