(
    function () {
        var saved = localStorage.getItem("ne-atlas-bg");
        if (saved) 
            document.body.style.setProperty("--page-bg", saved);
        document.querySelectorAll(".bg-picker").forEach(
            function (input) {
                if (saved) 
                    input.value = saved;
                input.addEventListener("input", function () {
                    document.body.style.setProperty("--page-bg", input.value);
                    localStorage.setItem("ne-atlas-bg", input.value);
                });
            }
        );
    }
)();