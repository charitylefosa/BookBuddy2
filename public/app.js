const API_KEY = 'AIzaSyDbde2mN1C-qESuiYnIPF3H0jSsl4ZA6Oo';
const API_URL = `https://www.googleapis.com/books/v1/volumes?key=${API_KEY}&q=`;

async function fetchBooks(query) {
  try {
    const url = `${API_URL}${encodeURIComponent(query)}`;
    console.log('Fetching books from URL:', url); // Debugging line
    const response = await axios.get(url);
    console.log('Response:', response); // Debugging line
    if (response.data.items && response.data.items.length > 0) {
      displayResults(response.data.items);
    } else {
      displayNoResults();
    }
  } catch (error) {
    console.error('Error fetching books:', error);
    displayError();
  }
}

function displayResults(books) {
  const resultsContainer = document.getElementById('search-results');
  resultsContainer.innerHTML = ''; // Clear previous results

  books.forEach(book => {
    const bookCard = document.createElement('div');
    bookCard.className = 'book-card';

    const bookInfo = book.volumeInfo;

    const bookTitle = document.createElement('h3');
    bookTitle.textContent = bookInfo.title;

    const bookAuthors = document.createElement('p');
    bookAuthors.textContent = bookInfo.authors ? `by ${bookInfo.authors.join(', ')}` : 'Unknown Author';

    const bookDescription = document.createElement('p');
    bookDescription.textContent = bookInfo.description || 'No description available.';

    const bookRating = document.createElement('p');
    bookRating.textContent = bookInfo.averageRating ? `Average Rating: ${bookInfo.averageRating}` : 'No rating available.';

    // Add book cover
    const bookCover = document.createElement('img');
    if (bookInfo.imageLinks && bookInfo.imageLinks.thumbnail) {
      bookCover.src = bookInfo.imageLinks.thumbnail;
    } else {
      bookCover.src = 'https://via.placeholder.com/100x150.png?text=No+Cover'; // Placeholder image URL
    }
    bookCover.alt = `${bookInfo.title} cover image`;

    // Add view button
    const viewButton = document.createElement('button');
    viewButton.textContent = 'View Book';
    viewButton.onclick = () => {
      const isbn = bookInfo.industryIdentifiers ? bookInfo.industryIdentifiers[0].identifier : null;
      if (isbn) {
        initializeViewer(isbn);
      } else {
        alert('ISBN not available for this book');
      }
    };

    bookCard.appendChild(bookCover); // Append book cover before title
    bookCard.appendChild(bookTitle);
    bookCard.appendChild(bookAuthors);
    bookCard.appendChild(bookDescription);
    bookCard.appendChild(bookRating);
    bookCard.appendChild(viewButton);

    resultsContainer.appendChild(bookCard);
  });
}

function displayNoResults() {
  const resultsContainer = document.getElementById('search-results');
  resultsContainer.innerHTML = '<p>No books found. Please try a different search query.</p>';
}

function displayError() {
  const resultsContainer = document.getElementById('search-results');
  resultsContainer.innerHTML = '<p>Error fetching books. Please try again later.</p>';
}

// Ensure Google Books API is loaded before attaching event listeners
google.books.load();
google.books.setOnLoadCallback(function() {
  document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-bar').value;
    if (query) {
      fetchBooks(query);
    }
  });
});

function initializeViewer(isbn) {
  var viewer = new google.books.DefaultViewer(document.getElementById('viewerCanvas'));
  viewer.load('ISBN:' + isbn);
}

