// function confirmar() {
//     return confirm('¿Estás seguro de eliminar esta unidad?');
// }

// document.addEventListener("DOMContentLoaded", function() {
//     var button_delete = document.querySelector(".btn-danger");
    
//     button_delete.addEventListener("click", function(event) {
//         event.preventDefault();
//         var confirmacion = confirm('¿Estás seguro de eliminar este elemento?');
        
//         if (confirmacion) {
//             // Si el usuario confirma, se envía el formulario
//             var form = button_delete.closest("form");
//             form.submit();
         
//         }
//     });
  
// });

// window.onload = function(){
//     var button;    
//     button = document.querySelector("button.btn-primary");
//     button.addEventListener("click", searchUnit);
    
// }

document.addEventListener("DOMContentLoaded", function() {
    var button_buscar = document.querySelector(".buscar");
    var button_delete = document.querySelector(".btn-danger");
    
    if (button_buscar) {
            button_buscar.addEventListener("click", function(event) {
                event.preventDefault();
                var input = document.getElementById("searchInput").value.toLowerCase();
                var rows = document.querySelectorAll(".table.table-striped tbody tr");
                var found = false;
                rows.forEach(function(row) {
                    var name = row.querySelector("td:nth-child(2)").textContent.toLowerCase();
                    if (name.includes(input)) {
                        row.style.display = "table-row";
                        found = true;
                    } else {
                        row.style.display = "none";
                    }
                });

                if (!found) {
                    alert("No se encontró el elemento solicitado.");
                }
            }
            )
        }
        if (button_delete) {
            button_delete.addEventListener("click", function(event) {
                event.preventDefault();
                var confirmacion = confirm('¿Estás seguro de eliminar este elemento?');
                
                if (confirmacion) {
                    // Si el usuario confirma, se envía el formulario
                    var form = button_delete.closest("form");
                    form.submit();
                 
                }
            });
        }

});

// function searchUnit() {
//     var confirmacion = confirm('¿Estás seguro de eliminar este elemento?');
//     var input = document.getElementById("searchInput").value.toLowerCase();
//     var rows = document.querySelectorAll(".table.table-striped tbody tr");
//     console.log("mensaje")
//     var found = false;
//     rows.forEach(function(row) {
//         var name = row.querySelector("td:nth-child(2)").textContent.toLowerCase();
//         if (name.includes(input)) {
//             row.style.display = "table-row";
//             found = true;
//         } else {
//             row.style.display = "none";
//         }
//     });

//     if (!found) {
//         alert("No se encontró la unidad con el nombre solicitado.");
//     }
// }



