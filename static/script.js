function handleKeyPress(event) {

    if (event.key === "Enter") {

        sendMessage();

    }

}



async function sendMessage() {

    const inputField =
        document.getElementById("user-input");

    const message =
        inputField.value.trim();

    if (message === "") return;



    const chatBox =
        document.getElementById("chat-box");



    /* USER MESSAGE */

    chatBox.innerHTML += `

        <div class="message user-message">

            ${message}

        </div>

    `;



    inputField.value = "";



    /* TYPING */

    const loadingId =
        "loading-" + Date.now();



    chatBox.innerHTML += `

        <div id="${loadingId}"
             class="message bot-message">

            <i>Typing...</i>

        </div>

    `;



    chatBox.scrollTop =
        chatBox.scrollHeight;



    try {

        const response = await fetch('/chat', {

            method: 'POST',

            headers: {

                'Content-Type': 'application/json'

            },

            body: JSON.stringify({

                message: message

            })

        });



        const data =
            await response.json();



        document
            .getElementById(loadingId)
            .remove();



        chatBox.innerHTML += `

            <div class="message bot-message">

                ${data.reply}

            </div>

        `;

    }

    catch (error) {

        document
            .getElementById(loadingId)
            .remove();



        chatBox.innerHTML += `

            <div class="message bot-message"
                 style="color:red;">

                Internet or Server Error!

            </div>

        `;

    }



    chatBox.scrollTop =
        chatBox.scrollHeight;

}



/* ========================= */
/* SIDEBAR */
/* ========================= */

function toggleMenu() {

    document
        .getElementById("sidebar")
        .classList
        .toggle("active");

}



/* ========================= */
/* ABOUT POPUP */
/* ========================= */

function showAbout() {

    document
        .getElementById("about-popup")
        .style
        .display = "flex";

}



function closeAbout() {

    document
        .getElementById("about-popup")
        .style
        .display = "none";

}



/* ========================= */
/* SHARE CHAT */
/* ========================= */

function shareChat() {

    navigator.share({

        title: "Manish AI Assistant",

        text: "Chat with my AI Assistant!",

        url: window.location.href

    });
    
    
    

}
function showMentor(){

    document
        .getElementById("mentor-popup")
        .style.display = "flex";

}

function closeMentor(){

    document
        .getElementById("mentor-popup")
        .style.display = "none";

}
