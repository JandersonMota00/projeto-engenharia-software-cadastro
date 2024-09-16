// Add event listeners to the navigation links
const navLinks = document.querySelectorAll('.sidebar a');
navLinks.forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    // Handle navigation logic here (e.g., load content, scroll to section, etc.)
    console.log('Link clicked:', link.textContent);
  });
});

// Add event listeners to the grid items
const gridItems = document.querySelectorAll('.grid-item');
gridItems.forEach(item => {
  item.addEventListener('click', event => {
    event.preventDefault();
    // Handle grid item click logic here (e.g., display modal, navigate to page, etc.)
    console.log('Grid item clicked:', item.textContent);
  });
});
