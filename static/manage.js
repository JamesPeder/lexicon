let currentTable = "";
let tableData = [];    // full data from backend
let filteredData = []; // filtered by search
let currentPage = 1;
let pageSize = 10;

async function loadTable() {
    currentTable = document.getElementById('table').value;
    document.getElementById('tableData').innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(`/words?table=${currentTable}`);
        tableData = await response.json();
        filteredData = tableData.slice();
        currentPage = 1;
        renderTablePage();
    } catch (err) {
        document.getElementById('tableData').innerHTML = `<p style="color:red;">Error: ${err}</p>`;
    }
}

function renderTablePage() {
    const tbodyStart = (currentPage - 1) * pageSize;
    const tbodyEnd = tbodyStart + pageSize;
    const pageData = filteredData.slice(tbodyStart, tbodyEnd);

    const container = document.getElementById('tableData');

    if (!container.querySelector('table')) {
        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const trHead = document.createElement('tr');

        Object.keys(pageData[0] || {}).forEach(k => {
            const th = document.createElement('th');
            th.textContent = k;

            const input = document.createElement('input');
            input.className = 'filter';
            input.dataset.key = k;
            input.addEventListener('input', filterTable);
            th.appendChild(document.createElement('br'));
            th.appendChild(input);

            trHead.appendChild(th);
        });

        const thActions = document.createElement('th');
        thActions.textContent = "Actions";
        trHead.appendChild(thActions);

        thead.appendChild(trHead);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        table.appendChild(tbody);

        container.innerHTML = "";
        container.appendChild(table);
    }

    const tbody = container.querySelector('tbody');
    tbody.innerHTML = "";

    pageData.forEach(row => {
        const tr = document.createElement('tr');
        Object.keys(row).forEach(k => {
            const td = document.createElement('td');
            td.setAttribute('data-key', k);
            td.setAttribute('contenteditable', 'true');
            td.textContent = row[k] ?? '';
            tr.appendChild(td);
        });

        const tdActions = document.createElement('td');
        tdActions.className = 'actions';
        tdActions.innerHTML = `<button onclick='saveRow(this)'>💾 Save</button>
                               <button onclick='deleteRow(this)'>🗑️ Delete</button>`;
        tr.appendChild(tdActions);

        tbody.appendChild(tr);
    });

    const totalPages = Math.ceil(filteredData.length / pageSize) || 1;
    document.getElementById("pageInfo").textContent = `Page ${currentPage} / ${totalPages}`;
}

// Paging
function changePageSize(size) { pageSize = parseInt(size); currentPage = 1; renderTablePage(); }
function prevPage() { if(currentPage>1){ currentPage--; renderTablePage(); } }
function nextPage() { if(currentPage<Math.ceil(filteredData.length/pageSize)){ currentPage++; renderTablePage(); } }

// Filtering
function filterTable() {
    const filters = {};
    document.querySelectorAll('.filter').forEach(input => {
        const key = input.dataset.key;
        const val = input.value.trim().toLowerCase();
        if (val !== "") filters[key] = val;
    });

    filteredData = tableData.filter(row => {
        return Object.entries(filters).every(([key,val]) => (row[key]??"").toString().toLowerCase().includes(val));
    });

    currentPage = 1;
    renderTablePage();
}

// Add row
function addRow() {
    const table = document.querySelector("#tableData table tbody");
    if (!table) return alert("Please select a table first.");
    const headers = Array.from(document.querySelectorAll("#tableData thead th")).map(th=>th.innerText).filter(h=>h!=="Actions");

    const newRow = document.createElement("tr");
    headers.forEach(h => { newRow.innerHTML += `<td contenteditable="true" data-key="${h}"></td>`; });
    newRow.innerHTML += `<td class="actions"><button onclick='saveRow(this)'>💾 Save</button><button onclick='deleteRow(this)'>🗑️ Delete</button></td>`;

    const insertIndex = (currentPage-1)*pageSize + table.rows.length;
    filteredData.splice(insertIndex,0,{});
    tableData.push({});
    table.appendChild(newRow);
}

// Save / Delete / Re-render
async function saveRow(btn){ /* same logic as before */ }
async function deleteRow(btn){ /* same logic as before */ }
async function rerender(){ /* same logic as before */ }

// auto-load
window.onload = loadTable;
