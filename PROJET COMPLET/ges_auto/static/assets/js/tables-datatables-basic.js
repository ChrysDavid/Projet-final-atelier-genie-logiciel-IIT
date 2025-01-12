// script.js
document.addEventListener('DOMContentLoaded', function () {
  // Sample data
  const data = [
      { id: 1, name: "John Doe", email: "john@example.com", date: "2024-01-01", salary: 50000, status: "active" },
      { id: 2, name: "Jane Smith", email: "jane@example.com", date: "2024-01-02", salary: 60000, status: "inactive" },
      { id: 3, name: "Bob Wilson", email: "bob@example.com", date: "2024-01-03", salary: 55000, status: "pending" }
  ];

  let currentPage = 1;
  let entriesPerPage = 10;
  let filteredData = [...data];

  // DOM Elements
  const tableBody = document.getElementById('tableBody');
  const searchInput = document.getElementById('searchInput');
  const entriesSelect = document.getElementById('entriesSelect');
  const addNewBtn = document.getElementById('addNewBtn');
  const modal = document.getElementById('recordModal');
  const recordForm = document.getElementById('recordForm');
  const closeBtn = document.querySelector('.close-btn');
  const cancelBtn = document.getElementById('cancelBtn');

  // Render table data
  function renderTable() {
      const start = (currentPage - 1) * entriesPerPage;
      const end = start + entriesPerPage;
      const paginatedData = filteredData.slice(start, end);

      tableBody.innerHTML = '';
      paginatedData.forEach(item => {
          const row = document.createElement('tr');
          row.innerHTML = `
          <td>${item.name}</td>
          <td>${item.email}</td>
          <td>${formatDate(item.date)}</td>
          <td>$${item.salary.toLocaleString()}</td>
          <td><span class="status-badge status-${item.status}">${item.status}</span></td>
          <td>
              <button class="btn btn-edit" data-id="${item.id}">Edit</button>
              <button class="btn btn-delete" data-id="${item.id}">Delete</button>
          </td>
      `;
          tableBody.appendChild(row);
      });

      updatePagination();
      updateEntriesInfo();
  }

  // Update pagination
  function updatePagination() {
      const totalPages = Math.ceil(filteredData.length / entriesPerPage);
      const pageNumbers = document.getElementById('pageNumbers');
      pageNumbers.innerHTML = '';

      for (let i = 1; i <= totalPages; i++) {
          const button = document.createElement('button');
          button.classList.add('btn-page');
          if (i === currentPage) button.classList.add('active');
          button.textContent = i;
          button.addEventListener('click', () => {
              currentPage = i;
              renderTable();
          });
          pageNumbers.appendChild(button);
      }
  }

  // Update entries info
  function updateEntriesInfo() {
      const start = (currentPage - 1) * entriesPerPage + 1;
      const end = Math.min(start + entriesPerPage - 1, filteredData.length);
      document.getElementById('startEntry').textContent = start;
      document.getElementById('endEntry').textContent = end;
      document.getElementById('totalEntries').textContent = filteredData.length;
  }

  // Event Listeners
  searchInput.addEventListener('input', function (e) {
      const searchTerm = e.target.value.toLowerCase();
      filteredData = data.filter(item =>
          item.name.toLowerCase().includes(searchTerm) ||
          item.email.toLowerCase().includes(searchTerm)
      );
      currentPage = 1;
      renderTable();
  });

  entriesSelect.addEventListener('change', function (e) {
      entriesPerPage = parseInt(e.target.value);
      currentPage = 1;
      renderTable();
  });

  addNewBtn.addEventListener('click', () => {
      modal.style.display = 'block';
  });

  closeBtn.addEventListener('click', () => {
      modal.style.display = 'none';
  });

  cancelBtn.addEventListener('click', () => {
      modal.style.display = 'none';
  });

  recordForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const newRecord = {
          id: data.length + 1,
          name: document.getElementById('name').value,
          email: document.getElementById('email').value,
          date: document.getElementById('date').value,
          salary: parseInt(document.getElementById('salary').value),
          status: document.getElementById('status').value
      };
      data.push(newRecord);
      filteredData = [...data];
      modal.style.display = 'none';
      recordForm.reset();
      renderTable();
  });

  // Delete record
  tableBody.addEventListener('click', function (e) {
      if (e.target.classList.contains('btn-delete')) {
          const id = parseInt(e.target.dataset.id);
          const index = data.findIndex(item => item.id === id);
          if (index !== -1) {
              if (confirm('Are you sure you want to delete this record?')) {
                  data.splice(index, 1);
                  filteredData = [...data];
                  renderTable();
              }
          }
      }
  });

  // Edit record
  tableBody.addEventListener('click', function (e) {
      if (e.target.classList.contains('btn-edit')) {
          const id = parseInt(e.target.dataset.id);
          const record = data.find(item => item.id === id);
          if (record) {
              // Populate form
              document.getElementById('name').value = record.name;
              document.getElementById('email').value = record.email;
              document.getElementById('date').value = record.date;
              document.getElementById('salary').value = record.salary;
              document.getElementById('status').value = record.status;

              // Change form mode to edit
              recordForm.dataset.mode = 'edit';
              recordForm.dataset.editId = id;

              // Show modal
              modal.style.display = 'block';
          }
      }
  });

  // Export functionality
  document.getElementById('exportBtn').addEventListener('click', function (e) {
      const target = e.target.closest('li');
      if (!target) return;

      const type = target.dataset.type;
      switch (type) {
          case 'csv':
              exportToCSV();
              break;
          case 'excel':
              exportToExcel();
              break;
          case 'pdf':
              exportToPDF();
              break;
          case 'print':
              printTable();
              break;
      }
  });

  // Export utilities
  function exportToCSV() {
      let csv = 'Name,Email,Date,Salary,Status\n';
      filteredData.forEach(item => {
          csv += `${item.name},${item.email},${item.date},${item.salary},${item.status}\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'table-export.csv';
      a.click();
      window.URL.revokeObjectURL(url);
  }

  function exportToExcel() {
      let table = '<table>';
      // Add header
      table += '<tr><th>Name</th><th>Email</th><th>Date</th><th>Salary</th><th>Status</th></tr>';

      // Add data
      filteredData.forEach(item => {
          table += `<tr>
          <td>${item.name}</td>
          <td>${item.email}</td>
          <td>${item.date}</td>
          <td>${item.salary}</td>
          <td>${item.status}</td>
      </tr>`;
      });
      table += '</table>';

      const blob = new Blob([table], { type: 'application/vnd.ms-excel' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'table-export.xls';
      a.click();
      window.URL.revokeObjectURL(url);
  }

  function exportToPDF() {
      // Note: In a real application, you'd want to use a proper PDF library
      alert('PDF export would require a PDF generation library');
  }

  function printTable() {
      const printWindow = window.open('', '_blank');
      printWindow.document.write(`
      <html>
          <head>
              <title>Print Table</title>
              <style>
                  table { border-collapse: collapse; width: 100%; }
                  th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                  th { background-color: #f5f5f5; }
              </style>
          </head>
          <body>
              <h2>Table Export</h2>
              <table>
                  <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Date</th>
                      <th>Salary</th>
                      <th>Status</th>
                  </tr>
                  ${filteredData.map(item => `
                      <tr>
                          <td>${item.name}</td>
                          <td>${item.email}</td>
                          <td>${formatDate(item.date)}</td>
                          <td>$${item.salary.toLocaleString()}</td>
                          <td>${item.status}</td>
                      </tr>
                  `).join('')}
              </table>
          </body>
      </html>
  `);
      printWindow.document.close();
      printWindow.focus();
      printWindow.print();
      printWindow.close();
  }

  // Utility functions
  function formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: 'numeric'
      });
  }

  // Previous page button
  document.getElementById('prevPage').addEventListener('click', () => {
      if (currentPage > 1) {
          currentPage--;
          renderTable();
      }
  });

  // Next page button
  document.getElementById('nextPage').addEventListener('click', () => {
      const totalPages = Math.ceil(filteredData.length / entriesPerPage);
      if (currentPage < totalPages) {
          currentPage++;
          renderTable();
      }
  });

  // Close modal when clicking outside
  window.addEventListener('click', (e) => {
      if (e.target === modal) {
          modal.style.display = 'none';
      }
  });

  // Initialize table
  renderTable();
});
