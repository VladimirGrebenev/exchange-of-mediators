
document.addEventListener('DOMContentLoaded', function () {
    var profileImageInput = document.getElementById('profile_image');
    var avatarImage = document.getElementById('avatar_image');

    if (profileImageInput) {
        profileImageInput.addEventListener('change', function () {
            var file = profileImageInput.files[0];
            var reader = new FileReader();

            reader.onload = function (e) {
                avatarImage.src = e.target.result;
            };

            reader.readAsDataURL(file);
        });
    }
});