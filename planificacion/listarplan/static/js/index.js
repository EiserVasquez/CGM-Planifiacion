// dirweb = "http://127.0.0.1:8000/";

let dataTable;
let dataTableIsInitialized = false;

const initDataTable = async () =>{
    if(dataTableIsInitialized){
        dataTable.destroy();
    }

    await lista_reservas();
    console.log($('dt-ordenes'));
    dataTable = $('dt-ordenes').DataTable();
    console.log(dataTable);
    // $('dt-ordenes').DataTable();
    dataTableIsInitialized = true;
}

const lista_reservas = async () => {
    try{
        const response = await fetch('http://127.0.0.1:8000/listarplan/lista_reservas/');
        const data = await response.json();
        console.log(data);

        let content = ``;
            data.reservas.forEach((dato,index) => {
                content += `
                            <tr>
                                <td>${dato.reserva}</td>
                                <td>${dato.reservapos}</td>
                                <td>${dato.orden}</td>
                                <td>${dato.material}</td>
                                <td>${dato.materialdeno}</td>
                                <td>${dato.ctd_nec}</td>
                                <td>${dato.ctd_dif}</td>
                                <td>${dato.ctd_reduc}</td>
                                <td>${dato.um_base}</td>                            
                            </tr>
                `;
            });
            treservas.innerHTML = content;

    }catch(ex){
        alert(ex);
    }
};


window.addEventListener('load', async () => {
    await initDataTable();
});
