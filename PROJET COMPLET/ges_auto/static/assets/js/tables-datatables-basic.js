document.addEventListener('DOMContentLoaded', function() {
    // Éléments DOM
    const userModal = new bootstrap.Modal(document.getElementById('userModal'));
    const userForm = document.getElementById('userForm');
    const searchInput = document.getElementById('searchInput');
    const entriesSelect = document.getElementById('entriesSelect');
    const table = document.querySelector('.table');
    const tableBody = table.querySelector('tbody');

    // État global
    let currentUserId = null;
    let users = [];

    // Fonction pour charger les données initiales
    function loadInitialData() {
        const rows = tableBody.querySelectorAll('tr');
        users = Array.from(rows).map(row => ({
            id: row.querySelector('.edit-btn')?.dataset.id,
            matricule: row.cells[0].textContent,
            nom: row.cells[1].textContent,
            prenom: row.cells[2].textContent,
            email: row.cells[3].textContent,
            fonction: row.cells[4].textContent,
            adresse: row.cells[5].textContent,
            date_embauche: row.cells[6].textContent,
            dernier_connexion: row.cells[7].textContent
        }));
    }

    // Fonction de recherche
    function handleSearch(searchTerm) {
        const filteredUsers = users.filter(user => 
            Object.values(user).some(value => 
                value && value.toString().toLowerCase().includes(searchTerm.toLowerCase())
            )
        );
        renderUsers(filteredUsers);
    }

    // Fonction de tri
    function handleSort(column, direction) {
        const sortedUsers = [...users].sort((a, b) => {
            if (direction === 'asc') {
                return a[column] > b[column] ? 1 : -1;
            }
            return a[column] < b[column] ? 1 : -1;
        });
        renderUsers(sortedUsers);
    }

    // Fonction pour afficher les utilisateurs
    function renderUsers(usersToRender) {
        tableBody.innerHTML = usersToRender.map(user => `
            <tr>
                <td>${user.matricule}</td>
                <td>${user.nom}</td>
                <td>${user.prenom}</td>
                <td>${user.email}</td>
                <td>${user.fonction || '-'}</td>
                <td>${user.adresse || '-'}</td>
                <td>${user.date_embauche || '-'}</td>
                <td>${user.dernier_connexion || '-'}</td>
                <td>
                    <div class="d-flex gap-2">
                        <button class="btn btn-sm btn-info edit-btn" data-id="${user.id}">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-danger delete-btn" data-id="${user.id}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="9" class="text-center">Aucun utilisateur trouvé.</td></tr>';
        
        // Réattacher les événements après le rendu
        attachEventListeners();
    }

    // Gestion de l'ajout/modification d'utilisateur
    async function handleUserSubmit(e) {
        e.preventDefault();
        const formData = new FormData(userForm);
        const url = currentUserId 
            ? `/utilisateurs/update/${currentUserId}/`
            : '/utilisateurs/create/';

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify(Object.fromEntries(formData)),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            if (response.ok) {
                const result = await response.json();
                userModal.hide();
                window.location.reload();
            } else {
                const error = await response.json();
                alert(error.message);
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Une erreur est survenue');
        }
    }

    // Gestion de la suppression
    async function handleDelete(userId) {
        if (!confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) return;

        try {
            const response = await fetch(`/utilisateurs/delete/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            if (response.ok) {
                window.location.reload();
            } else {
                const error = await response.json();
                alert(error.message);
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Une erreur est survenue');
        }
    }

    // Gestion de l'export
    function handleExport(format) {
        if (['csv', 'excel', 'pdf'].includes(format)) {
            window.location.href = `/utilisateurs/export/${format}/`;
        } else if (format === 'print') {
            window.print();
        }
    }

    // Attacher les écouteurs d'événements
    function attachEventListeners() {
        // Boutons d'édition
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                currentUserId = btn.dataset.id;
                const row = btn.closest('tr');
                const cells = row.cells;

                userForm.querySelector('[name="matricule"]').value = cells[0].textContent;
                userForm.querySelector('[name="nom"]').value = cells[1].textContent;
                userForm.querySelector('[name="prenom"]').value = cells[2].textContent;
                userForm.querySelector('[name="email"]').value = cells[3].textContent;
                userForm.querySelector('[name="fonction"]').value = cells[4].textContent;
                userForm.querySelector('[name="adresse"]').value = cells[5].textContent;
                userForm.querySelector('[name="date_embauche"]').value = cells[6].textContent;

                document.getElementById('modalTitle').textContent = 'Modifier l\'utilisateur';
                userModal.show();
            });
        });

        // Boutons de suppression
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', () => handleDelete(btn.dataset.id));
        });
    }

    // Initialisation
    loadInitialData();
    attachEventListeners();

    // Écouteurs d'événements globaux
    searchInput.addEventListener('input', e => handleSearch(e.target.value));
    entriesSelect.addEventListener('change', e => {
        // Implémenter la pagination côté client si nécessaire
        console.log('Entries per page:', e.target.value);
    });
    userForm.addEventListener('submit', handleUserSubmit);
    document.getElementById('addNewBtn').addEventListener('click', () => {
        currentUserId = null;
        userForm.reset();
        document.getElementById('modalTitle').textContent = 'Ajouter un utilisateur';
        userModal.show();
    });

    // Gestionnaire d'export
    document.querySelectorAll('.dropdown-item[data-type]').forEach(item => {
        item.addEventListener('click', () => handleExport(item.dataset.type));
    });

    // Gestionnaire de tri pour les en-têtes de colonnes
    table.querySelectorAll('thead th').forEach((th, index) => {
        if (index < table.querySelectorAll('thead th').length - 1) { // Exclure la colonne d'actions
            th.style.cursor = 'pointer';
            th.addEventListener('click', () => {
                const currentDirection = th.dataset.direction === 'asc' ? 'desc' : 'asc';
                th.dataset.direction = currentDirection;
                handleSort(Object.keys(users[0])[index], currentDirection);
            });
        }
    });
});