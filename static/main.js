


// function table_interface(data){
//   let rows = ""
//   data.forEach(interface => {
//     rows += `
//     <tr>
//     <td>${interface.Hostname}</td>
//     <td>${interface.InterfaceName}</td>
//     <td>${interface.Description}</td>
//     <td>${interface.IP}</td>
//     <td>${interface.MAC}</td>
//     <td>${interface.InterfaceState}</td>
//     <td>${interface.ProtocolState}</td>
//     </tr>
//     `
//   });

//   return `
//   <table id="interfaces_table">
//     <thead>
//         <tr>
//             <th>Hostname</th>
//             <th>InterfaceName</th>
//             <th>Description</th>
//             <th>IP</th>
//             <th>MAC</th>
//             <th>InterfaceState</th>
//             <th>ProtocolState</th>
//         </tr>
//     </thead>
//     <tbody>
//         ${rows}
//     </tbody>
// </table>
//   `
// }

// fetch(`http://127.0.0.1:5000/search`)
//   .then(res => res.json())
//   .then(data => {
//   console.log(data)
//   document.getElementById("my-table").innerHTML = table_interface(data)

//   let table = document.getElementById('interfaces_table');
//   let myTable = new JSTable(table, {
//     sortable: true,
//     searchable: true,
//   });
// })

let table = document.getElementById('interfaces_table');
let myTable = new JSTable(table);