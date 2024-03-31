const inputs = document.getElementsByTagName('input');
const button = document.getElementById('update');

let isUpdating = false;

button.addEventListener('click', () => {
    isUpdating = !isUpdating;

    if (isUpdating) {
        // Make fields editable and change button text
        for (let i = 3; i < 11; i++) {
            document.getElementsByTagName("input")[i].readOnly = false;
            document.getElementsByTagName("input")[i].style.borderWidth = "5px";
        }
        button.innerText = 'SAVE';
    } else {
        update_profile();
        window.location.reload();
    }
});

async function update_profile() {
    const data = {};
    const inputs = document.getElementsByTagName('input');

    for (let i = 3; i < 11; i++) {
        let input = inputs[i];
        data[input.name] = input.value;
    }

    const formData = new URLSearchParams();
    for (const [key, value] of Object.entries(data)) {
        formData.append(key, value);
    }

    const response = await fetch('/update_profile/', {
        method: 'POST',
        body: formData,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
        credentials: 'same-origin',
    });


    if (response.ok) {
        console.log('Profile updated successfully');
        window.location.reload();
    } else {
        console.log('Error updating profile');
    }
}
