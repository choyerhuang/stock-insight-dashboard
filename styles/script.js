document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchResults = document.getElementById('searchResults');

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(searchForm);
        const query = formData.get('name');

        fetch('/search', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            searchResults.innerHTML = `<p>${data}</p>`;
        })
        .catch(error => console.error('Error:', error));
    });
});

const searchInput = document.getElementById('name');

function search() {
  const query = searchInput.value;
  if (query.trim() == '') {
    alert('Please enter a city.');
    return;
  }
  // execute search functionality
}