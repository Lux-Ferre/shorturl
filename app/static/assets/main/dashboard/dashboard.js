class Dashboard {
    constructor(){
        this.get_links()
        this.create_listeners()
    }

    create_listeners(){
        document.getElementById("add_link_button").addEventListener("click", event => {
            event.preventDefault()

            const short_link = document.getElementById("short_link").value
            const full_link = document.getElementById("full_link").value

            window.dashboard.create_link(short_link, full_link)
        })
    }

    get_links(){
        axios.get("/api/get_links", {
            withCredentials: true
        })
        .then((response) => {
            window.dashboard.display_links(response.data.links);
        })
        .catch((error) => {
            console.log(error);
        })
    }

    display_links(links){
        const table = document.getElementById("url_table");
        const origin = window.location.origin

        for (const [short, full] of Object.entries(links)) {
            const row = table.insertRow();

            const short_cell = row.insertCell(0);
            const full_cell = row.insertCell(1);

            const short_url = `${origin}/l/${short}`

            let short_anchor = document.createElement("a")
            short_anchor.classList.add("short_link")
            short_anchor.href = short_url
            short_anchor.textContent = short_url
            short_anchor.target = "_blank"
            short_cell.appendChild(short_anchor)

            const full_url = `${full}`
            const full_anchor = document.createElement("a")
            full_anchor.href = full_url
            full_anchor.textContent = full_url
            full_anchor.target = "_blank"
            full_cell.appendChild(full_anchor)
        }
    }

    create_link(short_url, full_url){
        document.getElementById("add_link_button").disabled = true;
        document.getElementById("add_link_button").classList.add("disabled");
        axios.post("/api/add_link", {
            withCredentials: true,
            short_url: short_url,
            full_url: full_url
        })
            .then((response) => {
                if(response.status === 200){
                    window.location.reload();
                }
            })
            .catch((error) => {
                console.log(error.response.data);
            })
            .finally(() => {
                setTimeout(()=>{
                    document.getElementById("add_link_button").disabled = false;
                    document.getElementById("add_link_button").classList.remove("disabled");
                }, 2500)
            })
    }
}

window.dashboard = new Dashboard()
