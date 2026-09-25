async function loadDocuments() {
    const container =
        document.getElementById("documentsList");

    try {
        // Lo slash finale evita il redirect 307 di FastAPI
        const response =
            await fetch("/documents/");

        if (!response.ok) {
            throw new Error(
                "Errore nel caricamento dei documenti"
            );
        }

        const documents =
            await response.json();

        // -------------------------
        // Contatore documenti
        // -------------------------

        const documentCount =
            document.getElementById(
                "documentCount"
            );

        if (documentCount) {
            const count = documents.length;

            documentCount.textContent =
                count === 1
                    ? "1 documento"
                    : `${count} documenti`;
        }

        console.log(
            "Documenti ricevuti:",
            documents
        );

        container.innerHTML = "";

        if (documents.length === 0) {
            container.textContent =
                "Nessun documento presente.";
            return;
        }

        documents.forEach(doc => {

            const item =
                document.createElement("div");

            item.className =
                "document-item";

            item.setAttribute(
                "data-document-id",
                doc.document_id
            );


            // -------------------------
            // Informazioni documento
            // -------------------------

            const info =
                document.createElement("div");

            info.className =
                "document-info";


            const name =
                document.createElement("strong");

            name.textContent =
                doc.original_filename;


            const size =
                document.createElement("span");

            size.textContent =
                (doc.size_bytes / 1024).toFixed(1)
                + " KB";


            const date =
                document.createElement("span");

            if (doc.created_at) {

                const documentDate =
                    new Date(doc.created_at);

                date.textContent =
                    documentDate.toLocaleDateString(
                        "it-IT",
                        {
                            day: "2-digit",
                            month: "2-digit",
                            year: "numeric"
                        }
                    );

            } else {

                date.textContent =
                    "Data non disponibile";
            }


            info.appendChild(name);
            info.appendChild(size);
            info.appendChild(date);


            // -------------------------
            // Azioni
            // -------------------------

            const actions =
                document.createElement("div");

            actions.className =
                "document-actions";


            // -------------------------
            // Pulsante Testo
            // -------------------------

            const textButton =
                document.createElement("button");

            textButton.textContent =
                "Testo";

            textButton.addEventListener(
                "click",
                () => {
                    showDocumentText(
                        doc.document_id
                    );
                }
            );

            actions.appendChild(
                textButton
            );


            // -------------------------
            // Pulsante Summary
            // -------------------------

            const summaryButton =
                document.createElement("button");

            summaryButton.textContent =
                "Summary";

            summaryButton.addEventListener(
                "click",
                () => {
                    showDocumentSummary(
                        doc.document_id
                    );
                }
            );

            actions.appendChild(
                summaryButton
            );


            // -------------------------
            // Pulsante Ask
            // -------------------------

            const askButton =
                document.createElement("button");

            askButton.textContent =
                "Ask";

            askButton.addEventListener(
                "click",
                () => {
                    showAskBox(
                        doc.document_id
                    );
                }
            );

            actions.appendChild(
                askButton
            );


            // -------------------------
            // Pulsante Download
            // -------------------------

            const downloadButton =
                document.createElement("button");

            downloadButton.textContent =
                "Download";

            downloadButton.addEventListener(
                "click",
                () => {
                    downloadDocument(
                        doc.document_id
                    );
                }
            );

            actions.appendChild(
                downloadButton
            );


            // -------------------------
            // Pulsante Delete
            // -------------------------

            const deleteButton =
                document.createElement("button");

            deleteButton.textContent =
                "Delete";

            deleteButton.addEventListener(
                "click",
                () => {
                    deleteDocument(
                        doc.document_id,
                        doc.original_filename
                    );
                }
            );

            actions.appendChild(
                deleteButton
            );


            // -------------------------
            // Composizione documento
            // -------------------------

            item.appendChild(info);
            item.appendChild(actions);

            container.appendChild(item);
        });

    } catch (error) {

        console.error(
            "Errore:",
            error
        );

        container.textContent =
            "Impossibile caricare i documenti.";
    }
}


