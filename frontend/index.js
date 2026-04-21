const express = require("express")

const app = express()
const HOST = process.env.HOST || "0.0.0.0"
const PORT = Number(process.env.PORT) || 3000
const BACKEND_URL = process.env.BACKEND_URL || "http://127.0.0.1:8000"

app.set("view engine", "ejs")

app.use(express.static("public"))
app.use(express.urlencoded({ extended: true }))
app.use(express.json())

async function apiFetch(path, options = {}) {
    const response = await fetch(`${BACKEND_URL}${path}`, options)

    if (!response.ok) {
        let message = `Request failed with status ${response.status}`

        try {
            const errorPayload = await response.json()
            if (errorPayload.detail) {
                message = errorPayload.detail
            }
        } catch {
            // Ignore non-JSON error bodies and use the fallback message.
        }

        throw new Error(message)
    }

    return response.json()
}

function normalizeItems(itemsObject = {}) {
    return Object.entries(itemsObject).map(([id, item]) => ({
        id,
        ...item
    }))
}

app.get("/", (req, res) => {
    res.redirect("/items")
})

app.get("/items", async (req, res) => {
    try {
        const data = await apiFetch("/items")
        res.render("home", {
            items: normalizeItems(data.items),
            errorMessage: null
        })
    } catch (error) {
        res.status(500).render("home", {
            items: [],
            errorMessage: error.message
        })
    }
})

app.post("/items", async (req, res) => {
    try {
        await apiFetch("/items", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: req.body.name,
                description: req.body.description
            })
        })

        res.redirect("/items")
    } catch (error) {
        const data = await apiFetch("/items").catch(() => ({ items: {} }))
        res.status(400).render("home", {
            items: normalizeItems(data.items),
            errorMessage: error.message
        })
    }
})

app.get("/items/edit/:id", async (req, res) => {
    try {
        const data = await apiFetch(`/items/${req.params.id}`)
        res.render("edit-item", {
            item: {
                id: req.params.id,
                ...data.item
            },
            errorMessage: null
        })
    } catch (error) {
        res.status(404).redirect("/items")
    }
})

app.post("/items/edit/:id", async (req, res) => {
    try {
        await apiFetch(`/items/${req.params.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: req.body.name,
                description: req.body.description
            })
        })

        res.redirect("/items")
    } catch (error) {
        res.status(400).render("edit-item", {
            item: {
                id: req.params.id,
                name: req.body.name,
                description: req.body.description
            },
            errorMessage: error.message
        })
    }
})

app.get("/items/delete/:id", async (req, res) => {
    try {
        await apiFetch(`/items/${req.params.id}`, {
            method: "DELETE"
        })
    } finally {
        res.redirect("/items")
    }
})

app.listen(PORT, HOST, () => {
    console.log(`Express is now listening on port ${PORT}.`)
    console.log(`Frontend: http://${HOST}:${PORT}`)
    console.log(`Backend target: ${BACKEND_URL}`)
})
