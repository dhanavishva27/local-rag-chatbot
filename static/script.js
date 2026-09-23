const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");


function addMessage(
    content,
    type,
    sources = []
) {

    const message = document.createElement("div");

    message.className =
        `message ${type}-message`;


    const label = document.createElement("div");

    label.className = "message-label";

    label.textContent =
        type === "user"
            ? "You"
            : "Assistant";


    const messageContent =
        document.createElement("div");

    messageContent.className =
        "message-content";

    messageContent.textContent =
        content;


    message.appendChild(label);

    message.appendChild(messageContent);


    if (
        type === "bot" &&
        sources.length > 0
    ) {

        const sourcesContainer =
            document.createElement("div");

        sourcesContainer.className =
            "sources";


        const title =
            document.createElement("div");

        title.className =
            "sources-title";

        title.textContent =
            "Sources";


        sourcesContainer.appendChild(title);


        sources.forEach(source => {

            const item =
                document.createElement("div");

            item.className =
                "source-item";

            item.textContent =
                `📄 ${source.source} — Page ${source.page}`;

            sourcesContainer.appendChild(item);

        });


        message.appendChild(
            sourcesContainer
        );

    }


    chatMessages.appendChild(message);


    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


async function sendQuestion() {

    const question =
        questionInput.value.trim();


    if (!question) {
        return;
    }


    addMessage(
        question,
        "user"
    );


    questionInput.value = "";

    sendButton.disabled = true;

    sendButton.textContent =
        "Thinking...";


    try {

        const response =
            await fetch("/chat", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    question: question
                })

            });


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Something went wrong."
            );

        }


        addMessage(
            data.answer,
            "bot",
            data.sources
        );


    } catch (error) {

        addMessage(
            `Error: ${error.message}`,
            "bot"
        );

    } finally {

        sendButton.disabled = false;

        sendButton.textContent =
            "Send";

        questionInput.focus();

    }
}


sendButton.addEventListener(
    "click",
    sendQuestion
);


questionInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendQuestion();

        }

    }
);