async function uploadDocument() {

    const fileInput =
        document.getElementById("fileInput");

    const uploadStatus =
        document.getElementById(
            "uploadStatus"
        );

    const uploadButton =
        document.getElementById(
            "uploadButton"
        );


    if (fileInput.files.length === 0) {

        alert(
            "Seleziona prima un PDF."
        );

        return;
    }


    const file =
        fileInput.files[0];


    // Controllo lato UI
    if (file.type !== "application/pdf") {

        uploadStatus.textContent =
            "✕ Seleziona un file PDF.";

        return;
    }


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    uploadStatus.textContent =
        "Caricamento in corso...";

    uploadButton.disabled = true;


    try {

        const response =
            await fetch(
                "/documents/upload",
                {
                    method: "POST",
                    body: formData
                }
            );


        if (!response.ok) {

            throw new Error(
                "Errore durante il caricamento del documento"
            );
        }


        const documentData =
            await response.json();


        console.log(
            "Documento caricato:",
            documentData
        );


        uploadStatus.textContent =
            "✓ Documento caricato con successo.";


        // Aggiorniamo la lista
        await loadDocuments();


        // Puliamo il campo file
        fileInput.value = "";


    } catch (error) {

        console.error(
            "Errore:",
            error
        );


        uploadStatus.textContent =
            "✕ Errore durante il caricamento.";


        alert(
            "Impossibile caricare il documento."
        );


    } finally {

        uploadButton.disabled = false;
    }
}


async function deleteDocument(
    documentId,
    filename
) {

    const confirmed =
        confirm(
            `Sei sicuro di voler eliminare "${filename}"?`
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `/documents/${documentId}`,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {

            const errorData =
                await response.json();


            throw new Error(
                errorData.detail ||
                "Errore durante l'eliminazione"
            );
        }


        const result =
            await response.json();


        console.log(
            "Documento eliminato:",
            result
        );


        // Ricarichiamo la lista
        await loadDocuments();


    } catch (error) {

        console.error(
            "Errore:",
            error
        );


        alert(
            "Impossibile eliminare il documento."
        );
    }
}


function downloadDocument(documentId) {

    const url =
        `/documents/${documentId}/download`;

    // Lasciamo al browser la gestione
    // del download del file
    window.open(
        url,
        "_blank"
    );
}


async function showDocumentSummary(
    documentId
) {

    const documentItem =
        document.querySelector(
            `[data-document-id="${documentId}"]`
        );


    if (!documentItem) {

        console.error(
            "Elemento documento non trovato"
        );

        return;
    }


    // Se il summary è già aperto,
    // lo chiudiamo
    const existingSummary =
        document.querySelector(
            `[data-document-summary="${documentId}"]`
        );


    if (existingSummary) {

        existingSummary.remove();

        return;
    }


    try {

        const response =
            await fetch(
                `/documents/${documentId}/summary`
            );


        if (!response.ok) {

            throw new Error(
                "Errore nel caricamento del summary"
            );
        }


        const summaryData =
            await response.json();


        console.log(
            "Summary ricevuto:",
            summaryData
        );


        const summaryBox =
            document.createElement("div");


        summaryBox.className =
            "document-summary";


        summaryBox.setAttribute(
            "data-document-summary",
            documentId
        );


        summaryBox.textContent =
            summaryData.summary ||
            "Nessun summary disponibile.";


        documentItem.appendChild(
            summaryBox
        );


    } catch (error) {

        console.error(
            "Errore:",
            error
        );


        alert(
            "Impossibile caricare il summary del documento."
        );
    }
}


