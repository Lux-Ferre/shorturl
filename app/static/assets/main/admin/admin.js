class Admin {
    constructor(){
        this.get_pending()
        this.create_listeners()
    }

    create_listeners(){
        document.getElementById("user_table").addEventListener("click", event => {
            event.preventDefault()

            const clicked_element = event.target
            if(clicked_element.nodeName === "SPAN"){
                if(clicked_element.disabled){return}
                clicked_element.parentElement.querySelectorAll("span").forEach(span_element => {
                    span_element.disabled = true;
                    span_element.classList.add("disabled");
                })

                const id = clicked_element.parentElement.parentElement.dataset.userId
                if(clicked_element.classList.contains("approve_user")){
                    window.admin.approve_user(id)
                } else if (clicked_element.classList.contains("delete_user")){
                    window.admin.delete_user(id)
                }
            }
        })
    }

    get_pending(){
        axios.get("/api/get_pending", {
            withCredentials: true
        })
        .then((response) => {
            window.admin.display_pending_users(response.data.unconfirmed_users);
        })
        .catch((error) => {
            console.log(error);
        })
    }

    approve_user(user_id){
        axios.post("/api/approve_user", {
            withCredentials: true,
            user_id: user_id
        })
        .then((response) => {
            document.getElementById("user_table").innerHTML = "";
            window.admin.get_pending()
        })
        .catch((error) => {
            console.log(error.response.data.error_message);
            document.getElementById("user_table").innerHTML = "";
            window.admin.get_pending()
        })
    }

    delete_user(user_id){
        axios.post("/api/delete_user", {
            withCredentials: true,
            user_id: user_id
        })
        .then((response) => {
            document.getElementById("user_table").innerHTML = "";
            window.admin.get_pending()
        })
        .catch((error) => {
            console.log(error.response.data.error_message);
            document.getElementById("user_table").innerHTML = "";
            window.admin.get_pending()
        })
    }

    display_pending_users(users){
        for (const [id, email] of Object.entries(users)) {
            let clone = document.getElementById("user_template").content.cloneNode(true);

            clone.querySelector(".table_row").dataset.userId = id;
            clone.querySelector(".user_email").textContent = email;

            document.getElementById("user_table").appendChild(clone);
        }
    }
}

window.admin = new Admin();