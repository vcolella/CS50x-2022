// Get modal element
var factModal = document.getElementById('factModal');

// Listening for show
factModal.addEventListener('show.bs.modal', function (event) {
  // Button that triggered the modal
  console.log("showing modal");
  var button = event.relatedTarget;

  // Update the modal's content.
  var modalTitle = factModal.querySelector('.modal-title');
  var modalBody = factModal.querySelector('.modal-body');

  // Using api to get data
  const options = {
            method: 'GET',
            headers: {
                'X-RapidAPI-Key': '77672a95damsh7948dab7cfd7c4fp177ec6jsn0bbf88717388',
                'X-RapidAPI-Host': 'numbersapi.p.rapidapi.com'
            }
        };

        fetch('https://numbersapi.p.rapidapi.com/6/21/date?fragment=true&json=true', options)
            .then(response => response.json())
            .then(response => {
                modalTitle.textContent = 'In ' + response.year + ' ...';
                modalBody.textContent = response.text;
            })
            .catch(err => console.error(err));
});