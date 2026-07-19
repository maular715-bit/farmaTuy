document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('search-input');
  const btn = document.getElementById('search-btn');
  const results = document.getElementById('results');
  let currentPage = 1;
  let totalPages = 1;

  function render(items) {
    if (!items || items.length === 0) {
      results.innerHTML = '<div class="alert alert-secondary">No se encontraron productos.</div>';
      return;
    }
    let html = '<div class="list-group">';
    for (const m of items) {
      const name = m.medicamento || m.name || '';
      const desc = m.descripcion ? `<p class="mb-0 small">${m.descripcion}</p>` : '';
      html += `<a href="/medicamentos/${m.id}/" class="list-group-item list-group-item-action">
        <div class="d-flex w-100 justify-content-between">
          <h5 class="mb-1">${name}</h5>
        </div>
        ${desc}
      </a>`;
    }
    html += '</div>';
    results.innerHTML = html;
  }

  function renderWithPagination(payload) {
    render(payload.results);
    currentPage = payload.page || 1;
    totalPages = payload.total_pages || 1;

    const pager = document.createElement('div');
    pager.className = 'd-flex justify-content-between align-items-center mt-2';

    const info = document.createElement('div');
    info.innerText = `Página ${currentPage} de ${totalPages} — ${payload.total || 0} resultados`;

    const controls = document.createElement('div');

    const prev = document.createElement('button');
    prev.className = 'btn btn-sm btn-outline-primary me-2';
    prev.innerText = 'Anterior';
    prev.disabled = currentPage <= 1;
    prev.addEventListener('click', () => { if (currentPage>1) { currentPage -= 1; doSearch(); } });

    const next = document.createElement('button');
    next.className = 'btn btn-sm btn-outline-primary';
    next.innerText = 'Siguiente';
    next.disabled = currentPage >= totalPages;
    next.addEventListener('click', () => { if (currentPage<totalPages) { currentPage += 1; doSearch(); } });

    controls.appendChild(prev);
    controls.appendChild(next);

    pager.appendChild(info);
    pager.appendChild(controls);

    results.appendChild(pager);
  }

  async function doSearch() {
    const q = input.value.trim();
    if (!q) {
      results.innerHTML = '';
      return;
    }
    results.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Cargando...</span></div>';
    try {
      const url = `/api/medicamentos/search/?q=${encodeURIComponent(q)}&page=${currentPage}`;
      const r = await fetch(url);
      if (!r.ok) throw new Error('Error en la búsqueda');
      const data = await r.json();
      // API devuelve {results, page, page_size, total, total_pages}
      if (data.results) {
        renderWithPagination(data);
      } else {
        render(data);
      }
    } catch (e) {
      results.innerHTML = `<div class="alert alert-danger">${e.message}</div>`;
    }
  }

  btn.addEventListener('click', doSearch);
  input.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter') {
      ev.preventDefault();
      doSearch();
    }
  });
});
