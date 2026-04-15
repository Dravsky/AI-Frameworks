const express = require('express')

const app = express()
const PORT = 5000
const BACKEND_URL = "http://localhost:5050"

app.set("view engine", "ejs")

app.use(express.static("public"))

app.use(express.urlencoded({extended: true}))
app.use(express.json())

// <Sites>
app.get("/", (req, res) => {
    let url = `${BACKEND_URL}/featured-pokemon`
    fetch(url)
        .then(response => response.json())
        .then(featuredPokemon => {
            res.render("home", featuredPokemon)
        })
})

app.get("/pokepedia", (req, res) => {
    // If nothing is provided, set default values
    let name = req.query.name
    if (!name) { name = "ignore" }

    let include_official = req.query.include_official
    if (include_official === undefined) { include_official = "on" }

    let type1 = req.query.type1
    if (!type1) { type1 = "ignore" }    

    let type2 = req.query.type2
    if (!type2) { type2 = "ignore" }

    let listed = req.query.listed
    if (!listed) { listed = 151 }

    let url = `${BACKEND_URL}/pokepedia?name=${name}&include_official=${include_official}&type1=${type1}&type2=${type2}&listed=${listed}`
    fetch(url)
        .then(response => response.json())
        .then(data => {
            res.render("pokepedia", data)
        })
})

app.post("/pokepedia", (req, res) => {
    let name = req.body.name
    let include_official = req.body.include_official
    let type1 = req.body.type1
    let type2 = req.body.type2
    let listed = req.body.listed
    res.redirect(`/pokepedia?name=${name}&include_official=${include_official}&type1=${type1}&type2=${type2}&listed=${listed}`)
})

app.get("/create-pokemon", (req, res) => {
    res.render("create-pokemon")
})

app.post("/create-pokemon", (req, res) => {
    let url = `${BACKEND_URL}/create-pokemon`
    let headers = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(req.body)
    }

    fetch(url, headers)
        .then(resp => resp.json())
        .then(data => {
            res.redirect("/pokepedia")
        })
})

app.get("/pokepedia/delete/:id", (req, res) => {
    let idToDelete = req.params.id
    let url = `${BACKEND_URL}/pokepedia/delete/${idToDelete}`

    fetch(url)
        .then(resp => resp.json())
        .then(data => {
            res.redirect("/pokepedia")
        })
})

app.get("/pokepedia/edit-pokemon/:id", (req, res) => {
    let idToEdit = req.params.id
    let url = `${BACKEND_URL}/pokepedia/edit-pokemon/${idToEdit}`
    fetch(url)
        .then(response => response.json())
        .then(editPokemon => {
            res.render("edit-pokemon", editPokemon)
        })
})

app.post("/pokepedia/edit-pokemon/:id", (req, res) => {
    let idToEdit = req.params.id
    let url = `${BACKEND_URL}/pokepedia/edit-pokemon/${idToEdit}`
    let headers = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(req.body)
    }

    fetch(url, headers)
        .then(resp => resp.json())
        .then(data => {
            res.redirect("/pokepedia")
        })
})
// </Sites>

app.listen(PORT, () => {
    console.log(`Express is now listening on port ${PORT}.`)
    console.log(`http://localhost:${PORT}`)
})