function showAskBox(documentId) {

    const documentItem =
        document.querySelector(
            `[data-document-id="${documentId}"]`
        );


    if (!documentItem) {

        console.error(
            "Elemento documento non trovato"
        );

        return;
    }


    // Se la casella esiste già,
    // la rimuoviamo
    const existingAskBox =
        document.querySelector(
            `[data-document-ask="${documentId}"]`
        );


    if (existingAskBox) {

        existingAskBox.remove();

        return;
    }


    const askBox =
        document.createElement("div");


    askBox.className =
        "document-ask";


    askBox.setAttribute(
        "data-document-ask",
        documentId
    );


    const questionInput =
        document.createElement("textarea");


    questionInput.placeholder =
        "Scrivi una domanda sul documento...";


    questionInput.rows = 4;


    const askButton =
        document.createElement("button");


    askButton.textContent =
        "Chiedi";


    askButton.addEventListener(
        "click",
        () => {

            askDocumentQuestion(
                documentId,
                questionInput.value,
                askBox
            );
        }
    );


    const answerBox =
        document.createElement("div");


    answerBox.className =
        "document-answer";


    askBox.appendChild(
        questionInput
    );

    askBox.appendChild(
        askButton
    );

    askBox.appendChild(
        answerBox
    );


    documentItem.appendChild(
        askBox
    );
}


async function askDocumentQuestion(
    documentId,
    question,
    askBox
) {

    const answerBox =
        askBox.querySelector(
            ".document-answer"
        );


    const askButton =
        askBox.querySelector(
            "button"
        );


    if (!question.trim()) {

        answerBox.textContent =
            "Scrivi prima una domanda.";

        return;
    }


    answerBox.textContent =
        "Sto elaborando la domanda...";


    askButton.disabled = true;


    try {

        const response =
            await fetch(
                `/documents/${documentId}/ask`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        if (!response.ok) {

            const errorData =
                await response.json();


            throw new Error(
                errorData.detail ||
                "Errore durante la richiesta"
            );
        }


        const answerData =
            await response.json();


        console.log(
            "Risposta Ask ricevuta:",
            answerData
        );


        answerBox.textContent =
            answerData.answer ||
            "Nessuna risposta disponibile.";


    } catch (error) {

        console.error(
            "Errore:",
            error
        );


        answerBox.textContent =
            "Errore: " +
            error.message;


    } finally {

        askButton.disabled = false;
    }
}


async function showDocumentText(
    documentId
) {

    const documentItem =
        document.querySelector(
            `[data-document-id="${documentId}"]`
        );


    if (!documentItem) {

        console.error(
            "Elemento documento non trovato"
        );

        return;
    }


    // Se il testo è già aperto,
    // lo chiudiamo
    const existingTextBox =
        document.querySelector(
            `[data-document-text="${documentId}"]`
        );


    if (existingTextBox) {

        existingTextBox.remove();

        return;
    }


    try {

        const response =
            await fetch(
                `/documents/${documentId}/text`
            );


        if (!response.ok) {

            throw new Error(
                "Errore nel caricamento del testo"
            );
        }


        const documentData =
            await response.json();


        console.log(
            "Testo ricevuto:",
            documentData
        );


        const textBox =
            document.createElement("div");


        textBox.className =
            "document-text";


        textBox.setAttribute(
            "data-document-text",
            documentId
        );


        textBox.textContent =
            documentData.text ||
            "Nessun testo disponibile.";


        documentItem.appendChild(
            textBox
        );


    } catch (error) {

        console.error(
            "Errore:",
            error
        );


        alert(
            "Impossibile caricare il testo del documento."
        );
    }
}


// -------------------------
// Eventi
// -------------------------

const uploadButton =
    document.getElementById(
        "uploadButton"
    );


uploadButton.addEventListener(
    "click",
    uploadDocument
);


// -------------------------
// Ricerca documenti
// -------------------------

const searchInput =
    document.getElementById(
        "searchInput"
    );


if (searchInput) {

    searchInput.addEventListener(
        "input",
        () => {

            const searchText =
                searchInput.value
                    .toLowerCase()
                    .trim();


            const documentItems =
                document.querySelectorAll(
                    ".document-item"
                );


            documentItems.forEach(
                item => {

                    const filename =
                        item.querySelector(
                            ".document-info strong"
                        );


                    if (!filename) {
                        return;
                    }


                    const filenameText =
                        filename.textContent
                            .toLowerCase();


                    if (
                        filenameText.includes(
                            searchText
                        )
                    ) {

                        item.style.display =
                            "";

                    } else {

                        item.style.display =
                            "none";
                    }
                }
            );
        }
    );
}


// -------------------------
// Caricamento iniziale
// -------------------------

loadDocuments();