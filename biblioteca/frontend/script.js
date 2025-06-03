const API_URL = 'http://localhost:8000';

// Управління вкладками
function openTab(tabName) {
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = 'none';
    }
    
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    
    document.getElementById(tabName).style.display = 'block';
    event.currentTarget.classList.add('active');
    
    // Оновлення даних при переключенні вкладок
    if (tabName === 'usuarios') loadUsuarios();
    if (tabName === 'materiales') loadMateriales();
    if (tabName === 'prestamos') loadPrestamos();
}

// Динамічні поля для матеріалів
document.getElementById('tipo-material').addEventListener('change', function() {
    const tipo = this.value;
    const camposDiv = document.getElementById('campos-adicionales');
    camposDiv.innerHTML = '';
    
    if (tipo === 'libro') {
        camposDiv.innerHTML = `
            <input type="text" id="autor" placeholder="Автор">
            <input type="text" id="isbn" placeholder="ISBN">
            <input type="number" id="numero-paginas" placeholder="Кількість сторінок">
        `;
    } else if (tipo === 'revista') {
        camposDiv.innerHTML = `
            <input type="text" id="fecha-publicacion" placeholder="Дата публікації (YYYY-MM-DD)">
            <input type="text" id="numero-edicion" placeholder="Номер видання">
        `;
    } else if (tipo === 'dvd') {
        camposDiv.innerHTML = `
            <input type="number" id="duracion" placeholder="Тривалість (хвилини)">
            <input type="text" id="director" placeholder="Режисер">
        `;
    }
});

// Обробка форм
document.getElementById('usuario-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const apellido = document.getElementById('apellido').value;
    
    try {
        const response = await fetch(`${API_URL}/usuarios/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ nombre, apellido }),
        });
        
        if (response.ok) {
            loadUsuarios();
            this.reset();
        } else {
            alert('Помилка при додаванні користувача');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

document.getElementById('material-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const tipo = document.getElementById('tipo-material').value;
    const titulo = document.getElementById('titulo').value;
    
    let materialData = { tipo, titulo };
    
    if (tipo === 'libro') {
        materialData.autor = document.getElementById('autor').value;
        materialData.isbn = document.getElementById('isbn').value;
        materialData.numero_paginas = document.getElementById('numero-paginas').value;
    } else if (tipo === 'revista') {
        materialData.fecha_publicacion = document.getElementById('fecha-publicacion').value;
        materialData.numero_edicion = document.getElementById('numero-edicion').value;
    } else if (tipo === 'dvd') {
        materialData.duracion = document.getElementById('duracion').value;
        materialData.director = document.getElementById('director').value;
    }
    
    try {
        const response = await fetch(`${API_URL}/materiales/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(materialData),
        });
        
        if (response.ok) {
            loadMateriales();
            this.reset();
            document.getElementById('campos-adicionales').innerHTML = '';
        } else {
            alert('Помилка при додаванні матеріалу');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

document.getElementById('prestamo-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const idUsuario = document.getElementById('id-usuario').value;
    const idMaterial = document.getElementById('id-material').value;
    
    try {
        const response = await fetch(`${API_URL}/prestamos/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id_usuario: idUsuario, id_material: idMaterial }),
        });
        
        if (response.ok) {
            loadPrestamos();
            this.reset();
        } else {
            alert('Помилка при створенні позики');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

// Завантаження даних
async function loadUsuarios() {
    try {
        const response = await fetch(`${API_URL}/usuarios/`);
        const usuarios = await response.json();
        
        const usuariosList = document.getElementById('usuarios-list');
        usuariosList.innerHTML = '';
        
        usuarios.forEach(usuario => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h3>${usuario.nombre} ${usuario.apellido}</h3>
                <p><strong>ID:</strong> ${usuario.id_usuario}</p>
                <button onclick="viewUserInfo('${usuario.id_usuario}')">Інформація</button>
            `;
            usuariosList.appendChild(card);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadMateriales() {
    try {
        const response = await fetch(`${API_URL}/materiales/`);
        const materiales = await response.json();
        
        const materialesList = document.getElementById('materiales-list');
        materialesList.innerHTML = '';
        
        materiales.forEach(material => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h3>${material.titulo}</h3>
                <p><strong>Тип:</strong> ${material.tipo}</p>
                <p><strong>Код:</strong> ${material.codigo_inventario}</p>
                ${material.autor ? `<p><strong>Автор:</strong> ${material.autor}</p>` : ''}
                ${material.isbn ? `<p><strong>ISBN:</strong> ${material.isbn}</p>` : ''}
            `;
            materialesList.appendChild(card);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

async function loadPrestamos() {
    try {
        const response = await fetch(`${API_URL}/prestamos/`);
        const prestamos = await response.json();
        
        const prestamosList = document.getElementById('prestamos-list');
        prestamosList.innerHTML = '';
        
        prestamos.forEach(prestamo => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h3>Позика #${prestamo.id}</h3>
                <p><strong>Користувач ID:</strong> ${prestamo.id_usuario}</p>
                <p><strong>Матеріал ID:</strong> ${prestamo.id_material}</p>
                <p><strong>Дата позики:</strong> ${new Date(prestamo.fecha_prestamo).toLocaleDateString()}</p>
                <p><strong>Дата повернення:</strong> ${new Date(prestamo.fecha_devolucion).toLocaleDateString()}</p>
            `;
            prestamosList.appendChild(card);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// Перегляд інформації про користувача
async function viewUserInfo(userId) {
    try {
        const response = await fetch(`${API_URL}/usuarios/${userId}/info`);
        const userInfo = await response.json();
        
        alert(`
            Інформація про користувача:
            Ім'я: ${userInfo.nombre} ${userInfo.apellido}
            Позики: ${userInfo.prestamos.length > 0 ? 
                userInfo.prestamos.map(p => `\n- ${p[1]} (повернення до ${new Date(p[2]).toLocaleDateString()})`).join('') : 
                'Немає активних позик'}
        `);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Ініціалізація при завантаженні сторінки
window.onload = function() {
    loadUsuarios();
};