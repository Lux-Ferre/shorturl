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
        for (const [short, full] of Object.entries(links)) {
            const row = table.insertRow();

            const short_cell = row.insertCell(0);
            const full_cell = row.insertCell(1);

            short_cell.textContent = short;

            const anchor = document.createElement("a");
            anchor.href = full;
            anchor.textContent = full;
            anchor.target = "_blank"; // optional: open link in new tab
            full_cell.appendChild(anchor);
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
