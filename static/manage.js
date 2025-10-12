let currentTable = "";
let tableData = [];    // full data from backend
let filteredData = []; // filtered by search
let currentPage = 1;
let pageSize = 10;

async function loadTable(preservePaging = false) {
    currentTable = document.getElementById('table').value;
    document.getElementById('tableData').innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(`/words?table=${currentTable}`);
        tableData = await response.json();
        filteredData = tableData.slice();

        if (!preservePaging) {
            currentPage = 1;
        }

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
        // first-time render: build table & header with search inputs
        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const trHead = document.createElement('tr');

        Object.keys(pageData[0] || {}).forEach(k => {
            const th = document.createElement('th');
            th.textContent = k;

            // search input
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

    // render only tbody
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

    // update page info
    const totalPages = Math.ceil(filteredData.length / pageSize) || 1;
    document.getElementById("pageInfo").textContent = `Page ${currentPage} / ${totalPages}`;
}

function filterTable(resetPage=true) {
    const filters = {};
    document.querySelectorAll('.filter').forEach(input => {
        const key = input.dataset.key;
        const val = input.value.trim().toLowerCase();
        if (val !== "") filters[key] = val;
    });

    filteredData = tableData.filter(row => {
        return Object.entries(filters).every(([key, val]) =>
            (row[key] ?? "").toString().toLowerCase().includes(val)
        );
    });
    if (resetPage) {
        currentPage = 1;
    }
    renderTablePage();
}

function changePageSize(size) {
    pageSize = parseInt(size);
    currentPage = 1;
    renderTablePage();
}

function prevPage() {
    if(currentPage > 1) {
        currentPage--;
        renderTablePage();
    }
}

function nextPage() {
    if(currentPage < Math.ceil(filteredData.length / pageSize)) {
        currentPage++;
        renderTablePage();
    }
}

function addRow() {
    const table = document.querySelector("#tableData table tbody");
    if (!table) return alert("Please select a table first.");

    const headers = Array.from(document.querySelectorAll("#tableData thead th"))
        .map(th => th.innerText)
        .filter(h => h && h !== "Actions");

    const newRow = document.createElement("tr");
    headers.forEach(h => {
        newRow.innerHTML += `<td contenteditable="true" data-key="${h.trim()}"></td>`;
    });
    newRow.innerHTML += `<td class="actions">
                            <button onclick='saveRow(this)'>💾 Save</button>
                            <button onclick='deleteRow(this)'>🗑️ Delete</button>
                         </td>`;

    // Append row to both tableData and filteredData
    const placeholder = {};
    headers.forEach(h => placeholder[h.trim()] = null);
    tableData.push(placeholder);
    filteredData.push(placeholder);

    // Append to DOM at the end of current page
    table.appendChild(newRow);

    // Add "edited" highlight
    newRow.classList.add('edited');
}

async function saveRow(btn) {
    const row = btn.closest('tr');
    const cells = row.querySelectorAll('td[data-key]');
    const data = {};

    // collect data
    cells.forEach(cell => {
        const key = cell.dataset.key;
        const value = cell.innerText.trim();
        data[key] = value || null; // treat empty string as null
    });

    const key = Object.keys(data).includes('word') ? 'word'
              : Object.keys(data).includes('number') ? 'number'
              : 'id';

    if (!data.id) delete data.id;

    const body = { table: currentTable, key, data };

    try {
        const res = await fetch('/word', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        });

        const json = await res.json();
        if (!res.ok) throw new Error(JSON.stringify(json));

        // Updated entry from db
        const json_response_data = json.data;

        // Update tableData in place
        if (json_response_data.id) {
            // Try to find existing row by id
            let index = tableData.findIndex(r => r.id === json_response_data.id);

            if (index >= 0) {
                // Update existing row
                tableData[index] = { ...tableData[index], ...json_response_data };
            } else {
                // No row with this id yet: find placeholder row (id is null/undefined)
                index = tableData.findIndex(r => !r.id);
                if (index >= 0) {
                    tableData[index] = { ...tableData[index], ...json_response_data };
                } else {
                    // If no placeholder exists, append at the end
                    tableData.push(json_response_data);
                }
            }
        }

        // Update row style
        row.classList.remove('edited');

        // Update only current page without overwriting other edits
        filterTable(false);

    } catch(err) {
        alert(err);
    }
}

async function deleteRow(btn) {
    const row = btn.closest('tr');
    const cells = row.querySelectorAll('td[data-key]');
    const data = {};

    cells.forEach(cell => {
        const key = cell.dataset.key;
        const value = cell.innerText.trim();
        if (value !== "") data[key] = value;
    });

    const key = Object.keys(data).includes('word') ? 'word'
              : Object.keys(data).includes('number') ? 'number'
              : 'id';

    const body = { table: currentTable, key, action: 'delete', data };

    try {
        const res = await fetch('/word', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        });

        const json = await res.json();
        if (!res.ok) throw new Error(JSON.stringify(json));

        // Remove the row from tableData and filteredData
        const idKey = 'id';
        const idVal = data[idKey] ?? null;

        if (idVal) {
            const index = tableData.findIndex(r => String(r[idKey]) === String(idVal));
            if (index >= 0) tableData.splice(index, 1);

        } else {
            // fallback: remove by matching the row DOM index in current page
            const tbody = row.parentElement;
            const pageStart = (currentPage - 1) * pageSize;
            const rowIndex = Array.from(tbody.children).indexOf(row);
            const globalIndex = pageStart + rowIndex;
            if (globalIndex >= 0 && globalIndex < filteredData.length) {
                tableData.splice(globalIndex, 1);
            }
        }

        // Update page info without resetting current page
        const totalPages = Math.ceil(filteredData.length / pageSize) || 1;
        if (currentPage > totalPages) currentPage = totalPages;
        filterTable(false);

    } catch(err) {
        alert(err);
    }
}


async function rerender() {
    const res = await fetch('/render', { method: 'POST' });
    alert_notification(res);
}

async function alert_notification(response) {
    const data = await response.json();

    if (!response.ok) {
        // Only show alert for error responses
        alert(JSON.stringify(data, null, 2));
    } else {
        console.log('✅ Success:', data);
    }
}

document.querySelector("#tableData").addEventListener('input', function(e) {
    const td = e.target.closest('td');
    if (!td) return;
    const tr = td.closest('tr');
    if (!tr.classList.contains('edited')) {
        tr.classList.add('edited');
    }
});

// auto-load
window.onload = loadTable;